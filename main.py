import config as conf
import sounddevice as sd
import soundfile as sf
import edge_tts
import asyncio
import ollama
import json
import io
import numpy as np
import tempfile
import os
from faster_whisper import WhisperModel

# Setup whisper
print("Setting up whisper")
whisper_model = WhisperModel(conf.WHISPER_MODEL, device="cpu", compute_type="int8")

# Get base prompt, and initialize conversation history
with open("prompt.json", "r", encoding="utf-8") as f:
    base_messages = json.load(f)
conversation_history = []

# TTS audio function
async def speak(text, voice=conf.VOICE_TYPE):
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    data, samplerate = sf.read(io.BytesIO(audio_bytes))
    sd.play(data, samplerate)
    sd.wait()

# User microphone audio function
def record_audio():
    chunk_size = int(conf.SAMPLE_RATE * 0.1)
    max_silence_chunks = int(conf.SILENCE_DURATION / 0.1)
    max_speech_chunks = int(conf.MAX_DURATION / 0.1)

    # How many consecutive loud chunks needed to confirm real speech
    speech_confirm_chunks = int(conf.SPEECH_CONFIRM_DURATION / 0.1)

    print("Listening...")

    with sd.InputStream(samplerate=conf.SAMPLE_RATE, channels=1, dtype='float32') as stream:
        while True:
            # Accumulate a small rolling buffer so we don't lose audio
            pre_buffer = []
            consecutive_loud = 0

            while True:
                chunk, _ = stream.read(chunk_size)
                rms = np.sqrt(np.mean(chunk**2))
                pre_buffer.append(chunk.copy())

                # Only keep the last N chunks in the pre-buffer
                # so we don't accumulate forever
                if len(pre_buffer) > speech_confirm_chunks + 5:
                    pre_buffer.pop(0)

                if rms > conf.SILENCE_THRESHOLD:
                    consecutive_loud += 1
                    if consecutive_loud >= speech_confirm_chunks:
                        print("Speech confirmed")
                        break
                else:
                    consecutive_loud = 0

            audio_chunks = list(pre_buffer)  # include pre-buffer so no words are clipped
            silence_count = 0
            speech_chunks = 0

            while speech_chunks < max_speech_chunks:
                chunk, _ = stream.read(chunk_size)
                rms = np.sqrt(np.mean(chunk**2))
                audio_chunks.append(chunk.copy())
                speech_chunks += 1

                if rms > conf.SILENCE_THRESHOLD:
                    silence_count = 0
                else:
                    silence_count += 1
                    if silence_count >= max_silence_chunks:
                        print("Silence detected, stopping recording")
                        break
            else:
                print("Max duration reached")

            audio_np = np.concatenate(audio_chunks, axis=0).flatten()

            # If the audio is too short it's likely a fluke
            min_samples = int(conf.MIN_SPEECH_DURATION * conf.SAMPLE_RATE)
            if len(audio_np) < min_samples:
                print("Audio too short, ignoring")
                continue

            return audio_np

# Speech to text function
def transcribe(audio_np):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
    try:
        sf.write(tmp_path, audio_np, conf.SAMPLE_RATE)
        segments, _ = whisper_model.transcribe(tmp_path, language="en")
        text = " ".join(seg.text for seg in segments).strip()
    finally:
        os.remove(tmp_path)
    return text


# Main loop
while True:
    try:
        audio_np = record_audio()
        text = transcribe(audio_np)

        if not text:
            print("No speech detected, listening again...")
            continue

        print("You:", text)
        conversation_history.append({'role': 'user', 'content': text})

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        messages = base_messages + conversation_history
        response = ollama.chat(model=conf.OLLAMA_MODEL, messages=messages)
        reply = response['message']['content']

        if not reply:
            print("Empty response from LLM, listening again...")
            continue

        conversation_history.append({'role': 'assistant', 'content': reply})
        print("LLM:", reply)
        asyncio.run(speak(reply))

    except KeyboardInterrupt:
        print("Program terminated by user")
        break
    except Exception as e:
        print(f"Error: {e}")