import streamlit as st
import ollama
import os
import PyPDF2
from io import StringIO


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {str(e)}"


# Streamlit UI
st.title("Chat with Ollama")

# Check for the res directory
res_dir = "res"
if not os.path.exists(res_dir):
    st.error(f"Directory '{res_dir}' not found.")
    st.stop()

# Get PDF files from the res directory
files = [f for f in os.listdir(res_dir) if f.endswith('.pdf')]
file_paths = [os.path.join(res_dir, file) for file in files]

# Extract PDF contents
st.info(f"Found {len(files)} PDF files in the 'res' directory")
pdf_contents = {}

# Add a progress bar for PDF processing
with st.spinner("Processing PDF files..."):
    for pdf_path in file_paths:
        filename = os.path.basename(pdf_path)
        pdf_contents[filename] = extract_text_from_pdf(pdf_path)

user_input = st.text_input("Enter your message:", "")
prompt = ('Based on user input, analyze user mood and recommend food '
          'based on the PDF content')

if st.button("Send"):
    if user_input:
        # Create a context with the actual PDF content
        context = StringIO()
        context.write("PDF Contents:\n\n")
        
        for filename, content in pdf_contents.items():
            # Add a summary of each PDF (first 500 chars)
            context.write(f"--- {filename} ---\n")
            context.write(f"{content[:2000]}...\n\n")
        
        context.write(f"User Query:\n{user_input}\n\n")
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
