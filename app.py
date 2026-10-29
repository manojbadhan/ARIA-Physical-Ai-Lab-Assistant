import time
from flask import Flask, Response, jsonify, render_template_string
from main import ARIA

app = Flask(__name__)
aria = ARIA()
aria.start()

PAGE = """
<!doctype html>
<title>ARIA</title>
<style>
  body { font-family: system-ui; background:#111; color:#eee; margin:0; padding:20px; }
  .wrap { display:flex; gap:20px; flex-wrap:wrap; }
  img { max-width:100%; border-radius:8px; }
  .panel { background:#1c1c1c; padding:16px; border-radius:8px; min-width:260px; }
  button { padding:8px 16px; border:0; border-radius:6px; cursor:pointer; }
</style>
<h2>ARIA</h2>
<div class="wrap">
  <img src="/video" width="640">
  <div class="panel">
    <h3>Status</h3>
    <pre id="status">loading...</pre>
    <button onclick="fetch('/quit', {method:'POST'})">Stop</button>
  </div>
</div>
<script>
  setInterval(async () => {
    const r = await fetch('/status');
    document.getElementById('status').textContent = JSON.stringify(await r.json(), null, 2);
  }, 1000);
</script>
"""

def mjpeg():
    while True:
        jpg = aria.get_jpeg()
        if jpg:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
        time.sleep(0.03)

@app.route("/")
def index():
    return render_template_string(PAGE)

@app.route("/video")
def video():
    return Response(mjpeg(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/status")
def status():
    return jsonify({"running": not aria.s.quit.is_set()})

@app.route("/quit", methods=["POST"])
def quit_():
    aria.stop()
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)