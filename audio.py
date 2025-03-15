import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("medium")

# Function to record audio from the microphone
def record_audio(duration, sample_rate=16000):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished
    print("Recording finished.")
    return np.squeeze(audio)

# Function to transcribe audio using Whisper
def transcribe_audio(audio, sample_rate=16000):
    # Convert the audio to the format expected by Whisper
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
    # Perform the transcription
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    
    return result.text

# Function to be called from the Streamlit app
def transcribe_audio_from_microphone(duration):
    audio = record_audio(duration)
    transcription = transcribe_audio(audio)
    return transcription