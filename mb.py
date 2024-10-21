import streamlit as st
import speech_recognition as sr
import openai
import pyttsx3
from moviepy.editor import VideoFileClip, AudioFileClip
# from dotenv import load_dotenv
import os
# load_dotenv()


# Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = '22ec84421ec24230a3638d1b51e3a7dc'

# Define Streamlit app
def main():
    st.title("Video Audio Replacement")

    # Upload video file
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Load video and extract audio
        video = VideoFileClip(uploaded_file)
        audio = video.audio

        # Transcribe audio using Google Speech-to-Text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio.filename) as source:
            audio_data = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            st.error("Google Speech-to-Text could not understand audio")
            return
        except sr.RequestError as e:
            st.error("Could not request results from Google Speech-to-Text; {0}".format(e))
            return

        # Correct transcription using GPT-4
        prompt = f"Correct the following transcription:\n{transcription}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        corrected_transcription = response.choices[0].text

        # Generate AI-generated voice using Google Text-to-Speech
        engine = pyttsx3.init()
        engine.setProperty("voice", "google_tts_journey")
        engine.say(corrected_transcription)
        engine.save_to_file("generated_audio.mp3", corrected_transcription)
        engine.runAndWait()

        # Replace original audio with AI-generated audio
        new_audio = AudioFileClip("generated_audio.mp3")
        video.audio = new_audio
        video.write_videofile("output_video.mp4")

        st.success("Video processed successfully!")
        st.download_button("Download output video", "output_video.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
