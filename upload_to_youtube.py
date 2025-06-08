
import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = Credentials(
    None,
    refresh_token=os.getenv("YT_REFRESH_TOKEN"),
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.getenv("YT_CLIENT_ID"),
    client_secret=os.getenv("YT_CLIENT_SECRET")
)

creds.refresh(google.auth.transport.requests.Request())
youtube = build("youtube", "v3", credentials=creds)

request_body = {
    "snippet": {
        "title": "German Word of the Day",
        "description": "Learn a new German word every day!",
        "tags": ["Learn German", "German word of the day"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "public",
        "madeForKids": False
    }
}

media_file = MediaFileUpload("output.mp4")
response = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
).execute()

print("Uploaded video ID:", response.get("id"))
