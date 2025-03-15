import streamlit as st
import ollama
import audio
import asyncio

# python -m streamlit run streamlit_app.py

AUDIO_LENGTH = 120  # seconds

# Streamlit UI
st.title("Nourish Mind")

# Add a "Start" button to start recording
if st.button("Start"):
    st.write("Recording... Please wait.")
    user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)
    st.write("Recording finished.")

    if st.button("Send"):
        if user_input:
            # Ensure there's a running event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Send request to local Ollama
            response = loop.run_until_complete(ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}]))

            # Display response
            st.write("Ollama's Response:")
            st.write(response['message']['content'])
        else:
            st.warning("Please enter a message before sending.")