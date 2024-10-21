import streamlit as st
from dotenv import load_dotenv
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip
import azure.cognitiveservices.speech as sr
# from speech_recognition import AudioFile 
# from speech_recognition import Recognizer as r
import openai
import requests
import json
import os
load_dotenv()

def main():
    st.title("Video Audio Replacement")
    if connection_check():
        file_trim_and_split()

def connection_check():
    azure_openai_key = os.getenv('AI_API_KEY')
    azure_openai_endpoint = os.getenv('AI_ENDPOINT')
    if azure_openai_key and azure_openai_endpoint:
        try:
            # Setting up headers for the API request
            # Define the headers needed for the API request, including the API key for authentication.
            headers = {
                "Content-Type": "application/json",  # Specifies that we are sending JSON data
                "api-key": azure_openai_key  # The API key for authentication
            }
            # Data to be sent to Azure OpenAI
            # Define the payload, which includes the message prompt and token limit.
            # **** This is where you can customize the message prompt and token limit. ****
            data = {
                "messages": [{"role": "user", "content": "Hello, Azure OpenAI!"}], 
                # The message we want the model to respond to
                # "prompt" : [
                    # "Tell me a joke."
                # ],
                "max_tokens": 50  # Limit the response length
            }
            # Making the POST request to the Azure OpenAI endpoint
            # Send the request to the Azure OpenAI endpoint using the defined headers and data.
            response = requests.post(azure_openai_endpoint, headers=headers, json=data)
            # Check if the request was successful
            # Handle the response, checking the status and displaying the result.
            if response.status_code == 200:
                result = response.json()  # Parse the JSON response
                st.success(result["choices"][0]["message"]["content"].strip())  # Display the response content from the AI
                return True           

            else:
                # Handle errors if the request was not successful
                st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")
        except Exception as e:
            # Handle any exceptions that occur during the request
            st.error(f"Failed to connect or retrieve response: {str(e)}")
    else:
        # Warn the user if key or endpoint is missing
        st.warning("Please enter all the required details.")


def file_trim_and_split():
    
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        # Load video and extract audio
        st.write(uploaded_file.name)
        with tempfile.NamedTemporaryFile(delete=False) as temp_video:
            temp_video.write(uploaded_file.read())
        video = VideoFileClip(temp_video.name)
        audio = video.audio
        # audio.write_audiofile("original_audio.mp3")
        with open(audio, 'rb')as audio_file:
            # with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            #     temp_audio.write(audio_file)
            speech_to_text(audio_file)
        # st.audio(audio)
        # speech_to_text("orignal_audio.mp3")


def speech_to_text(audio_path):
    st.write(os.getcwd())
    with open(audio_path, 'rb') as audio_file:
        audio = audio_file.read()
    # Transcribe audio using AZURE Speech-to-Text
    speech_config = sr.SpeechConfig(subscription=os.getenv('AZURE_K1'), region=os.getenv('AZURE_REGION'))
    audio_config = sr.audio.AudioConfig(filename=audio)
    
    transcribed = sr.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    transcribed.recognize_once()
    if transcribed.reason == sr.ResultReason.RecognizedSpeech: 
        st.write(f'{transcribed.text}')
    else:
        st.error(f'Error {transcribed.reason}')
    # with AudioFile(audio) as source:
        # audio = r.record(source)
    # try:
        # st.write(f'{r.recognise_google(audio)}')
    # except Exception as e:
        # st.error(f"Error : {e}")

def text_to_speech(transcription):
    pass

def final_video(final_audio, video_file):
    pass

if __name__ == "__main__":
    main()
