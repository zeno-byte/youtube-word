import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Debug: Check if video file exists
video_file = "output_video.mp4"
print(f"Checking for video file: {video_file}")
if not os.path.exists(video_file):
    print(f"Error: {video_file} not found")
    raise FileNotFoundError(f"{video_file} not found")

# Debug: Verify environment variables
print(f"YT_CLIENT_ID: {'set' if os.getenv('YT_CLIENT_ID') else 'not set'}")
print(f"YT_CLIENT_SECRET: {'set' if os.getenv('YT_CLIENT_SECRET') else 'not set'}")
print(f"YT_REFRESH_TOKEN: {'set' if os.getenv('YT_REFRESH_TOKEN') else 'not set'}")

# Initialize credentials
creds = Credentials(
    None,
    refresh_token=os.getenv("YT_REFRESH_TOKEN"),
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.getenv("YT_CLIENT_ID"),
    client_secret=os.getenv("YT_CLIENT_SECRET")
)

# Refresh credentials
creds.refresh(google.auth.transport.requests.Request())

# Build YouTube API client
youtube = build("youtube", "v3", credentials=creds)

# Define video metadata
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

# Upload video
media_file = MediaFileUpload(video_file)
response = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
).execute()

print(f"Video uploaded: https://www.youtube.com/watch?v={response.get('id')}")
