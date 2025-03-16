import streamlit as st
import ollama
import audio
import asyncio

# python -m streamlit run streamlit_app.py

AUDIO_LENGTH = 120  # seconds

# Initialize session state
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Streamlit UI
st.title("Nourish Mind")

# Add a "Start" button to start recording
if not st.session_state.recording:
    if st.button("Start"):
        st.session_state.recording = True
        st.write("Recording... Please wait.")
        st.session_state.user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)
        st.session_state.recording = False
        st.write("Recording finished.")

# Add a "Stop" button to stop recording
if st.session_state.recording:
    if st.button("Stop"):
        st.session_state.recording = False
        st.write("Recording stopped.")
        st.session_state.user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)
        st.write("Recording finished.")

# Add a "Send" button to send the transcribed audio
if st.session_state.user_input:
    if st.button("Send"):
        user_input = st.session_state.user_input
        print("User input:", user_input)
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