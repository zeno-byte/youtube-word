import os
import tempfile
from moviepy.editor import TextClip, AudioFileClip
from elevenlabs.client import ElevenLabs

# Narration text (replace with your actual text source)
narration_text = "Hello, welcome to today's word of the day!"

# Debug: Print environment and narration_text
print(f"narration_text: {narration_text}")
print(f"COMMUNITY_LANGUAGE: {os.getenv('COMMUNITY_LANGUAGE', 'en')}")
print(f"ELEVEN_API_KEY: {'set' if os.getenv('ELEVEN_API_KEY') else 'not set'}")
print(f"IMAGEMAGICK_BINARY: {os.getenv('IMAGEMAGICK_BINARY')}")
import elevenlabs
print(f"elevenlabs version: {elevenlabs.__version__}")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))
if not os.getenv('ELEVEN_API_KEY'):
    print("Error: ELEVEN_API_KEY not set")
    raise ValueError("ELEVEN_API_KEY is required")

# Generate narration audio using ElevenLabs
audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
audio_stream = client.text_to_speech.convert(
    text=narration_text,
    voice_id="r0k1Z0o0k1l0a0r0b0",  # Replace with a valid voice ID (e.g., Rachel's ID from ElevenLabs)
    model_id="eleven_monolingual_v1",
    output_format="mp3_44100_128"
)
with open(audio_file, "wb") as f:
    for chunk in audio_stream:
        if chunk:
            f.write(chunk)

# Create text clip using ImageMagick (method='caption')
text_clip = TextClip(
    narration_text,
    fontsize=40,
    color='white',
    bg_color='black',
    size=(720, 1280),
    method='caption'  # Use ImageMagick for word-wrapping
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
