import openai
import numpy as np
import sounddevice as sd
import soundfile as sf
import pyttsx3
import tempfile
import requests
import speech_recognition as sr
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()


promotions = f"Special Promotion: \"Savory Nights\"\nJoin us for dinner from Monday to Thursday and enjoy a 20% discount on your total bill when you mention the promo code SAVORY20."


industry = " Restaurant"


guidelines =  "     "
CompanyInfo = {
    "What is the restaurant's name?": "The restaurant is called The Savory Bistro.",
    "Where is the restaurant located?": "We are located at 456 Pleasant Avenue, Townsville, NY 54321.",
    "What type of cuisine do you offer?": "The Savory Bistro offers a delightful mix of Mediterranean and Pan-Asian cuisines.",
    "What are your opening hours?": "We are open from 11:30 AM to 10:00 PM, Monday to Sunday.",
    "How can I make a reservation?": "To make a reservation, you can call us at +1 (555) 123-4567 or visit our website at www.savorybistro.com/reservations.",
    "What is the maximum group size for reservations?": "We can accommodate groups of up to 6 people for reservations.",
    "Do you take walk-in customers?": "Yes, we do take walk-in customers, but availability may vary based on the day and time.",
    "Can I see the menu?": "Certainly! You can view our menu on our website at www.savorybistro.com/menu.",
    "What are today's specials?": "Our specials change daily, so please call us or visit our website for the latest updates on today's specials.",
    "Does the restaurant cater to dietary restrictions or allergies?": "Yes, we can accommodate dietary restrictions and allergies. Please inform us in advance, and our chef will be happy to assist you with suitable options.",
    "Can I host a private event or party at the restaurant?": "Absolutely! We offer private event hosting. Please contact us at +1 (555) 123-4567 or email us at info@savorybistro.com for more details and reservations.",
    "I dined at your restaurant last week and had a fantastic experience. How can I leave a review?": "We're delighted to hear that you had a wonderful time! You can leave a review on our website or on popular review platforms like Yelp or Google Maps.",
    "I had a question about my recent visit. Is there a manager I can speak to?": "Of course! I'll connect you with one of our managers. Please hold for a moment.",
    "What is the phone number of the restaurant?": "You can reach us at +1 (555) 123-4567.",
    "Does the restaurant have an email address?": "Yes, you can contact us via email at info@savorybistro.com.",
    "Thank you for your help!": "You're welcome! If you have any more questions, feel free to ask. Have a great day!",
}




def format_company_info(info_dict):
    return '\n'.join([f"{key}: {value}" for key, value in info_dict.items()])


formatted_company_info = format_company_info(CompanyInfo)




class Conversation:
    def __init__(self):
        self.history = []


    def add_message(self, message):
        self.history.append(message)


    def get_history(self):
        return ' '.join(self.history)


def transcribe_audio_to_text(file_name):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        print("API unavailable or unresponsive.")
        speak_text("I'm having trouble connecting to the speech recognition service.")
        return None
    except sr.UnknownValueError:
        print("Unable to recognize speech.")
        speak_text("I'm sorry, I couldn't understand that.")
        return None


def generate_response(conversation, prompt):
   
    prompt = prompt.lower()
    if "restaurant's name" in prompt or "name of the restaurant" in prompt:
        return "The Savory Bistro"
    elif "opening hours" in prompt or "when do you open" in prompt:
        return "We are open from 11:30 AM to 10:00 PM, Monday to Sunday."
    elif "type of cuisine" in prompt or "what kind of food" in prompt:
        return "The Savory Bistro offers a delightful mix of Mediterranean and Pan-Asian cuisines."
    elif "restaurant located" in prompt or "where is the restaurant" in prompt:
        return "The restaurant is located at 456 Pleasant Avenue, Townsville, NY 54321."
    elif "make a reservation" in prompt or "book a table" in prompt:
        return "To make a reservation, you can call us at +1 (555) 123-4567 or visit our website at www.savorybistro.com/reservations."
    elif "maximum group size" in prompt or "how many people" in prompt:
        return "We can accommodate groups of up to 6 people for reservations."
    elif "walk-in customers" in prompt or "do you accept walk-ins" in prompt:
        return "Yes, we do take walk-in customers, but availability may vary based on the day and time."
    elif "see the menu" in prompt or "what's on the menu" in prompt:
        return "Certainly! You can view our menu on our website at www.savorybistro.com/menu."
    elif "today's specials" in prompt or "what are the specials" in prompt:
        return "Our specials change daily, so please call us or visit our website for the latest updates on today's specials."
    elif "dietary restrictions" in prompt or "allergies" in prompt:
        return "Yes, we can accommodate dietary restrictions and allergies. Please inform us in advance, and our chef will be happy to assist you with suitable options."
    elif "host a private event" in prompt or "party at the restaurant" in prompt:
        return "Absolutely! We offer private event hosting. Please contact us at +1 (555) 123-4567 or email us at info@savorybistro.com for more details and reservations."
    elif "phone number" in prompt or "can i call" in prompt:
        return "You can reach us at +1 (555) 123-4567."
    elif "email address" in prompt or "can i email" in prompt:
        return "Yes, you can contact us via email at info@savorybistro.com."
    elif "thank you" in prompt or "thanks" in prompt:
        return "You're welcome! If you have any more questions, feel free to ask. Have a great day!"
    else:
        # If we cannot answer the question directly, let's use GPT-3
        conversation_history = conversation.get_history()
        gpt3_prompt = conversation_history + ' ' + prompt
        response = OpenAI.Completion.create(
            engine="text-davinci-003",
            prompt=f"""Instructions: As a industry receptionist professional,industry:\n{industry}\n you are responsible for composing a comprehensive reply to the query using the guidelines provided.
                        - Communicate clearly and professionally.
                        - Analyze issues and offer appropriate solutions.
                        - Display empathy and patience.
                        - Maintain a positive attitude.
                        - Ensure accuracy in all aspects of your answers.
                        - Adapt to different customers and scenarios.
                        - Provide information on Company information\n\n Company information:\n{formatted_company_info}
                        - Inform customers about current promotions.\n\n promotions:\n{promotions}
                        - Comply with organizational and legal guidelines.\n\n legal guidelines:\n{guidelines}
                        - Respond promptly and accurately, showing compassion and maintaining consistency with company guidelines.
                         Query: {gpt3_prompt}
                        Answer: Respond to the customer's query by following the guidelines above.""",
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].text.strip()






def speak_text(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_for_input(recognizer, source):
    print("Waiting for your command...")
    audio = recognizer.listen(source)
    try:
        transcription = recognizer.recognize_google(audio)
        print(f"Transcription: {transcription}")
        return transcription
    except sr.UnknownValueError:
        pass


def main():
    conversation = Conversation()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak_text("Welcome to The Savory Bistro. How can I assist you today?")
        while True:
            user_input = listen_for_input(recognizer, source)
            if user_input:
                print(f"You: {user_input}")
                conversation.add_message(user_input)
                response = generate_response(conversation, user_input)
                speak_text(response)
                conversation.add_message(response)


if __name__ == "__main__":
    main()

