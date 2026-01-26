using Godot;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;


public partial class ControllerSocket : Node
{
	public override void _Ready()
	{
		Server();
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}

	private async Task Client()
	{
		using var socket = new Socket(SocketType.Stream, ProtocolType.Tcp);
		await socket.ConnectAsync(new IPEndPoint(IPAddress.Loopback, 8080));

		Console.WriteLine("Type into the console to echo the contents");

		var ns = new NetworkStream(socket);
		var readTask = Console.OpenStandardInput().CopyToAsync(ns);
		var writeTask = ns.CopyToAsync(Console.OpenStandardOutput());

		// Quit if any of the tasks complete
		await Task.WhenAny(readTask, writeTask);
	}

	private async Task Server()
	{
		var listenSocket = new Socket(SocketType.Stream, ProtocolType.Tcp);
		listenSocket.Bind(new IPEndPoint(IPAddress.Loopback, 1031));

		GD.Print($"Listening on {listenSocket.LocalEndPoint}");

		listenSocket.Listen();

		while (true)
		{
			// Wait for a new connection to arrive
			var connection = await listenSocket.AcceptAsync();

			// We got a new connection spawn a task to so that we can echo the contents of the connection
			_ = Task.Run(async () =>
			{
				GD.Print("Received Connection");
				var buffer = new byte[4096];
				try
				{
					while (true)
					{
						int read = await connection.ReceiveAsync(buffer, SocketFlags.None);
						if (read == 0)
						{
							break;
						}

						// to send data back to the connection
						// await connection.SendAsync(buffer[..read], SocketFlags.None);
						string resultString = Encoding.UTF8.GetString(buffer[..read]);
						GD.Print(resultString);
						var inputs = JsonSerializer.Deserialize<ControllerInput[]>(resultString, new JsonSerializerOptions {PropertyNameCaseInsensitive = true});
						foreach(var input in inputs)
						{
							// GetViewport().PushInput(input.AsInputEventAction());
							var inputAction = input.AsInputEventAction();
							Input.ParseInputEvent(inputAction);
							// Input.ActionRelease(input.Action);
						}

						// CallDeferred("emit_signal", SignalName.OnControllerMessageReceived, input);
						// There exists issues in calling emit signal from a thread so defer as above
						// EmitSignal(SignalName.OnControllerMessageReceived, result);
					}
				}
				catch(Exception e)
				{
					GD.Print(e.Message);
				}
				finally
				{
					connection.Dispose();
				}
			});
		}
	}
}
