# VR_OM_Lift

A VR-controlled robotic forklift powered by a Raspberry Pi 4, Unity, OpenXR, and real-time PC tooling. This project combines physical hardware control, live streaming, and immersive virtual input using the Meta Quest.

---

## 📁 Project Structure

```
VR_OM_Lift/
├── unity/           # Unity project for VR control (OpenXR + Meta Quest)
├── stl/             # 3D models for physical rig (e.g., forklift parts)
├── pi/              # Raspberry Pi motor + stream control
│   ├── motor_server.py
│   ├── start_pi_services.sh
│   └── stream/      # MJPEG streamer source
├── tools/           # PC-based utilities (e.g., GUI controller)
│   └── PC_Lift_Controller.py
└── README.md        # This file
```

---

##  Components

### 🖥️ Unity (Meta Quest)
- Uses Unity 6 with XR Plugin Management + OpenXR
- Input system maps Quest controller inputs to JSON commands
- Controls motor and lift via TCP socket

###  Raspberry Pi
- Runs `motor_server.py` to accept and process socket commands
- Starts video stream using `mjpg_streamer`
- Powered by L298N (DC motors) and ULN2003 (stepper lift)

###  PC_Lift_Controller (Tools)
- GUI tool written in Python + PySimpleGUI
- WASD and Arrow Key controls
- Real-time command logging
- Snapshots from MJPEG stream
- Works wirelessly over the same network

---

## 🚀 How to Run

### On the Pi
```bash
cd ~/Documents/VR_OM_Lift/pi
chmod +x start_pi_services.sh
./start_pi_services.sh
```
This launches both `pigpiod`, the MJPEG stream, and motor control server.

### On the PC
```bash
cd VR_OM_Lift/tools
pip install FreeSimpleGUI requests pillow
python3 PC_Lift_Controller.py
```

---

##  Controls (Quest or PC)

| Action     | Quest Input / PC Key  | Command Sent     |
|------------|------------------------|------------------|
| Forward    | Left Stick Up / W      | forward          |
| Backward   | Left Stick Down / S    | backward         |
| Left       | Left Stick Left / A    | left             |
| Right      | Left Stick Right / D   | right            |
| Spin       | Right Stick X / Arrows | spin_left/right  |
| Lift       | Triggers / Arrows      | lift_up/down     |
| Stop       | UI / Key               | all_stop         |

Also supports: `lift_max`, `lift_zero`, `nudge_left`, `nudge_right`

---

##  Streaming

- Accessible at `http://<PI_IP>:8080/?action=stream`
- Works in browsers (including Quest browser)
- Can be pulled into Unity or Python GUI

---

##  Wiring and Circuit Documentation

###  Camera
| Component         | Connection                |
|------------------|---------------------------|
| Logitech USB Cam | USB Port (Auto-detects)   |

###  DC Motors (L298N Motor Driver)
| Motor            | L298N IN1/IN2 | Pi GPIO | Description           |
|------------------|--------------|---------|-----------------------|
| Left Motor       | IN1 / IN2    | 17 / 27 | Forward/Reverse       |
| Right Motor      | IN3 / IN4    | 23 / 24 | Forward/Reverse       |
| Enable Pins      | ENA / ENB    | Jumper  | Always ON (jumpered)  |
| Power (12V/5V)   | VIN / GND    | External supply         |

###  Stepper Motor (28BYJ-48 + ULN2003)
| IN# on ULN2003   | Pi GPIO Pin  | Note                    |
|------------------|--------------|-------------------------|
| IN1              | GPIO 5       | Step signal             |
| IN2              | GPIO 6       |                         |
| IN3              | GPIO 13      |                         |
| IN4              | GPIO 19      |                         |
| 5V + GND         | Pi + External| Shared power rail       |

###  Raspberry Pi GPIO Summary
| Purpose         | GPIO Pin(s)           |
|------------------|------------------------|
| DC Motor L       | 17 (IN1), 27 (IN2)     |
| DC Motor R       | 23 (IN3), 24 (IN4)     |
| Stepper IN1–4    | 5, 6, 13, 19           |
| pigpiod control  | Required on boot       |

---

## 🛠 Built With
- Python 3
- PySimpleGUI
- MJPEG Streamer
- Unity 6 + OpenXR
- Raspberry Pi GPIO + pigpio

---

##  Devpost
This project was created during a hardware-focused hackathon.

 [Check out the Devpost Submission](https://devpost.com/) _(Insert final link here)_

Includes:
- Full write-up
- Demo video
- Team insights and project reflection

---

Let us know if you want a 1-pager, slide deck, or printable version for showcase or resume!