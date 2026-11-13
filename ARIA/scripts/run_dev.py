import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from backend.app import create_app
create_app().run(debug=True, port=5000)
