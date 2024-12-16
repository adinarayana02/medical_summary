import streamlit as st
import openai
from pydub import AudioSegment
import io

# Set your OpenAI API key
openai.api_key = "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"

# Function to summarize the transcript into medical sections
def medical_summary(transcript):
    prompt = f"""
    Organize the following medical transcript into the predefined sections:

    Sections:
    1. Medical Specialty
    2. CHIEF COMPLAINT
    3. Purpose of visit
    4. HISTORY and Physical
       - PAST MEDICAL HISTORY
       - PAST SURGICAL HISTORY
       - ALLERGIES History
       - Social History
       - REVIEW OF SYSTEMS
    5. PHYSICAL EXAMINATION
       - GENERAL
       - Vitals
       - ENT
       - Head
       - Neck
       - Chest
       - Heart
       - Abdomen
       - Pelvic
       - Extremities

    Transcript:
    {transcript}

    Provide a structured summary in the above format.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use gpt-3.5-turbo if GPT-4 is unavailable
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=3000  # Adjust max_tokens based on the expected size of the summary
        )
        structured_summary = response['choices'][0]['message']['content'].strip()
        return structured_summary
    except Exception as e:
        return f"An error occurred: {e}"

# Function to convert audio to text using OpenAI's Whisper or any suitable service
def transcribe_audio(audio_file):
    # Placeholder for audio transcription logic
    # Use OpenAI Whisper API or other transcription libraries here
    # For example, using OpenAI's Whisper model (assuming you've integrated it)
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1).set_frame_rate(16000)  # Convert to mono and set appropriate frame rate

    # Save the audio to a buffer for processing
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    # Here, you would normally call the transcription API or process the file
    # Example (assuming transcription API integration):
    # response = openai.Audio.transcribe(model="whisper-1", file=buffer)

    # For this example, we'll simulate it by returning a mock transcript
    return "Patient complains of chest pain, shortness of breath, and dizziness. He has a history of hypertension."

# Streamlit UI
def main():
    # Custom CSS to improve UI aesthetics
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
            }
            .title {
                font-size: 36px;
                color: #1E2A47;
                font-weight: 600;
                text-align: center;
                padding-top: 30px;
                padding-bottom: 10px;
            }
            .subheader {
                font-size: 24px;
                color: #2F4F9A;
                text-align: center;
                margin-bottom: 20px;
            }
            .card {
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 30px;
            }
            .button {
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #45a049;
            }
            .error {
                color: red;
                font-weight: bold;
                text-align: center;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and subtitle
    st.markdown('<div class="title">Medical Transcription Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Upload an audio file or enter the transcript to generate a medical summary</div>', unsafe_allow_html=True)

    # Layout: Input Area in Card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        audio_file = st.file_uploader("Upload an audio file (wav, mp3, etc.)", type=["wav", "mp3"], label_visibility="collapsed")
        transcript_text = st.text_area("Or, enter the transcript manually:", height=200)

        # Button to generate summary
        if st.button("Generate Medical Summary", key="generate", use_container_width=True):
            if audio_file:
                # Transcribe the audio file to text
                st.write("Transcribing audio...")
                transcript = transcribe_audio(audio_file)
                st.write(f"Transcript: {transcript}")

            elif transcript_text:
                # Use the provided transcript text
                transcript = transcript_text
            else:
                st.markdown('<div class="error">Please upload an audio file or enter a transcript.</div>', unsafe_allow_html=True)

            # Generate and display the medical summary
            if transcript:
                st.write("Generating Medical Summary...")
                summary = medical_summary(transcript)
                st.write("Medical Summary:")
                st.write(summary)

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
