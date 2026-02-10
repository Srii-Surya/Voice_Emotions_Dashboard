import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
from emotion_analyzer import analyze_audio

st.set_page_config(page_title="Voice Emotion Analyzer", layout="wide")
st.title("🎙 Voice Emotion Analysis Dashboard")

uploaded_file = st.file_uploader("Upload a WAV audio file", type=["wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.read())
        audio_path = temp_file.name

    st.audio(uploaded_file)
    timeline = analyze_audio(audio_path)
    df = pd.DataFrame(timeline)

    st.subheader("Emotion Timeline")
    st.dataframe(df)

    st.subheader("Emotion Distribution")
    st.bar_chart(df["emotion"].value_counts())
