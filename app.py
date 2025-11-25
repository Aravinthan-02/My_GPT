import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Client
client= Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI chatbot",layout="centered", initial_sidebar_state="expanded")
st.title("🤖 My GPT")
st.markdown("""
### What’s on your mind today?
Type your message below to start chatting.
""")
# st.write("This is my first version of Chatbot similar to Chatgpt😇 Here you can ask your queries through the prompt and get your responses. This is my Version 1 and Version 2 will be released soon")

# To store messages

if "messages" not in st.session_state:
    st.session_state.messages=[]
    
# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        
# User input
prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt})
    
    # Display the prompt
    with st.chat_message("user"):
        st.write(prompt)
        
    # Assistant response
    with st.chat_message("assistant"):
        resp_container=st.empty()
        full_resp=""
        
        stream= client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_resp += chunk.choices[0].delta.content
                resp_container.write(full_resp)
                
        # Save the response
        st.session_state.messages.append(
            {"role":"assistant", "content":full_resp}
        )