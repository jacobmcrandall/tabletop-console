public class ControllerMessage
{
    public char KeyType { get; set; }
    public int Index { get; set; } = 0;
    public int R { get; set; } = 0;
    public int G { get; set; } = 0;
    public int B { get; set; } = 0;
    public double? Brightness { get; set; } = 1.0;
}