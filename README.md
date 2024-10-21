# Video Audio Replacement with AI

This project is a Proof of Concept (PoC) that demonstrates how to replace the audio in a video file with AI-generated voice. The process involves transcribing the original audio, correcting the transcription using GPT-4o, and generating new audio using Google's Text-to-Speech API.

## Features

- Upload a video file with improper audio.
- Transcribe the audio using Google's Speech-to-Text API.
- Correct the transcription using OpenAI's GPT-4o model.
- Generate new audio using Google's Text-to-Speech API (Journey voice model).
- Replace the original audio in the video with the newly generated audio.

## Requirements

- Python 3.7+
- Streamlit
- Google Cloud SDK
- OpenAI API key
- MoviePy

## Setup

1. **Clone the repository**:
   ```sh git clone https://github.com/yourusername/video-audio-replacement.git
   cd video-audio-replacement
   ```
2. **Create a virtual environment**
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. **Install dependencies**
   `pip install -r requirements.txt`

4. **Setup Encironment Variables**
   Create a `.env` file in the root directory and add your OpenAI API Key:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Setup Google Cloud Credentials**
   Download your Google cloud credentials JSON file and save it as `g_credits.json` in the root directory.

## USAGE

1. **Run the Streamlit app**:

   ```
   stremlit run t1.py
   ```

2. **Upload a Video**:

   - use the file uploader in the Sttreamlit app to upload a video file.

3. **Process the vodeo**:

   - The app will transcribe the audio, correct the transcription, generate new audio, and repace the original audio in the video.

4. **Download the processed video**:
   - The app will display the processed video which youcan download.

## FILE STRUCTURE

video-audio-replacement/
│
├── .gitignore
├── .env
├── g_creds.json
├── requirements.txt
├── t1.py
└── README.md

### Notes

- Replace `yourusername` with your actual GitHub username.
- Ensure you have the necessary API keys and credentials set up as described in the setup section.
