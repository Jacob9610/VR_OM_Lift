using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.XR;

public class InputReader : MonoBehaviour
{
    public InputActionAsset inputActions;

    private InputAction moveAction;
    private InputAction spinAction;
    private InputAction liftUpAction;
    private InputAction liftDownAction;

    private PiCommandClient client = new PiCommandClient();

    private void OnEnable()
    {
        var gameplay = inputActions.FindActionMap("Gameplay");
        moveAction = gameplay.FindAction("Move");
        spinAction = gameplay.FindAction("Spin");
        liftUpAction = gameplay.FindAction("LiftUp");
        liftDownAction = gameplay.FindAction("LiftDown");

        gameplay.Enable();
    }

    private void Update()
    {
        Vector2 move = moveAction.ReadValue<Vector2>();
        float spin = spinAction.ReadValue<float>();
        bool liftUp = liftUpAction.ReadValue<float>() > 0.5f;
        bool liftDown = liftDownAction.ReadValue<float>() > 0.5f;

        int left = 0;
        int right = 0;

        // Forward/back
        if (move.y > 0.3f)
        {
            left = 1;
            right = 1;
        }
        else if (move.y < -0.3f)
        {
            left = -1;
            right = -1;
        }

        // Turn left/right
        if (move.x > 0.3f)
        {
            left = 1;
            right = 0;
        }
        else if (move.x < -0.3f)
        {
            left = 0;
            right = 1;
        }

        // Spin in place (right stick X)
        if (Mathf.Abs(spin) > 0.3f)
        {
            left = spin > 0 ? 1 : -1;
            right = -left;
        }

        // Send drive command
        string driveCmd = $"{{\"drive\":{{\"left_motor\":{left},\"right_motor\":{right}}}}}";
        client.SendCommand(driveCmd);

        // Lift
        if (liftUp)
            client.SendCommand("{\"lift\":\"up\"}");
        else if (liftDown)
            client.SendCommand("{\"lift\":\"down\"}");
    }
}
