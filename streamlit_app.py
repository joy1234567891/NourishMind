import streamlit as st
import ollama
import os

# Streamlit UI
st.title("Chat with Ollama")
# List files in the res directory

res_dir = "res"
if not os.path.exists(res_dir):
    st.error(f"Directory '{res_dir}' not found.")
    st.stop()

files = os.listdir(res_dir)
file_paths = [os.path.join(res_dir, file) for file in files]
user_input = st.text_input("Enter your message:", "")
prompt = 'based on user input to analyze user mood and recommend food based on files'
if st.button("Send"):
    if user_input:
        # Combine file paths, user input, and prompt into the context
        context = f"Files in 'res' directory:\n{file_paths}\n\nUser Query:\n{user_input}\n\nPrompt:\n{prompt}"
        
        # Send request to Ollama
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": context}])
        

        # Display response
        st.write("Ollama's Response:")
        st.write(response['message']['content'])
    else:
        st.warning("Please enter a message before sending.")
