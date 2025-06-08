import os
import tempfile
from moviepy.editor import TextClip, AudioFileClip
from gtts import gTTS

# Narration text (replace with your actual text source)
narration_text = "Hello, welcome to today's word of the day!"

# Debug: Print environment and narration_text
print(f"narration_text: {narration_text}")
print(f"COMMUNITY_LANGUAGE: {os.getenv('COMMUNITY_LANGUAGE', 'en')}")
print(f"IMAGEMAGICK_BINARY: {os.getenv('IMAGEMAGICK_BINARY')}")
try:
    import gtts
    print(f"gTTS version: {gtts.__version__}")
except ImportError:
    print("gTTS not installed")

# Generate narration audio using gTTS
audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
tts = gTTS(text=narration_text, lang="en", slow=False)
tts.save(audio_file)

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
