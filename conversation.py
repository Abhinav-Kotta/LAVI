import os
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
from datetime import datetime
import uuid
from openai import OpenAI
from audio import record
from pathlib import Path

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
uid = uuid.uuid4()
filename = f'{timestamp}_{uid}.txt'

def record_and_transcribe_audio():
    try:
        print("Recording...")
        record(10, f"{now}.wav")  # Record for 5 seconds and save as audio.wav
        print("WAV file saved.")
    except Exception as e:
        print(e)

    with open(f"{now}.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        
    return transcript.text

def text_to_speech(text_response):
    speech_file_path = Path(__file__).parent / f"llm_{now}.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input= text_response
    )

    response.stream_to_file(speech_file_path)

# def conversation_AI():
#     while True:
#         query = record_and_transcribe_audio()
#         if query.lower() == 'bye':
#             break

#         with open(filename, 'a') as f:
#             f.write('\n')  # Write a newline character
#             f.write(f'customer: {query}\n')  # Write your text
#         loader1 = TextLoader("data.txt")
#         loader2 = TextLoader(filename)
#         index = VectorstoreIndexCreator().from_loaders([loader1, loader2])

#         response = index.query(query, llm=ChatOpenAI())
#         text_to_speech(response)
#         with open(filename, 'a') as f:
#             f.write(f'AI: {response}\n')
#         print(f'AI: {response}')

# conversation_AI()
    
def conversation_AI(query):
    while True:
        # query = record_and_transcribe_audio()
        if query.lower() == 'bye':
            break

        with open(filename, 'a') as f:
            f.write('\n')  # Write a newline character
            f.write(f'customer: {query}\n')  # Write your text
        loader1 = TextLoader("data.txt")
        loader2 = TextLoader(filename)
        index = VectorstoreIndexCreator().from_loaders([loader1, loader2])

        response = index.query(query, llm=ChatOpenAI())
        text_to_speech(response)
        with open(filename, 'a') as f:
            f.write(f'AI: {response}\n')
        print(f'AI: {response}')