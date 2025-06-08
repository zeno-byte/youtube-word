import os
import tempfile
from moviepy.editor import TextClip, AudioFileClip
from elevenlabs.client import ElevenLabs
import elevenlabs

# Narration text
narration_text = "Hello, welcome to today's word of the day!"

# Debug: Print environment and configuration
print(f"narration_text: {narration_text}")
print(f"COMMUNITY_LANGUAGE: {os.getenv('COMMUNITY_LANGUAGE', 'en')}")
print(f"ELEVEN_API_KEY: {'set' if os.getenv('ELEVEN_API_KEY') else 'not set'}")
print(f"IMAGEMAGICK_BINARY: {os.getenv('IMAGEMAGICK_BINARY', 'not set')}")
print(f"elevenlabs version: {elevenlabs.__version__}")

# Validate environment variables
if not os.getenv('ELEVEN_API_KEY'):
    raise ValueError("ELEVEN_API_KEY is required")
if not os.getenv('IMAGEMAGICK_BINARY'):
    print("Warning: IMAGEMAGICK_BINARY not set, may cause issues with TextClip")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))

# List available voices to debug (uncomment to run)
# from elevenlabs import Voices
# try:
#     voices = client.voices.get_all()
#     print("Available voices:")
#     for voice in voices:
#         print(f"Voice ID: {voice.voice_id}, Name: {voice.name}")
# except Exception as e:
#     print(f"Error fetching voices: {e}")
#     raise

# Generate narration audio
audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
try:
    audio_stream = client.text_to_speech.convert(
        text=narration_text,
        voice_id="v7QyOKVRzHDBpjhEZHqo",  # Replaced with new voice_id
        model_id="eleven_monolingual_v1",
        output_format="mp3_44100_128"
    )
    with open(audio_file, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
except Exception as e:
    print(f"Error generating audio: {e}")
    os.remove(audio_file)  # Clean up if failed
    raise

# Create text clip using ImageMagick
try:
    text_clip = TextClip(
        narration_text,
        fontsize=40,
        color='white',
        bg_color='black',
        size=(720, 1280),
        method='caption'  # Requires ImageMagick
    )
except Exception as e:
    print(f"Error creating text clip: {e}")
    os.remove(audio_file)
    raise

# Load audio and set clip duration
try:
    audio_clip = AudioFileClip(audio_file)
    duration = audio_clip.duration
    text_clip = text_clip.set_duration(duration).set_audio(audio_clip)
except Exception as e:
    print(f"Error processing audio clip: {e}")
    os.remove(audio_file)
    raise

# Save the final video
output_path = "output_video.mp4"
try:
    text_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    print(f"Video generated successfully: {output_path}")
except Exception as e:
    print(f"Error generating video: {e}")
    raise
finally:
    # Clean up temporary audio file
    if os.path.exists(audio_file):
        os.remove(audio_file)
    # Close clips to free resources
    if 'audio_clip' in locals():
        audio_clip.close()
    if 'text_clip' in locals():
        text_clip.close()
