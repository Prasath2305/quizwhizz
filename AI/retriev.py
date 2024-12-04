import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase connection
cred_file = "creds.json"  # Replace with your credentials file name
database_url = "https://web-extension-73948-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Load Firebase credentials
cred = credentials.Certificate(cred_file)
firebase_admin.initialize_app(cred, {"databaseURL": database_url})

# Fetch data from Firebase
ref = db.reference("/")  # Root reference
data = ref.get()

if data:
    # Extract the first key and its nested keys
    main_key = list(data.keys())[0]  # Get the first key
    nested_keys = list(data[main_key].keys())  # Get the nested keys of the first key

    # Prepare dictionary
    result_dict = {main_key: nested_keys}

    # Print the result
    print(json.dumps(result_dict, indent=4))
else:
    print("No data found in the Firebase database.")
