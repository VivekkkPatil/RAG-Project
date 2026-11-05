import speech_recognition as sr

def listen() -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 50
    recognizer.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            try:
                # Try Google first
                text = recognizer.recognize_google(audio)
                return text
            except:
                # Fallback to Whisper
                text = recognizer.recognize_whisper(audio, model="base")
                return text
        except sr.WaitTimeoutError:
            return "Timeout - no speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech service unavailable"