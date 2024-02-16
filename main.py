import os
import sys
import constants
import openai
from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")

query = sys.argv[1]
print(query)

loader = TextLoader("data.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query, llm=ChatOpenAI()))