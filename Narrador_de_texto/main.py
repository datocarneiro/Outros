import pyttsx3

speak = pyttsx3.init()

text = ("teste  123456789 ")

speak.say(text)
speak.runAndWait()
speak.stop()