# Create a Virtual Environment and activate it.
# python -m venv venv
# .\venv\Scripts\Activate.ps1
# To create a reqirements file
# pip freeze -r reqirements.txt 

import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = " " # Enter your api key 


def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
    client = OpenAI(api_key=" ") # Enter your Openai api key

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content


def process_command(c):
    command = c.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open_new_tab("https://www.youtube.com")

    elif "open twitter" in command:
        speak("Opening Twitter")
        webbrowser.open_new_tab("https://www.twitter.com")

    elif "open linkedin" in command or "open likedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open_new_tab("https://www.linkedin.com")

    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musiclibrary.music.get(song, None)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")

    elif "news".lower() in command.lower():
        url = f"https://newsdata.io/api/1/latest?apikey={newsapikey}&country=in,am,au,sg&language=en&category=education,technology,crime&timezone=Asia/Kolkata"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                articles = data.get('results', [])
                if articles:
                    speak("Here are the latest news headlines:")
                    for i, article in enumerate(articles[:5]):
                        speak(article['title'])
                else:
                    speak("No news articles found.")
            else:
                speak("Failed to fetch news. Please check the API or internet connection.")
        except Exception as e:
            print(f"Error fetching news: {e}")

    elif "exit" in command or "quit" in command:
        speak("Shutting down. Goodbye!")
        exit()

    else:
        output = aiProcess(c)
        speak(output)


# Main logic
speak("Initializing Jarvis...")

while True:
    try:
        with sr.Microphone() as source:
            print("Listening for wake word 'Jarvis'...")
            audio = recognizer.listen(source, phrase_time_limit=2)

        command = recognizer.recognize_google(audio)
        print("Heard:", command)

        if command.strip().lower() == "jarvis":
            speak("Hello Sir!")

            with sr.Microphone() as source:
                print("Jarvis Active and Listening...")
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            print("Command:", command)
            process_command(command)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except Exception as e:
        print(f"An error occurred: {e}")
