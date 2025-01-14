import speech_recognition as sr 
import webbrowser #For using web browser 
import pyttsx3 #For text to speech conversion
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer() #Helps in taking speech recognition functionality
engine = pyttsx3.init() #initialize a tts engine object
newsapi = "NEWS_API"

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id) #for the female voice

def speak(text):
    engine.say(text) #queue the text you want to say
    engine.runAndWait() #it processes the queue and blocked the program until the queue is completed

# For accessing OpenAI
def aiProcess(command):
    client = OpenAI(api_key="OPENAI KEY",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-12-13&sortBy=publishedAt&apiKey={newsapi}")
        if r.status_code==200:
            data = r.json()

            #Extract the articles
            articles = data.get('articles',[])

            #Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let openAI handle the request
        output = aiProcess()
        speak(output)


   
if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    #Listen for the wake word "Sakura"
    #obtain audio from the microphone
    while True:
        r = sr.Recognizer()
        print("Recognizing....")
    #Recoginze speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Listening......")
                audio = r.listen(source, timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active......")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))    
