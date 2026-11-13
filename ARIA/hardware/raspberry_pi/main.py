"""Voice + vision loop for the robot. Run with: python main.py --pi"""
import time
from ai_engine.orchestration.agent import Agent
from ai_engine.speech.wake_word import WakeWord
from hardware.raspberry_pi.audio_controller import listen, speak

def run():
    agent, wake = Agent(), WakeWord()
    cam = None
    try:
        from hardware.raspberry_pi.camera_controller import CameraController
        cam = CameraController()
    except Exception as e:
        print("Camera unavailable:", e)
    print("ARIA ready. Say 'ARIA' to start.")
    history = []
    while True:
        text = listen()
        if not text: continue
        cmd = wake.process(text)
        if cmd is None: continue            # wake word enforced: ignore everything else
        out = agent.handle(cmd, history)
        if out["intent"] == "vision" and cam:
            label = cam.identify(); out["reply"] = f"I can see {label}." if label else "I could not recognise that."
        history += [{"role": "user", "content": cmd}, {"role": "assistant", "content": out["reply"]}]
        speak(out["reply"]); wake.extend()
        time.sleep(0.2)

if __name__ == "__main__":
    run()
