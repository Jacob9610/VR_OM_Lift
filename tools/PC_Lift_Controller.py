import FreeSimpleGUI as sg
import socket
import json
import threading
import requests
from PIL import Image
from io import BytesIO

# === CONFIG ===
PI_IP = "10.143.230.242"
PORT = 8000
STREAM_URL = f"http://{PI_IP}:8080/?action=snapshot"

# === Send JSON Command ===
def send_command(cmd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((PI_IP, PORT))
            s.send(json.dumps(cmd).encode())
    except Exception as e:
        print(f"Error: {e}")

# === Background Camera Thread ===
def update_stream(window):
    while True:
        try:
            r = requests.get(STREAM_URL, timeout=1)
            if r.status_code == 200:
                img = Image.open(BytesIO(r.content))
                img.thumbnail((320, 240))
                bio = BytesIO()
                img.save(bio, format="PNG")
                window.write_event_value("-STREAM-", bio.getvalue())
        except:
            pass

# === GUI Layout ===
layout = [
    [sg.Image(key="-IMAGE-")],
    [sg.Multiline(size=(45, 8), key="-LOG-", autoscroll=True)],
    [sg.Text("Use WASD for drive, arrows for lift/spin")],
    [
        sg.Button("Lift Max", size=(10, 1), key="LIFT_MAX"),
        sg.Button("Lift Zero", size=(10, 1), key="LIFT_ZERO"),
        sg.Button("Nudge Left", size=(12, 1), key="NUDGE_LEFT"),
        sg.Button("Nudge Right", size=(12, 1), key="NUDGE_RIGHT")
    ],
    [
        sg.Button("Stop", size=(10, 1), key="STOP"),
        sg.Button("Quit") 
    ]
]

window = sg.Window("PC_Lift_Controller", layout, finalize=True, return_keyboard_events=True)

threading.Thread(target=update_stream, args=(window,), daemon=True).start()

# === Key Map ===
keymap = {
    "w": {"command": "forward"},
    "s": {"command": "backward"},
    "a": {"command": "left"},
    "d": {"command": "right"},
    "Left:37": {"command": "spin_left"},
    "Right:39": {"command": "spin_right"},
    "Up:38": {"command": "lift_up"},
    "Down:40": {"command": "lift_down"},
}

# === Event Loop ===
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Quit":
        break

    elif event == "STOP":
        send_command({"command": "all_stop"})
        window["-LOG-"].print("Sent: all_stop")

    elif event == "LIFT_MAX":
        send_command({"command": "lift_max"})
        window["-LOG-"].print("Sent: lift_max")

    elif event == "LIFT_ZERO":
        send_command({"command": "lift_zero"})
        window["-LOG-"].print("Sent: lift_zero")

    elif event == "NUDGE_LEFT":
        send_command({"command": "nudge_left"})
        window["-LOG-"].print("Sent: nudge_left")

    elif event == "NUDGE_RIGHT":
        send_command({"command": "nudge_right"})
        window["-LOG-"].print("Sent: nudge_right")

    elif event == "-STREAM-":
        window["-IMAGE-"].update(data=values["-STREAM-"])

    elif event in keymap:
        cmd = keymap[event]
        send_command(cmd)
        window["-LOG-"].print(f"Sent: {json.dumps(cmd)}")

window.close()
