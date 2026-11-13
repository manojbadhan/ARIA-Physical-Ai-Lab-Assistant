"""Run ARIA:  python main.py        (web app on http://localhost:5000)
             python main.py --pi   (voice+vision loop on the Raspberry Pi)"""
import sys
from backend.app import create_app

if __name__ == "__main__":
    if "--pi" in sys.argv:
        from hardware.raspberry_pi.main import run
        run()
    else:
        from backend.config import Config
        create_app().run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
