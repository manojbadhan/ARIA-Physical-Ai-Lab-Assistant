import subprocess, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(root / "requirements.txt")])
subprocess.check_call([sys.executable, str(root / "scripts" / "initialize_database.py")])
print("Setup done. Copy .env.example to .env and add API keys.")
