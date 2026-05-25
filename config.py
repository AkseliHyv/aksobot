OLLAMA_MODEL = "phi3:mini"
WHISPER_MODEL = "base"
VOICE_TYPE = "en-IE-EmilyNeural"

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.08        # Quietest value that is recognized
SILENCE_DURATION = 2            # Allowed silence before cutting off recording
MAX_DURATION = 30               # max duration of recorded audio
SPEECH_CONFIRM_DURATION = 0.3   # seconds of consecutive loud audio to confirm speech
MIN_SPEECH_DURATION = 3         # minimum seconds of audio to send to Whisper