import speech_recognition as sr
from textblob import TextBlob
import tempfile
import os
from pydub import AudioSegment


def split_audio(file_path, chunk_duration=5):
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_duration * 1000):
        chunk = audio[i:i + chunk_duration * 1000]
        chunks.append((chunk, i / 1000))

    return chunks


def analyze_audio(file_path):
    recognizer = sr.Recognizer()
    timeline = []

    chunks = split_audio(file_path)

    for chunk, start_time in chunks:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            chunk.export(temp.name, format="wav")
            temp_path = temp.name

        try:
            with sr.AudioFile(temp_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            polarity = TextBlob(text).sentiment.polarity

            if polarity > 0.2:
                emotion = "Positive"
            elif polarity < -0.2:
                emotion = "Negative"
            else:
                emotion = "Neutral"

            timeline.append({
                "time": f"{int(start_time//60)}:{int(start_time%60):02d}",
                "emotion": emotion
            })

        except sr.UnknownValueError:
            pass

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return timeline
