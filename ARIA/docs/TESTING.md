# Testing

`pytest -q` runs unit, API, integration and hardware-protocol tests. They need only flask, numpy, python-dotenv and pytest; no API keys, camera or GPU.
Manual checks on the robot: wake word ignored without "ARIA", TTS under 3 s, camera index opens, "where is X" returns a photo.
