import speech_recognition as sr
from twilio.rest import Client
import geocoder
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import pygame
import crypto
from dotenv import load_dotenv, find_dotenv

 

def send_sms(message, location):
    #loads the .env file
    load_dotenv(find_dotenv("creds.env")) 
    #fetches variables from the env file
    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    twilio_phone_number = os.getenv("twilio_phone_number")
    recipient_phone_number = ['+2348167924294']

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the SMS message
    message = client.messages.create(
        body=f"{message}\nLocation: {location}", from_=twilio_phone_number, to=recipient_phone_number
    )

    print(f"SMS sent")

def get_location():
    g = geocoder.ip('me')
    return g.latlng

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            # Check for specific words
            if "stop" in text:
                location = get_location()
                send_sms("DOMESTIC VIOLENCE ONGOING", location)
            else:
                text = recognizer.recognize_google(audio)
#        except sr.UnknownValueError:
#            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        # After processing, re-enable the button
        button.config(state=tk.NORMAL)

# Function for the bouncing effect
def bounce_button():
    # Move the button up and down
    for _ in range(5):
        app.update()
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        app.update_idletasks()
        app.after(100)
        button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        app.update_idletasks()
        app.after(100)

# Function to handle button click
def on_button_click():
    # Disable the button during speech recognition
    button.config(state=tk.DISABLED)
    recognize_speech()
    # Trigger the bouncing effect after speech recognition
    bounce_button()

# Function to play a sound
# i don't think this is necessary as in a rape case / life threatning situation a sound may cause the attacker to go berserk but it's still okay for demo purposes
def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

# Create the Tkinter window
app = tk.Tk()
app.title("Speech Recognition App")

# Load microphone image
# change mic image??
mic_image = Image.open("Secur/microphone.png")  # Replace with the path to your microphone image
mic_image = mic_image.resize((50, 50), Image.Resampling.NEAREST)
mic_photo = ImageTk.PhotoImage(mic_image)

# Create the button with microphone image
button = tk.Button(app, image=mic_photo, command=on_button_click, bd=0, relief=tk.FLAT)
button.photo = mic_photo  # Reference to prevent image from being garbage collected
button.pack(pady=20)

# Start the Tkinter event loop
app.mainloop()
