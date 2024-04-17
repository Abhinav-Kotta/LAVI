import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Customer Service AI")

#OpenAI API
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai_api = st.secrets['OPENAI_API_KEY']
    else:
        openai_api = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai_api.startswith('sk_') and len(openai_api)==52):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['OPENAI_API_KEY'] = openai_api