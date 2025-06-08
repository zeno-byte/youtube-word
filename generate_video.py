import os
import csv
import datetime
from moviepy.editor import *
from elevenlabs import generate, save, set_api_key

# Set your ElevenLabs API key from environment variable
set_api_key(os.getenv("ELEVEN_API_KEY"))

# Select the community language: 'en' or 'fr'
LANGUAGE = os.getenv("COMMUNITY_LANGUAGE", "en")
file = f"data/german_words_{LANGUAGE}.csv"

# Load words from CSV
with open(file, newline='', encoding='utf-8') as f:
    words = list(csv.DictReader(f))

# Calculate today's index based on date
today = datetime.date.today()
index = (today - datetime.date(2024, 1, 1)).days % len(words)
word = words[index]

# Prepare narration text depending on language
if LANGUAGE == "fr":
    narration_text = (
        f"Mot du jour: {word['word']}. Signification: {word['meaning']}. "
        f"Exemple: {word['example']}. Traduction: {word['translation']}"
    )
else:
    narration_text = (
        f"Word of the Day: {word['word']}. Meaning: {word['meaning']}. "
        f"Example: {word['example']}. Translation: {word['translation']}"
    )

# Generate audio with ElevenLabs voice "Rachel"
audio = generate(text=narration_text, voice="Rachel", model="eleven_monolingual_v1")
save(audio, "voice.mp3")

# Create video with text and audio
audio_clip = AudioFileClip("voice.mp3")
text_clip = TextClip(
    narration_text,
    fontsize=40,
    color='white',
    bg_color='black',
    size=(720, 1280),
    method='caption'
)
text_clip = text_clip.set_duration(audio_clip.duration).set_position('center')

final_video = CompositeVideoClip([text_clip.set_audio(audio_clip)])
final_video.write_videofile("output.mp4", fps=24)
