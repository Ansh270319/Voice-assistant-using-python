import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser
import re
import schedule
import time
import os
import random
import smtplib
from email.message import EmailMessage

recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that. Can you please repeat?")
        return listen()
    except sr.RequestError:
        speak("Sorry, I'm facing some technical issues. Please try again later.")
        return None

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def open_website(query):
    query = query.replace("open", "").strip()
    url =
    f"https://{query}"
    try:
        webbrowser.open(url)
    except webbrowser.Error as e:
        speak(f"Sorry, I couldn't open the website because of error: {e}")

def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "pune",
        "appid": "64de586459821453dfe08c1c72939119",
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather is {weather_description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

def send_email(recipient, subject, body):
    try:
        message = EmailMessage()
        message["From"] = "anshtandale9804@gmail.com"
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("anshtandale9804@gmail.com", "Anannya@9804")
            server.send_message(message)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Sorry, there was an error sending the email: {e}")

def tell_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        joke = response.json()["joke"]
        speak(joke)
    else:
        speak("Sorry, I couldn't fetch a joke at the moment.")

def handle_query(query):
    if "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "weather" in query:
        get_weather()
    elif "search" in query:
        search_query = re.search("search (.+)", query).group(1)
        search_web(search_query)
    elif "reminder" in query and "at" in query:
        reminder_match = re.search("reminder (.+) at (.+)", query)
        if reminder_match:
            reminder = reminder_match.group(1)
            time = reminder_match.group(2)
            set_reminder(reminder, time)
            speak("Reminder set.")
        else:
            speak("Sorry, I couldn't understand the reminder. Please try again.")
    elif "send email" in query:
        send_email(recipient="john@example.com", subject="Subject", body="Body")
    elif "tell a joke" in query:
        tell_joke()
    elif "exit" in query:
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("Sorry, I can't help with that.")

if __name__ == "__main__":
    speak("Hi, I'm your college assistant. How can I help you?")

    while True:
        query = listen()
        if query:
            if "open" in query:
                open_website(query)
            else:
                handle_query(query)

        time.sleep(1)
