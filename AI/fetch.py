import re
import firebase_admin
from firebase_admin import credentials, db
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

def is_youtube_link(url):
    if not isinstance(url, str):
        return False
    youtube_regex = re.compile(
        r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+",
        re.IGNORECASE,
    )
    return bool(youtube_regex.match(url))

def transcribe_youtube_link(youtube_url):
    video_id = youtube_url.split('v=')[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Extract only the text from the transcript
        text_only = [entry['text'] for entry in transcript]
        
        # Join the text into a single string
        full_text = ' '.join(text_only)
        return full_text
    except Exception as e:
        return f"An error occurred: {e}"

def get_nested_content(data, parent_key, child_key):
    if parent_key in data and child_key in data[parent_key]:
        return data[parent_key][child_key]
    else:
        return None

def extract_value_from_result(result):
    if isinstance(result, dict):
        first_key = next(iter(result))
        return result[first_key]
    return result

def main():
    cred_file = "creds.json"
    database_url = "https://web-extension-73948-default-rtdb.asia-southeast1.firebasedatabase.app/"
    parent_key = "youtubeLink"
    child_key = "Pat"

    cred = credentials.Certificate(cred_file)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

    ref = db.reference("/")
    data = ref.get()

    if data:
        result = get_nested_content(data, parent_key, child_key)
        if result:
            result = extract_value_from_result(result)
            print(f"Retrieved content: {result}")
            if is_youtube_link(result.strip('"')):
                print("Detected a YouTube link. Starting transcription...")
                transcript_text = transcribe_youtube_link(result.strip('"'))
                print("Transcript:")
                print(transcript_text)
            else:
                print("Result is not a YouTube link.")
                print("Result:")
                print(result)
        else:
            print(f"Content not found for child key '{child_key}' under parent key '{parent_key}'")
    else:
        print("No data found in the Firebase database.")

if __name__ == "__main__":
    main()
