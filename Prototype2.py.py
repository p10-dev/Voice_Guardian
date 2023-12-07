import speech_recognition as sr
from twilio.rest import Client
import geocoder
import tkinter as tk

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
def on_button_click():
    recognize_speech()
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
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Call the function to start speech recognition
recognize_speech()
app = tk.Tk()
app.title("Speech Recognition App")
button = tk.Button(app, text="Start Listening", command=on_button_click)
button.pack(pady=20)

app.mainloop()
tk.