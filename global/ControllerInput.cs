using Godot;

public class ControllerInput
{
   public string Action {get;set;}
   public int? Strength {get;set;}
   public bool? Pressed {get;set;}

   public InputEventAction AsInputEventAction()
    {
        var input = new ControllerInputEventAction();
        input.Action = this.Action;
        input.Strength = this.Strength ?? 0;
        input.Pressed = this.Pressed ?? false;
        input.Position = this.Strength ?? 0;
        // GD.Print($"Action: {input.Action} | Strength: {input.Strength} | Pressed: {input.Pressed}");
        return input;
    }
}

public partial class ControllerInputEventAction : InputEventAction
{
   public int Position {get;set;}
}