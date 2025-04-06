PC_Lift_Controller Tool
A lightweight Python GUI to control your forklift wirelessly from a PC. Includes real-time camera feed, keyboard control, and command logging.

Features
JSON socket control to Raspberry Pi

Keyboard mappings:

WASD = Drive commands are a little slow be careful!!!

⬅️➡️ = Spin

⬆️⬇️ = Lift up/down

🖱 Buttons for:

Lift Max, Lift Zero

Nudge Left, Nudge Right

Stop, Quit

 Live MJPEG camera snapshots

 Command log with timestamps

 How to Run
Make sure your Pi server is running:

bash
Copy
Edit
./start_pi_services.sh
On your PC (Python 3.8+), install dependencies:

bash
Copy
Edit
pip install FreeSimpleGUI requests pillow
Launch the GUI:

bash
Copy
Edit
python3 PC_Lift_Controller.py
Make sure to update the PI_IP variable if needed.