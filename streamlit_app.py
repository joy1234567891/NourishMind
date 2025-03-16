import streamlit as st
import ollama
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import json

# Initialize Streamlit UI
st.title("Nourish Mind")

# Check if context.txt exists
context_file = r"res\\context.txt"
embedding_file = r"res\\context_embeddings.json"

if not os.path.exists(context_file):
    st.error(f"File '{context_file}' not found.")
    st.stop()

# Load SentenceTransformer for embedding calculations
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read context.txt and compute embeddings (if not already computed)
if not os.path.exists(embedding_file):
    with open(context_file, "r", encoding="utf-8") as file:
        context_content = file.readlines()

    # Compute embedding for each line
    context_embeddings = {line.strip(): model.encode(line.strip()).tolist() for line in context_content}

    # Save embeddings to a JSON file to avoid repeated computation
    with open(embedding_file, "w", encoding="utf-8") as f:
        json.dump(context_embeddings, f, ensure_ascii=False, indent=4)
else:
    # Load precomputed embeddings
    with open(embedding_file, "r", encoding="utf-8") as f:
        context_embeddings = json.load(f)

# User input
user_input = st.text_input("Enter your message:", "")

# Process input when the send button is clicked
if st.button("Send"):
    if user_input:
        # Compute embedding for user input
        user_embedding = model.encode(user_input)

        # Compute cosine similarity to find the most relevant context
        def cosine_similarity(vec1, vec2):
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        most_relevant_context = sorted(
            context_embeddings.items(),
            key=lambda item: cosine_similarity(user_embedding, np.array(item[1])),
            reverse=True
        )[:3]  # Select the top 3 most relevant lines

        selected_context = "\n".join([ctx[0] for ctx in most_relevant_context])

        # Generate the final prompt
        prompt = (f"Based on user input, analyze user mood and based on the input context, "
                  f"analyze which nutrition might be lacking due to this mood, "
                  f"then randomly pick one and recommend food containing this nutrition.\n\n"
                  f"Relevant Context:\n{selected_context}\n\nUser Query:\n{user_input}")

        # Send request to Ollama
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )

        # Display the response
        st.write("Nourish Mind Advise:")
        st.write(response['message']['content'])
    else:
        st.warning("Please enter a message before sending.")
