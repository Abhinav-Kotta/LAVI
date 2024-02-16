from openai import OpenAI
from audio import record
from pathlib import Path
from datetime import datetime
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

now = datetime.now()

def record_and_transcribe_audio():
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

def text_to_speech(text_response):
    speech_file_path = Path(__file__).parent / f"llm_{now}.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input= text_response
    )

    response.stream_to_file(speech_file_path)