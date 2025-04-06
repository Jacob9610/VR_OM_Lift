#!/bin/bash

echo "🔧 Starting pigpiod..."
sudo pigpiod
sleep 1

echo "🔍 Searching for Logitech camera..."
CAMERA_DEV=$(v4l2-ctl --list-devices | grep -A1 "Logitech" | tail -n1 | tr -d '\t')

if [[ ! -e "$CAMERA_DEV" ]]; then
  echo "⚠️ Logitech not found. Trying fallback device..."
  CAMERA_DEV=$(ls /dev/video* | head -n 1)
fi

if [[ ! -e "$CAMERA_DEV" ]]; then
  echo "❌ No camera device found. Exiting."
  exit 1
fi

echo "📷 Using camera: $CAMERA_DEV"

echo "🚀 Starting MJPEG Stream..."
cd ~/Documents/VR_OM_Lift/mjpg-streamer/mjpg-streamer-experimental
./_build/mjpg_streamer \
  -i "./_build/input_uvc.so -d $CAMERA_DEV -r 640x480 -f 30" \
  -o "./_build/output_http.so -p 8080 -w ./www" &

sleep 2

echo "🧠 Starting Motor Server..."
cd ~/Documents/VR_OM_Lift/pi
python3 motor_server.py
