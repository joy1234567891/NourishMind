import streamlit as st
import ollama
import audio

# python -m streamlit run streamlit_app.py

AUDIO_LENGTH = 120  # seconds

# Streamlit UI
st.title("Chat with Ollama")

# Get user input from calling transcribe_audio_from_microphone
user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)

if st.button("Send"):
    if user_input:
        # Send request to local Ollama
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}])

        # Display response
        st.write("Ollama's Response:")
        st.write(response['message']['content'])
    else:
        st.warning("Please enter a message before sending.")
