import streamlit as st
import tempfile
import moviepy.editor as mp
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from google.cloud import texttospeech
from gtts import gTTS
from moviepy.editor import *

# Set up Google Cloud Speech-to-Text and Text-to-Speech clients
speech_client = speech.SpeechClient()
text_to_speech_client = texttospeech.TextToSpeechClient()

def transcribe_audio(audio_file):
    """Transcribe audio using Google Speech-to-Text API."""
    with open(audio_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )

    response = speech_client.recognize(config=config, audio=audio)
    transcribed_text = response.results[0].alternatives[0].transcript
    return transcribed_text

def generate_voice(text):
    """Generate audio using Google Text-to-Speech API."""
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Studio-D'  # Journey voice model
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = text_to_speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open('generated_voice.mp3', 'wb') as out:
        out.write(response.audio_content)

def main():
    st.title("Video Audio Enhancement with AI")

    # Upload video file
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    if video_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        # Extract audio from the video
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile("original_audio.mp3")

        # Transcribe the audio
        transcribed_text = transcribe_audio("original_audio.mp3")

        # Display the transcribed text
        st.write("Transcribed Text:")
        st.text(transcribed_text)

        # Generate AI-enhanced text using GPT-4 (Replace with your GPT-4 implementation)
        enhanced_text = "Enhanced text using GPT-4"  # Replace with your implementation

        # Display the enhanced text
        st.write("AI-Enhanced Text:")
        st.text(enhanced_text)

        # Generate audio from the enhanced text
        generate_voice(enhanced_text)

        # Replace audio in the video
        new_audio = AudioSegment.from_mp3("generated_voice.mp3")
        audio_without_video = mp.AudioFileClip("generated_voice.mp3")
        final_audio = audio_without_video.set_duration(video.duration)
        final_audio.write_audiofile("final_audio.mp3")

        new_video = video.set_audio(final_audio)
        new_video.write_videofile("enhanced_video.mp4")

        # Display the enhanced video
        st.video("enhanced_video.mp4")

if __name__ == "__main__":
    main()
