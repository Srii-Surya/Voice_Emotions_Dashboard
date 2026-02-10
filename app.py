import streamlit as st
import pandas as pd
import tempfile
from pydub import AudioSegment
from emotion_analyzer import analyze_audio

st.set_page_config(page_title="Voice Emotion Analyzer", layout="wide")
st.title("🎙 Voice Emotion Analysis Dashboard")

st.write(
    "Upload an audio file (WAV or MP3). "
    "The system analyzes emotions over time and displays when emotions change."
)

uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["wav", "mp3"]
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        # Convert MP3 to WAV if needed
        if uploaded_file.type == "audio/mpeg":
            audio = AudioSegment.from_mp3(uploaded_file)
            audio.export(temp_file.name, format="wav")
        else:
            temp_file.write(uploaded_file.read())

        audio_path = temp_file.name

    st.audio(uploaded_file)

    st.subheader("🔍 Analyzing emotions...")
    timeline = analyze_audio(audio_path)

    if timeline:
        df = pd.DataFrame(timeline)

        st.subheader("📌 Emotion Timeline (Minute & Second)")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Emotion Distribution")
        st.bar_chart(df["emotion"].value_counts())

    else:
        st.warning("No speech detected in the audio.")
