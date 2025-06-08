import os
import tempfile
from moviepy.editor import TextClip, AudioFileClip
from moviepy.config import change_settings
from elevenlabs import ElevenLabs

# Force Pillow for text rendering (bypass ImageMagick)
change_settings({"IMAGEMAGICK_BINARY": None})

# Narration text (replace with your actual text source)
narration_text = "Hello, welcome to today's word of the day!"

# Debug: Print environment and narration_text
print(f"narration_text: {narration_text}")
print(f"COMMUNITY_LANGUAGE: {os.getenv('COMMUNITY_LANGUAGE', 'en')}")
print(f"ELEVEN_API_KEY: {'set' if os.getenv('ELEVEN_API_KEY') else 'not set'}")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))
if not os.getenv('ELEVEN_API_KEY'):
    raise ValueError("ELEVEN_API_KEY is required")

# Generate narration audio using ElevenLabs
audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
audio = client.generate(
    text=narration_text,
    voice="Rachel",  # Adjust voice as needed (e.g., "Adam", "Bella")
    model="eleven_monolingual_v1"
)
with open(audio_file, "wb") as f:
    f.write(audio)

# Create text clip using Pillow (method='label')
text_clip = TextClip(
    narration_text,
    fontsize=40,
    color='white',
    bg_color='black',
    size=(720, 1280),
    method='label'  # Use Pillow instead of ImageMagick
)

# Load audio and set clip duration
audio_clip = AudioFileClip(audio_file)
duration = audio_clip.duration
text_clip = text_clip.set_duration(duration).set_audio(audio_clip)

# Save the final video
output_path = "output_video.mp4"
text_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

# Clean up temporary audio file
os.remove(audio_file)

print(f"Video generated successfully: {output_path}")
