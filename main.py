import os
import sys
import constants
import openai
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
from datetime import datetime
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
uid = uuid.uuid4()
filename = f'{timestamp}_{uid}.txt'


while True:
    query = input("You: ")
    if query.lower() == 'bye':
        break

    with open(filename, 'a') as f:
        f.write('\n')  # Write a newline character
        f.write(f'customer: {query}\n')  # Write your text
    loader1 = TextLoader("data.txt")
    loader2 = TextLoader(filename)
    index = VectorstoreIndexCreator().from_loaders([loader1, loader2])

    response = index.query(query, llm=ChatOpenAI())

    with open(filename, 'a') as f:
        f.write(f'AI: {response}\n')
    print(f'AI: {response}')