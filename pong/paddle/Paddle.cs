using Godot;
using System;

public partial class Paddle : CharacterBody2D
{
	private float PreviousInputPosition {get; set;} = 0;

	[Export]
	public string RotaryAction = "0_rotary_moved";

    public override void _Input(InputEvent @event)
    {
        if (@event.IsAction(RotaryAction))
		{
			var eRotaryAction = @event as ControllerInputEventAction;
			var positionDiff = eRotaryAction.Position - PreviousInputPosition;
			PreviousInputPosition = eRotaryAction.Position;
			var moveDiff = positionDiff * 32;
			Position = new Vector2(Position.X, Position.Y + moveDiff);

		}
    }

}
