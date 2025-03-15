import streamlit as st
import ollama
import audio

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
            # Send request to local Ollama
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}])

            # Display response
            st.write("Ollama's Response:")
            st.write(response['message']['content'])
        else:
            st.warning("Please enter a message before sending.")