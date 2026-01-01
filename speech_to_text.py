import threading

import sounddevice as sd

import numpy as np

from faster_whisper import WhisperModel


# Shared state for recording
recording_data = []
is_recording = False
SAMPLERATE = 16000
CHANNELS = 1

# Lock for thread-safe operations
recording_lock = threading.Lock()

# Whisper model loading (only once to save time)
# Options: tiny, base, small, medium, large-v2, large-v3
model = WhisperModel("small", device="cpu", compute_type="int8")

# Audio stream reference
audio_stream = None


# Callback function for audio recording
def audio_callback_(indata, frames, time, status):
    if status:
        print("Audio input status:", status)
    with recording_lock:
        if is_recording:
            recording_data.append(indata.copy())


def start_recording_():
    global is_recording, recording_data, audio_stream

    if is_recording:
        return False

    recording_data = []  # Reset data buffer
    is_recording = True

    # Open the audio stream
    audio_stream = sd.InputStream(
        callback=audio_callback_, channels=CHANNELS, samplerate=SAMPLERATE
    )
    audio_stream.start()

    return True


def stop_recording_():
    global is_recording, audio_stream

    if not is_recording:
        return None

    is_recording = False

    # Stop and close the audio stream
    if audio_stream:
        audio_stream.stop()
        audio_stream.close()

    audio_data = (
        np.concatenate(recording_data, axis=0).flatten()
        if recording_data
        else np.array([])
    )

    if len(audio_data) == 0:
        return None

    # faster-whisper returns segments as a generator
    segments, info = model.transcribe(
        audio_data, language="en", initial_prompt="The text is in English."
    )

    # Convert generator to list to process segments
    segments_list = list(segments)

    if not segments_list:
        return None

    # Check average log probability
    avg_logprobs = [segment.avg_logprob for segment in segments_list]
    if sum(avg_logprobs) / len(avg_logprobs) < -3:
        return None

    # Check no speech probability
    no_speech_probs = [segment.no_speech_prob for segment in segments_list]
    if sum(no_speech_probs) / len(no_speech_probs) > 0.5:
        return None

    # Convert to format compatible with original code
    result = {
        "text": " ".join([segment.text for segment in segments_list]),
        "segments": [
            {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "avg_logprob": segment.avg_logprob,
                "no_speech_prob": segment.no_speech_prob,
            }
            for segment in segments_list
        ],
        "language": info.language,
    }

    return result
