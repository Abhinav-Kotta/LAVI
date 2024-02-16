from openai import OpenAI
import os
from audio import record
from datetime import datetime

now = datetime.now()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization='org-05eljs5kP30eUXQdYzFyBj0S')

def transcribe_audio():
    try:
        print("Recording...")
        record(5, f"{now}.wav")  # Record for 5 seconds and save as audio.wav
        print("WAV file saved.")
    except Exception as e:
        print(e)

    with open(f"{now}.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        
    return transcript