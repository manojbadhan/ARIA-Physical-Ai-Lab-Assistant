# ARIA - Physical AI Lab Assistant

ARIA is a voice assistant that can see. A camera window shows live object detection, and you talk to her out loud. She listens for her name, understands your question, looks at what the camera currently sees, and answers in speech.

> "ARIA, what is this used for?" - while holding a tool in front of the camera.

## What it does

- **Sees:** YOLO runs live on the camera feed and draws boxes on the window.
- **Listens hands-free:** no buttons. She waits for her name ("ARIA"), then keeps listening for 12 seconds for follow-ups.
- **Understands:** speech is turned into text with Groq Whisper, with noise and wrong-language results filtered out.
- **Thinks:** the question, plus the objects the camera sees, goes to an LLM on Groq.
- **Speaks:** the answer is read aloud with text-to-speech. English works out of the box; Hindi works when the machine has a Hindi voice.
- **Shows what she heard:** the window prints the status (listening, hearing you, thinking, speaking) and the text she understood, and draws a microphone level bar.

## How it works

```
 camera ──► LiveDetector (YOLO, background thread) ──► objects currently in view ─┐
                                                                                 │
 mic ──► MicListener (loudness + voice detector) ──► speech-to-text (Groq Whisper)
                         │                                  │
                         │                       wake word check ("ARIA")
                         │                                  │
                         │                                  ▼
                         │            LLM (Groq)  ◄── question + camera objects
                         │                                  │
                         └──── mic muted while speaking ◄── text-to-speech
```

The camera window runs in the main thread. The voice loop runs in its own thread, so the video never freezes while she is thinking or talking.

## Tech stack and APIs

| Part | Technology | Runs on | Used in |
|---|---|---|---|
| Language model | Groq Chat Completions API, model `openai/gpt-oss-120b` (`GROQ_MODEL` in `config.py`), called through the `groq` Python SDK | Groq cloud | `llm/model.py` |
| Speech-to-text | Groq Audio Transcriptions API, Whisper `whisper-large-v3-turbo` (`STT_MODEL` in `config.py`); `whisper-large-v3` is used when `LANGUAGE = "hi"` | Groq cloud | `audio/stt.py`, `assistant.py` |
| Object detection | Ultralytics YOLO11 (`yolo11s.pt`) on PyTorch | your machine | `vision/live_detector.py` |
| Text-to-speech | `pyttsx3` (Windows SAPI5 voices; eSpeak NG on Linux and Raspberry Pi) | your machine | `audio/tts.py` |
| Microphone input | `sounddevice` (PortAudio) | your machine | `audio/listener.py` |
| Voice detection | WebRTC VAD (`webrtcvad-wheels`) plus a `numpy` loudness check | your machine | `audio/listener.py` |
| Camera and window | OpenCV | your machine | `main.py`, `vision/display.py` |
| Settings | `python-dotenv` loads `.env` | your machine | `config.py` |

Only the language model and the speech-to-text need the internet, and both use the same key: `GROQ_API_KEY`. Create one in the Groq console (console.groq.com) and put it in `.env`.

### How the APIs are called

- **Language model:** temperature 0.3, up to 1000 tokens, 30 second timeout, and the last 20 messages (10 exchanges) of conversation. The system prompt is the lab prompt from `llm/prompts.py`, then the voice rules and language rule from `chat/prompts2.py`. A short camera note is added to the question only when it is about something in view.
- **Speech-to-text:** the language is fixed (`en` or `hi`), temperature 0, and a short prompt ("Hello ARIA.") tells Whisper how her name is spelled. The response is requested as `verbose_json`, so each segment's confidence can be checked. Segments that look like silence, low confidence, repetition, or text in the wrong script are dropped.
- **Cost and limits:** each question is one transcription request and one chat request, so usage counts against your Groq plan's rate limits.

### What leaves your computer

- The recorded question (a short WAV file, overwritten each time in the system temp folder) goes to Groq for transcription.
- The transcribed text, the recent conversation, and the **names** of the objects seen (for example "bottle, cell phone") go to Groq's language model.
- Camera images are never sent anywhere. Detection runs locally and only the object names are shared.

### Configured but not used yet

- **RAG settings** already in `config.py`: `all-MiniLM-L6-v2` embeddings (sentence-transformers), notes read from `notes/`, chunks of 400 characters with 50 overlap, top 3 results, a similarity threshold of 0.35, and the index saved under `rag/store/`. `llm/prompts.py` also has a `RAG_SYSTEM_PROMPT`. None of this is connected to `main.py` until the `rag/` code is added.
- **Hindi voice options** that were considered but are not used: Sarvam AI's speech APIs and `edge-tts`.

## Project structure

```
minor_project/
├── main.py                 starts the camera window, the detector and the voice thread
├── assistant.py            the voice loop: listen -> wake word -> speech-to-text -> LLM -> speech
├── config.py               API key and model names (reads .env)
├── .env                    GROQ_API_KEY=...   (never commit this)
├── requirements.txt
├── yolo11s.pt              YOLO weights
│
├── audio/
│   ├── listener.py         hands-free microphone listening (noise rejection, speech detection)
│   ├── stt.py              SpeechToText class (Groq Whisper)
│   └── tts.py              TextToSpeech class (pyttsx3)
├── chat/
│   └── prompts2.py         greeting, spoken-style rules, language rules, camera-note builder
├── llm/
│   ├── model.py            LabAssistantLLM class (Groq)
│   └── prompts.py          lab system prompt
├── vision/
│   ├── live_detector.py    YOLO in a background thread
│   ├── display.py          boxes, status line, "You: ..." text, mic level bar
│   └── camera.py           standalone camera/FPS test
└── rag/                    notes search (placeholder until the RAG code is added)
```

`assistant.py` finds `LabAssistantLLM`, `SpeechToText` and `TextToSpeech` by class name, so it keeps working if you rename those files.

## Setup

**Requirements:** Python 3.10 or newer, a webcam, a microphone and a speaker.

1. Install the packages:

   ```
   pip install opencv-python ultralytics numpy sounddevice webrtcvad-wheels pyttsx3 groq python-dotenv
   ```

   Put the same packages in `requirements.txt`. `webrtcvad-wheels` is the voice detector. Without it ARIA still runs, but she picks up much more background noise.

2. Get a Groq API key and create a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_key_here
   ```

3. Run it from the project root:

   ```
   python main.py
   ```

### Raspberry Pi

```
sudo apt install espeak-ng libportaudio2
```

`espeak-ng` is the speech engine and also provides a Hindi voice. On a Pi, `main.py` automatically uses smaller camera frames and limits YOLO to 4 detections per second so the microphone is not starved of CPU. If the Pi still struggles, try the smaller `yolo11n.pt` weights.

## Using it

1. Start `python main.py`. She greets you and measures the room noise for 2 seconds. **Stay quiet during that time.**
2. Say **"ARIA, ..."** followed by your question, for example "ARIA, what is this?".
3. For the next 12 seconds you can keep talking without repeating her name.
4. Press **Q** in the camera window to quit, or say "goodbye".

Questions with words like "this", "it", "holding" or "in front" get the camera's objects added automatically. Everything else is normal conversation.

## Settings you may want to change

| File | Setting | What it does |
|---|---|---|
| `assistant.py` | `LANGUAGE` | `"en"` or `"hi"`. Hindi needs a Hindi voice on the machine; without one she falls back to English. |
| `assistant.py` | `WAKE_WORD_REQUIRED` | `False` makes her answer everything she hears. |
| `assistant.py` | `WAKE_WORDS`, `ACTIVE_WINDOW` | Accepted spellings of her name, and the follow-up window in seconds. |
| `assistant.py` | `ECHO_TAIL` | Seconds the mic stays deaf after she speaks. Use about 1.5 for a Bluetooth speaker. |
| `audio/listener.py` | `MIC_DEVICE`, `MIC_CHANNELS` | Which microphone to use. `python -m sounddevice` lists devices. |
| `audio/listener.py` | `MIC_THRESHOLD`, `VAD_AGGRESSIVENESS` | Loudness bar and strictness of the voice detector. |
| `vision/live_detector.py` | `YOLO_WEIGHTS`, `CONF`, `IMGSZ`, `IGNORE_LABELS` | Model, confidence, detection size, and labels to ignore (`person` by default). |
| `main.py` | `CAMERA_INDEX`, `DETECT_FPS` | Which camera, and how often a frame is given to YOLO. |
| `chat/prompts2.py` | `GREETINGS`, `VOICE_RULES`, `LANGUAGE_RULES` | How she greets you and how she talks. |

## Troubleshooting

The terminal prints a tagged line for almost every decision, so read it first.

| What you see | Meaning and fix |
|---|---|
| Replies print but you hear nothing | The speech engine went silent. ARIA detects this, prints `[tts] ... did not really speak`, restarts the engine and retries. If it says `still silent after a restart`, check the Windows output device and volume. |
| Status never leaves `LISTENING` and the mic bar never crosses the red tick | Mic level too low. Set `MIC_THRESHOLD` lower, and check the `[mic] input device:` line. |
| `[mic] sound reached X but the speech threshold is Y` | Your voice is just under the threshold. Set `MIC_THRESHOLD` to the suggested value. |
| `(ignored, no ARIA) ...` on screen, or `[wake] ignored` | She did not hear her name. Say "ARIA, ..." first, or add the spelling Whisper produced to `WAKE_WORDS`. |
| `[stt] dropped low-confidence` or `dropped wrong-language` | Speech-to-text distrusted the result and threw it away. This is the noise filter working. |
| `[echo] ignored` | She heard her own voice and ignored it. Move the mic away from the speaker. |
| `[mic] WARNING: audio was dropped` | The CPU is overloaded. Lower `DETECT_FPS` or use smaller YOLO weights. |
| `[tts] No Hindi voice installed` | Install a Hindi voice (Pi: `espeak-ng`; Windows: a Hindi speech voice), or keep `LANGUAGE = "en"`. |
| Voice comes out of the wrong speaker | She uses the system's default output. Change the default output device, then restart ARIA. |

## Hardware notes

- **Speaker next to the microphone.** ARIA already ignores the mic while she speaks, and filters echo by comparing what she heard with what she just said. For the best result, separate the mic from the speaker physically, or use a USB mic array with built-in echo cancellation and play her voice through it.
- **Bluetooth speakers** work as the output only if they are the system default, and they add delay, so raise `ECHO_TAIL`. They cannot be used with a hardware echo-cancelling array.

## Limitations

- She needs an internet connection: speech-to-text and the language model are cloud APIs.
- She cannot be interrupted while speaking.
- Anything said while she is thinking or speaking is dropped.
- `yolo11s.pt` only knows the 80 everyday COCO objects (bottle, phone, scissors and so on). It does not know lab tools until you train custom weights.
- Offline Hindi voices sound robotic.
- Whisper can mishear Hindi-English mixed sentences.

## Roadmap

- Custom YOLO weights trained on the lab's mechanical and robotics equipment.
- RAG: answers grounded in the lab's own notes (`rag/` is still empty).
- Knowing which lab she is in (ask the teacher, or read a printed marker).
- Surveillance rules and an event log.
- Web dashboard and Raspberry Pi packaging.
- Higher-quality Hindi and Hinglish speech.