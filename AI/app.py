import re
import firebase_admin
from firebase_admin import credentials, db
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from text_processing import get_text_chunks
from vectorization import get_vectorstore
from chatbot import get_conversation_chain

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

cred_file = "creds.json"
database_url = "https://web-extension-73948-default-rtdb.asia-southeast1.firebasedatabase.app/"
cred = credentials.Certificate(cred_file)
firebase_admin.initialize_app(cred, {"databaseURL": database_url})

app = Flask(__name__)

text = ""

def is_youtube_link(url):
    if not isinstance(url, str):
        return False
    youtube_regex = re.compile(r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+", re.IGNORECASE)
    return bool(youtube_regex.match(url))

def transcribe_youtube_link(youtube_url):
    video_id = youtube_url.split('v=')[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_only = [entry['text'] for entry in transcript]
        full_text = ' '.join(text_only)
        return full_text
    except Exception as e:
        return f"An error occurred: {e}"

def get_nested_content(data, parent_key, child_key):
    if parent_key in data and child_key in data[parent_key]:
        return data[parent_key][child_key]
    return None

def extract_value_from_result(result):
    if isinstance(result, dict):
        first_key = next(iter(result))
        return result[first_key]
    return result

def fetch_firebase_data():
    ref = db.reference("/")
    data = ref.get()
    available_content = []
    if data:
        for parent_key in data.keys():
            for child_key in data[parent_key].keys():
                available_content.append(f"{parent_key}/{child_key}")
    return available_content

# Ensure `text` is set before `get_text_chunks`
def update_text_and_vectorstore(new_text):
    global text
    text = new_text
    text_chunks = get_text_chunks(text)
    
    if text_chunks:  # Ensure that text_chunks is not empty
        global vectorstore
        vectorstore = get_vectorstore(text_chunks)
    else:
        raise ValueError("Text chunks are empty. Cannot create vectorstore.")

text_chunks = []  # Initialize as empty
vectorstore = None

@app.route('/')
def landing_page():
    available_content = fetch_firebase_data()
    return render_template('landing.html', content_list=available_content)

@app.route('/process_content', methods=['POST'])
def process_content():
    selected_content = request.form['content']
    parent_key, child_key = selected_content.split("/")

    ref = db.reference("/")
    data = ref.get()

    if data:
        result = get_nested_content(data, parent_key, child_key)
        if result:
            result = extract_value_from_result(result)
            print(f"Retrieved content: {result}")  # Log the retrieved content
            global text
            if is_youtube_link(result.strip('"')):
                transcript_text = transcribe_youtube_link(result.strip('"'))
                update_text_and_vectorstore(transcript_text)
                return redirect(url_for('chat'))
            else:
                update_text_and_vectorstore(result)
                return redirect(url_for('chat'))
    return jsonify({'status': 'error', 'message': 'Content not found in Firebase.'})

@app.route('/chat', methods=['GET'])
def chat():
    global conversation_chain
    # Ensure that the conversation_chain is initialized with the latest vectorstore
    conversation_chain = get_conversation_chain(vectorstore)
    return render_template('index.html', chatbot_name="John")

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    global text, conversation_chain
    
    # Get the response from the conversation chain
    response = conversation_chain({"question": user_message, "chat_history": text})
    
    bot_response = response.get("answer")
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True,port=6000)
