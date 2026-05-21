# Local Voice Assistant

A locally-running voice assistant that listens through your microphone, transcribes speech with Whisper, generates a response via Ollama, and reads it back using Edge TTS.

## How it works

1. The program listens for audio input and waits until it detects sustained speech above a configurable threshold
2. Once silence follows the speech, the recording stops and gets transcribed by `faster-whisper`
3. The transcript is appended to a rolling conversation history and sent to a local Ollama model
4. The model's reply is spoken aloud through `edge-tts` and played back via `sounddevice`

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally with your chosen model pulled
- A working microphone

Install Python dependencies:

```bash
pip install sounddevice soundfile edge-tts ollama faster-whisper numpy
```

On Linux you may also need:

```bash
sudo apt install libportaudio2
```

## Configuration

All tunable parameters live in `config.py`. Expected values:

| Variable | Description |
|---|---|
| `WHISPER_MODEL` | Whisper model size, e.g. `"base"` or `"small"` |
| `OLLAMA_MODEL` | Name of the Ollama model to use, e.g. `"llama3"` |
| `VOICE_TYPE` | Edge TTS voice string, e.g. `"en-US-AriaNeural"` |
| `SAMPLE_RATE` | Microphone sample rate, typically `16000` |
| `SILENCE_THRESHOLD` | RMS level below which audio is considered silence |
| `SILENCE_DURATION` | Seconds of silence before recording stops |
| `MAX_DURATION` | Maximum recording length in seconds |
| `SPEECH_CONFIRM_DURATION` | Seconds of loud audio required to confirm real speech |
| `MIN_SPEECH_DURATION` | Minimum recording length; shorter clips are discarded |

## Prompt

The assistant's base personality and instructions are loaded from `prompt.json`. The file should contain a list of messages in Ollama's chat format:

```json
[
  { "role": "system", "content": "You are a helpful assistant." }
]
```

## Running

```bash
python main.py
```

The program prints transcriptions and model replies to stdout. Press `Ctrl+C` to exit.

## Notes

- Conversation history is capped at the 20 most recent messages to keep context manageable
- Whisper runs on CPU with int8 quantization by default, which keeps memory usage low
- All processing is local; nothing is sent to external services except the TTS audio synthesis through Microsoft Edge TTS
    - This is planned to be changed in the future by utilizing a local tool such as Kotoro