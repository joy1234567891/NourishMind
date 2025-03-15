import streamlit as st
import ollama

# Streamlit UI
st.title("Chat with Ollama")

user_input = st.text_input("Enter your message:", "")

if st.button("Send"):
    if user_input:
        # Send request to local Ollama
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_input}])

        # Display response
        st.write("Ollama's Response:")
        st.write(response['message']['content'])
    else:
        st.warning("Please enter a message before sending.")
