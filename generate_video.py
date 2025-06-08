
import os
import csv
import datetime
from moviepy.editor import *
from gtts import gTTS

LANGUAGE = os.getenv("COMMUNITY_LANGUAGE", "en")
file = f"data/german_words_{LANGUAGE}.csv"

with open(file, newline='', encoding='utf-8') as f:
    words = list(csv.DictReader(f))

today = datetime.date.today()
index = (today - datetime.date(2024, 1, 1)).days % len(words)
word = words[index]

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

tts = gTTS(narration_text, lang='fr' if LANGUAGE == 'fr' else 'en')
tts.save("voice.mp3")

audio_clip = AudioFileClip("voice.mp3")
text_clip = TextClip(narration_text, fontsize=40, color='white', bg_color='black', size=(720, 1280), method='caption')
text_clip = text_clip.set_duration(audio_clip.duration).set_position('center')

final = CompositeVideoClip([text_clip.set_audio(audio_clip)])
final.write_videofile("output.mp4", fps=24)
