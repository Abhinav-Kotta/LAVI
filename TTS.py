
from pathlib import Path
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization='org-05eljs5kP30eUXQdYzFyBj0S')

print(client)

speech_file_path = Path(__file__).parent / "speech_2.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input="The Savory Bistro offers a delightful mix of Mediterranean and Pan-Asian cuisines."
)

response.stream_to_file(speech_file_path)
