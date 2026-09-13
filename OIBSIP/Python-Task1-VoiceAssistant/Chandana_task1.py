import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

while True:

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        if "hello" in text.lower():
            speak("Hello! How can I help you?")

        elif "time" in text.lower():
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + current_time)

        elif "date" in text.lower():
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + current_date)

        elif "open google" in text.lower():
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in text.lower():
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "youtube" in text.lower() and "search" in text.lower():
            search_query = text.lower().replace("youtube", "").replace("search", "").strip()

            if search_query:
                speak("Searching YouTube for " + search_query)
                webbrowser.open("https://www.youtube.com/results?search_query=" + search_query)
            else:
                speak("What should I search for?")

        elif "bye" in text.lower() or "exit" in text.lower():
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I don't understand.")

    except:
        speak("Sorry, I could not understand you. Please repeat.")
