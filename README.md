# Robot Companion

A voice-interactive robot companion built in Python. Listens through a microphone, understands what you say, and talks back.

## Current Features

- Microphone input via PyAudio
- Speech-to-text via SpeechRecognition
- Text-to-speech responses via pyttsx3

## Planned

- Local LLM for conversation and responses
- OLED eyes
- Mobility with wheels and legs
- Runs on Raspberry Pi

## Setup

```bash
git clone <repo-url>
cd <project-folder>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source venv/bin/activate
python main.py
```