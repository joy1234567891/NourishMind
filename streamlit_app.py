import streamlit as st
import ollama
import audio
import asyncio

# Constants
AUDIO_LENGTH = 120  # seconds

# Initialize session state
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Streamlit UI
st.title("Nourish Mind")

# Start recording when button is clicked
if not st.session_state.recording:
    if st.button("Start"):
        st.session_state.recording = True
        st.write("Recording... Please wait.")
        with st.spinner("Transcribing audio..."):
            st.session_state.user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)
        st.session_state.recording = False
        st.write("Recording finished.")

# Stop recording when button is clicked
if st.session_state.recording:
    if st.button("Stop"):
        st.session_state.recording = False
        st.write("Recording stopped.")
        with st.spinner("Transcribing audio..."):
            st.session_state.user_input = audio.transcribe_audio_from_microphone(AUDIO_LENGTH)
        st.write("Recording finished.")

# Send transcribed audio to Ollama
if st.session_state.user_input:
    if st.button("Send"):
        user_input = st.session_state.user_input
        st.write("User input:", user_input)

        # Async function to handle Ollama request
        async def get_ollama_response(user_input):
            response = await ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}])
            return response['message']['content']

        # Call the async function using asyncio.run()
        response = asyncio.run(get_ollama_response(user_input))

        # Display the response from Ollama
        st.write("Ollama's Response:")
        st.write(response)
    else:
        st.warning("Please enter a message before sending.")
