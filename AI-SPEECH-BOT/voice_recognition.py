import speech_recognition as sr

r = sr.Recognizer()

mic = sr.Microphone()

with mic as source:
    print("Speak anything")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try :
    text = r.recognize_google(audio)
    print("You said",str(text))
except Exception as Error:
    print(Error)