import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from moviepy.editor import VideoFileClip, AudioFileClip
import openai
import tempfile
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./g_creds.json"

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join([result.alternatives[0].transcript for result in response.results])

def correct_transcription(transcription):
    response = openai.Completion.create(
        engine="gpt-4o",
        prompt=f"Correct the following transcription: {transcription}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

def generate_audio(text, output_path):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-J"  # Journey voice model
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)

def replace_audio_in_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(audio_path)
    video = video.set_audio(new_audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main():
    st.title("Video Audio Replacement with AI")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(temp_audio.name)
            audio_path = temp_audio.name
        
        transcription = transcribe_audio(audio_path)
        st.write("Original Transcription:", transcription)
        
        corrected_transcription = correct_transcription(transcription)
        st.write("Corrected Transcription:", corrected_transcription)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_new_audio:
            generate_audio(corrected_transcription, temp_new_audio.name)
            new_audio_path = temp_new_audio.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output_video:
            replace_audio_in_video(video_path, new_audio_path, temp_output_video.name)
            output_video_path = temp_output_video.name
        
        st.video(output_video_path)

if __name__ == "__main__":
    main()