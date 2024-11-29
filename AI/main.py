import os
from context import text
from text_processing import get_text_chunks
from vectorization import get_vectorstore
from chatbot import get_conversation_chain, chat_interface
from context import text
# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

def main():
    # Step 1: Split the text into chunks
    text_chunks = get_text_chunks(text)

    # Step 2: Create a FAISS vector store
    vectorstore = get_vectorstore(text_chunks)

    # Step 3: Set up the conversation chain
    conversation_chain = get_conversation_chain(vectorstore)

    # Step 4: Start the chatbot interface
    chat_interface(conversation_chain)

if __name__ == "__main__":
    main()
