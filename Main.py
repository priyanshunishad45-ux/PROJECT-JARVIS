import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai

# -------------------------
# CONFIGURATION
# -------------------------
import os
newsapi = os.getenv("98d5caa33aaa3b761ed40b44925d28df")
GEMINI_API_KEY = os.getenv("AIzaSyBQ_qrMKSsndXpqNf8S_cyrVpDJpJihFjo")

genai.configure(api_key=GEMINI_API_KEY)

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------
# GEMINI CHAT FUNCTION
# -------------------------
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry boss, Gemini is not responding right now."

# -------------------------
# COMMAND PROCESSOR
# -------------------------
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Sorry boss, I don't have that song in my library.")

    elif "news" in c:
        speak("Fetching the latest news for you, boss...")
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if articles:
                    headlines = [a["title"] for a in articles[:5]]
                    for h in headlines:
                        print("📰", h)
                        speak(h)
                    
                    # Ask Gemini to summarize the headlines
                    summary = ask_gemini("Summarize these news headlines: " + ", ".join(headlines))
                    speak("Here's a quick summary:")
                    speak(summary)
                else:
                    speak("No news available right now.")
            else:
                speak("Sorry boss, I couldn't fetch the news.")
        except Exception as e:
            print(e)
            speak("Something went wrong while fetching news.")

    else:
        # If command is not predefined → use Gemini
        speak("Let me think...")
        reply = ask_gemini(c)
        print("Gemini:", reply)
        speak(reply)

# -------------------------
# MAIN PROGRAM LOOP
# -------------------------
if __name__ == "__main__":
    speak("Initializing Jarvis with Gemini AI...")
    while True:
        print("Listening for wake word 'Jarvis'...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
            
            if word.lower() == "jarvis":
                speak("Yes boss?")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

        except Exception as e:
            print("Error:", e)
