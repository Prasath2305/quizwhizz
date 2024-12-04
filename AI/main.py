from flask import Flask, render_template, request, jsonify
import os
from context import text
from text_processing import get_text_chunks
from vectorization import get_vectorstore
from chatbot import get_conversation_chain, chat_interface
from context import text

# Set Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

app = Flask(__name__)

# Set up the chatbot
text_chunks = get_text_chunks(text)
vectorstore = get_vectorstore(text_chunks)
conversation_chain = get_conversation_chain(vectorstore)

# Set the chatbot name variable (can be changed)
chatbot_name = "John"  # Change this variable as needed


# Main route to display the chat interface
@app.route('/')
def index():
    return render_template('index.html', chatbot_name=chatbot_name)


# Route to handle sending messages
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']

    # Process the user message using the conversation chain
    bot_response = conversation_chain.run(user_message)

    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
