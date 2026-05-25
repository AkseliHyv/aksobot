# milo-robot

Milo is a voice-based dekstop assistant and to-be-robot that listens, thinks, and talks back. Built in Python, designed to eventually live inside a physical robot running on a Raspberry Pi.

## How It Works

1. Listens via microphone using a custom voice activity detector
2. Transcribes speech locally using Faster Whisper
3. Sends text to a local LLM via Ollama
4. Responds out loud using Edge TTS with a natural sounding voice

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install and start Ollama, then pull the model:

```bash
ollama pull phi3:mini
ollama serve
```

Run:

```bash
python main.py
```

## Requirements

- Python 3.10+
- Ollama
- A microphone
- Internet connection for Edge TTS

## Roadmap

- Locally made voice instead of Edge TTS
- Raspberry Pi deployment
- OLED eyes that reflect mood
- Emotional state system that influences responses
- Persistent memory across conversations
- Physical movement with wheels and legs

## Config

Settings like model name, voice, sample rate, and silence thresholds live in `config.py`.