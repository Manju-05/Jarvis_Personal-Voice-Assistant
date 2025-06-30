# Import required libraries
import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Add your API key
newsapikey = " "


# Function to speak text
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


# Function to get AI response from OpenAI
def aiProcess(command):
    client = OpenAI(api_key=" ")  # Add your OpenAI API key

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


# Function to process commands
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

    elif "news" in command:
        url = ""  # Add your news API URL
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
                speak("Failed to fetch news.")
        except Exception as e:
            print(f"Error fetching news: {e}")

    elif "exit" in command or "quit" in command:
        speak("Shutting down. Goodbye!")
        exit()

    else:
        output = aiProcess(c)
        speak(output)


# Main program starts here
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            # Listen for the wake word
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source,phrase_time_limit=2)

            # Convert audio to text
            command = recognizer.recognize_google(audio)
            print("Heard:", command)

            # If wake word is detected
            if command.strip().lower() == "jarvis":
                speak("Hello Sir!")

                # Listen for the actual command
                with sr.Microphone() as source:
                    print("Jarvis Active and Listening...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                process_command(command)

        # Handle unknown speech
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")

        # Handle other errors
        except Exception as e:
            print(f"An error occurred: {e}")
