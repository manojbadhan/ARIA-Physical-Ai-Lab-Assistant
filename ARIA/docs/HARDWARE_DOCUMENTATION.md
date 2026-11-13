# Hardware

- Raspberry Pi 5 running `python main.py --pi`; USB mic and speaker; depth/RGB camera (find the RGB node with `v4l2-ctl --list-devices`, set `CAMERA_INDEX`).
- ESP32 / Arduino talk over USB serial at 115200 baud using JSON lines (`hardware/communication/serial_handler.py`). Firmware in `hardware/esp32/firmware` and `hardware/arduino/firmware`.
- Speed settings that mattered: force Whisper `language=en`, use VAD so silence is not transcribed, use a medium/low Piper or Edge voice.
