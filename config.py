OLLAMA_MODEL = "llama3.2:3b-instruct-q4_K_M"
WHISPER_MODEL = "small"
VOICE_TYPE = "en-GB-RyanNeural"

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.06        # Quietest value that is recognized
SILENCE_DURATION = 1.5          # Allowed silence before cutting off recording
MAX_DURATION = 30               # max duration of recorded audio
SPEECH_CONFIRM_DURATION = 0.3   # seconds of consecutive loud audio to confirm speech
MIN_SPEECH_DURATION = 0.5       # minimum seconds of audio to send to Whisper