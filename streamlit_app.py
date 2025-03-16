import streamlit as st
import ollama
import os
from io import StringIO

# Streamlit UI
st.title("Chat with Ollama")

# Check for the context.txt file
context_file = r"res\\context.txt"
if not os.path.exists(context_file):
    st.error(f"File '{context_file}' not found.")
    st.stop()

# Read the content from context.txt
try:
    with open(context_file, 'r', encoding='utf-8') as file:
        context_content = file.read()
except Exception as e:
    st.error(f"Error reading '{context_file}': {str(e)}")
    st.stop()

user_input = st.text_input("Enter your message:", "")
prompt = ('Based on user input, analyze user mood and based on the input context,'
          ' analyze this kind of mood might cause from lacking which nutrition, '
          'and select randomly one nutrition which user might lack, recommend food which contains such nutrition')

if st.button("Send"):
    if user_input:
        # Create a context with the actual content
        context = StringIO()
        context.write("Context Content:\n\n")
        context.write(context_content)
        context.write(f"\n\nUser Query:\n{user_input}\n\n")
        context.write(f"Prompt:\n{prompt}")
        
        # Send request to Ollama
        response = ollama.chat(
            model="llama3.2", 
            messages=[{"role": "user", "content": context.getvalue()}]
        )
        
        # Display response
        st.write("Ollama's Response:")
        st.write(response['message']['content'])
    else:
        st.warning("Please enter a message before sending.")