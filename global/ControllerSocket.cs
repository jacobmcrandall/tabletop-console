using Godot;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public partial class ControllerSocket : Node
{
	private const int socketPort = 1031;
	private Socket connection {get; set;} = null;

	public override void _Ready()
	{
		StartServer();
	}

	public async Task SendMessage(List<ControllerMessage> messages)
	{
		if (connection == null)
			return;
		
		await connection.SendAsync(JsonSerializer.Serialize(messages).ToAsciiBuffer(), SocketFlags.None);
	}

	private async Task StartController()
	{
		Process process = new Process();
		process.StartInfo = new ProcessStartInfo
		{
			WindowStyle = ProcessWindowStyle.Normal,
			FileName = "python.exe",
			Arguments = "./controller/main.py"
		};
		process.Start();
	}

	private async Task StartServer()
	{
		var listenSocket = new Socket(SocketType.Stream, ProtocolType.Tcp);
		listenSocket.Bind(new IPEndPoint(IPAddress.Loopback, socketPort));

		GD.Print($"Listening on {listenSocket.LocalEndPoint}");
		listenSocket.Listen();

		StartController();

		while (true)
		{
			// Wait for a new connection to arrive
			connection = await listenSocket.AcceptAsync();

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

						string resultString = Encoding.UTF8.GetString(buffer[..read]);
						GD.Print(resultString);
						var inputs = JsonSerializer.Deserialize<ControllerInput[]>(resultString, new JsonSerializerOptions {PropertyNameCaseInsensitive = true});
						foreach(var input in inputs)
						{
							var inputAction = input.AsInputEventAction();
							Input.ParseInputEvent(inputAction);
							// Input.ActionRelease(input.Action);
						}
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
