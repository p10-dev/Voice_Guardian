from dotenv import load_dotenv, find_dotenv
from encryptor import *
from PIL import Image, ImageTk
from recorder import *
from twilio.rest import Client
import geocoder
import os
import pygame
import speech_recognition as sr
import tkinter as tk
import time


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

# Function to play a sound
def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

# Function to recognize speech
def recognize_speech(max_listen_time=5):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        start_time = time.time()
        audio = None

        while time.time() - start_time < max_listen_time:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)

            # Check for specific words
                if "stop" in text:
                    location = get_location()
                    send_sms("DOMESTIC VIOLENCE ONGOING", location)
                    print("sent!")
                    record()
                    encrypt_and_save('securit23',output_wav_file)
                    play_sound('alarm.mp3')
                    time.sleep(5)
                    if os.path.exists(output_wav_file):
                        os.remove(output_wav_file)
                    
                else:
                    text = recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected within the specified time.")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        else:
            button.config(state=tk.NORMAL)
            
                
    if audio is None:
            print("Timeout: No speech detected within the specified time.")
        # After processing, re-enable the button
            button.config(state=tk.NORMAL)

# Function for the bouncing effect
def bounce_button(bounce_count = 5):
    # Move the button up and down
    for _ in range(bounce_count):
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
    #Trigger the bouncing effect after speech recognition
    bounce_button()
    app.destroy()
# Create the Tkinter window
app = tk.Tk()
app.title("Voice Guardian")

# Load microphone image

mic_image = Image.open("mic2.png")  # Replace with the path to your microphone image
mic_image = mic_image.resize((300, 300), Image.Resampling.NEAREST)
mic_photo = ImageTk.PhotoImage(mic_image)

# Create the button with microphone image
button = tk.Button(app, image=mic_photo, command=on_button_click, bd=0, relief=tk.FLAT)
button.photo = mic_photo  # Reference to prevent image from being garbage collected
button.pack(pady=20)

# Start the Tkinter event loop
app.mainloop()
