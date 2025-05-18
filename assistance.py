import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb 
import os
import random
import pywhatkit as kit
import pyautogui
import smtplib
from email.message import EmailMessage

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is " + Time)
    print("The current time is ", Time)

def date():
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    speak(f"The current date is {day} {month} {year}")
    print(f"The current date is {day}/{month}/{year}")

def wishme():
    print("Welcome back sir!!")
    speak("Welcome back sir!!")
    
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good Morning Sir!!")
        print("Good Morning Sir!!")
    elif 12 <= hour < 16:
        speak("Good Afternoon Sir!!")
        print("Good Afternoon Sir!!")
    elif 16 <= hour < 24:
        speak("Good Evening Sir!!")
        print("Good Evening Sir!!")
    else:
        speak("Good Night Sir, See You Tomorrow")

    speak("shuzuka at your service sir, please tell me how may I help you.")
    print("Shuzuka at your service sir, please tell me how may I help you.")

def screenshot():
    img = pyautogui.screenshot()
    img_folder = os.path.expanduser("~\\Pictures")
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    img_path = os.path.join(img_folder, "screenshot.png")
    img.save(img_path)
    speak("I've taken a screenshot, please check it.")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in") # type: ignore
        print(query)
    except Exception as e:
        print(e)
        speak("Please say that again.")
        return "Try Again"

    return query.lower()

def send_email():
    try:
        speak("email address.")
        recipient = input("Please enter the recipient's email address: ") #type:ignore
        # takecommand().replace(" at ", "@").replace(" dot ", ".")

        speak("What is the subject?")
        subject = takecommand()

        speak("What is the message?")
        message = takecommand()

        email = EmailMessage()
        email['From'] = "adipudinagendrababu@gmail.com"  
        email['To'] = recipient
        email['Subject'] = subject
        email.set_content(message)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("adipudinagendrababu@gmail.com", "cuwj vmip kztf duno") 
            server.send_message(email)

        speak("Email has been sent successfully.")
        print("Email Sent Successfully!")

    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the email.")
def send_whatsapp_message():
    speak("Please provide the recipient's phone number without the country code.")
    phone_number = input("Enter phone number (without country code): ").strip()
    
    # Ensure country code is prefixed
    full_phone_number = f"+91{phone_number}"
    
    speak("What message should I send?")
    message = takecommand()
    
    # Set a time 1 minute ahead to avoid instant sending issues
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 1
    
    # Handle minute overflow
    if minute >= 60:
        hour = (hour + 1) % 24  # Adjust hour if needed
        minute = 0

    speak(f"Sending WhatsApp message to {full_phone_number} at {hour}:{minute}")
    
    # Send the message
    kit.sendwhatmsg(full_phone_number, message, hour, minute) # type: ignore
    
    speak("Message has been sent successfully.") 
if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "who are you" in query:
            speak("I'm Shuzuka , created by Mr.naga . I'm a desktop voice assistant.")
            print("I'm Shuzuka, created by Mr. naga. I'm a desktop voice assistant.")

        elif "how are you" in query:
            speak("I'm fine sir, What about you?")
            print("I'm fine sir, What about you?")

        elif "fine" in query or "good" in query:
            speak("Glad to hear that sir!!")
            print("Glad to hear that sir!!")

        elif "wikipedia" in query:
            try:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except:
                speak("Can't find this page sir, please ask something else.")

        elif "open youtube" in query:
            wb.open("https://www.youtube.com/") 

        elif "open google" in query:
            wb.open("https://www.google.com/") 
            
        elif "open github" in query:
            wb.open("https://github.com/")

        elif "open linkedin" in query:
            wb.open("https://in.linkedin.com/")

        elif "open stack overflow" in query:
            wb.open("https://stackoverflow.com")

        elif "open facebook" in query:
            wb.open("https://facebook.com")

        elif "open twitter" in query:
            wb.open("https://x.com/")
    
        elif "open telegram" in query:
            wb.open("https://telegram.com")

        elif "play music" in query:
            song_dir = os.path.expanduser("C:\\Users\\Public\\Music")  # Change this to your music folder
            songs = os.listdir(song_dir)
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(song_dir, song))
            else:
                speak("No music found in your folder.")

        elif "open chrome" in query:
            chromePath ="https://www.chrome.com"
            os.startfile(chromePath)

        elif "search on chrome" in query:
            try:
                speak("What should I search?")
                search = takecommand()
                wb.open(f"https://www.google.com/search?q={search}")
                print(f"Searching: {search}")

            except Exception as e:
                speak("Can't open now, please try again later.")
                print("Can't open now, please try again later.")

        elif "remember that" in query:
            speak("What should I remember?")
            data = takecommand()
            speak("You told me to remember " + data)
            print("You told me to remember: " + data)
            with open("data.txt", "w") as remember:
                remember.write(data)

        elif "do you remember anything" in query:
            try:
                with open("data.txt", "r") as remember:
                    speak("You told me to remember " + remember.read())
                    print("You told me to remember: " + remember.read())
            except FileNotFoundError:
                speak("I don't remember anything.")

        elif "screenshot" in query:
            screenshot()

        elif "send a mail" in query:
            send_email()
            
        elif "send whatsapp message" in query:
            send_whatsapp_message()

        elif "offline" in query:
            speak("Bye sir, see you soon.")
            quit()
            