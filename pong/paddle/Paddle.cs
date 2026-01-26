using Godot;
using System;

public partial class Paddle : CharacterBody2D
{
	public const float Speed = 50.0f;

	private float PreviousInputPosition {get; set;} = 0;


	[Export]
	public string RotaryAction = "0_rotary_moved";

	public override void _PhysicsProcess(double delta)
	{
		MoveAndCollide(new Vector2(0, (float)(Velocity.Y * delta)));
		Velocity = new Vector2(0, Velocity.Y - 1);
		var screenSize = GetViewportRect().Size;
		var paddleHeight = 32;
		Position = new Vector2(Position.X, Math.Clamp(Position.Y, paddleHeight / 2, screenSize.Y - (paddleHeight / 2)));
	}

    public override void _Input(InputEvent @event)
    {
        if (@event.IsAction(RotaryAction))
		{
			var eRotaryAction = @event as ControllerInputEventAction;
			var positionDiff = eRotaryAction.Position - PreviousInputPosition;
			Velocity = new Vector2(0, positionDiff*Speed);
			PreviousInputPosition = eRotaryAction.Position;

		}
    }

}
