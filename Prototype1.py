import speech_recognition as sr
from twilio.rest import Client
import geocoder
import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageFilter
import pygame
def send_sms(message, location):
    # Replace these variables with your Twilio credentials
    account_sid = 'AC8c2ddad14187e6980eb97fe826f4053a'
    auth_token = 'eb4cb7796da51bbac3d6d19f6ea73efc'
    twilio_phone_number = '+14139923498'
    recipient_phone_number = ['+2348167924294']

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the SMS message
    message = client.messages.create(
        body=f"{message}\nLocation: {location}",
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print(f"SMS sent with SID: {message.sid}")

def get_location():
    g = geocoder.ip('me')
    return g.latlng

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            # Check for specific words
            if "stop" in text:
                location = get_location()
                send_sms("Alert: The app detected the word 'STOP'.", location)
                play_sound("Secur/ding.wav")  # Replace with the path to your sound file
            else:
                print("No negative word detected")
        except sr.UnknownValueError:
            print("Could not understand audio")
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
def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

# Create the Tkinter window
app = tk.Tk()
app.title("Voice Guardian")

# Load microphone image
mic_image = Image.open("Secur/microphone.png")  # Replace with the path to your microphone image
mic_image = mic_image.resize((50, 50), Image.Resampling.NEAREST)
mic_photo = ImageTk.PhotoImage(mic_image)

# Create the button with microphone image
button = tk.Button(app, image=mic_photo, command=on_button_click, bd=0, relief=tk.FLAT)
button.photo = mic_photo  # Reference to prevent image from being garbage collected
button.pack(pady=20)

# Start the Tkinter event loop
app.mainloop()
