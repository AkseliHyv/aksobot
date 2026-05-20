import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)

    except sr.RequestError as e:
        print("Could not request results;", e)

    except sr.UnknownValueError:
        print("Could not understand audio")

    except KeyboardInterrupt:
        print("Program terminated by user")
        break