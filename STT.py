from openai import OpenAI
import os
from audio import record

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization='org-05eljs5kP30eUXQdYzFyBj0S')

try:
    print("Recording...")
    record(5, "audio_2.wav")  # Record for 5 seconds and save as audio.wav
    print("WAV file saved.")
except Exception as e:
    print(e)

with open("audio_2.wav", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

print(transcript)
