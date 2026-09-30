"""Speech-to-text with Whisper exported from Qualcomm AI Hub."""
import numpy as np

SAMPLE_RATE = 16000
CHUNK_SECONDS = 10


class Transcriber:
    def __init__(self):
        # qai_hub_models provides a ready Whisper app wrapper (encoder + decoder).
        from qai_hub_models.models.whisper_base import App, Model
        self.app = App(Model.from_pretrained())

    def transcribe(self, audio: np.ndarray) -> str:
        """audio: float32 mono at 16 kHz."""
        return self.app.transcribe(audio, SAMPLE_RATE).strip()

    def stream(self, record_seconds: int = 60):
        """Yield captions from the microphone in rolling chunks."""
        import sounddevice as sd
        for _ in range(max(1, record_seconds // CHUNK_SECONDS)):
            chunk = sd.rec(CHUNK_SECONDS * SAMPLE_RATE, samplerate=SAMPLE_RATE,
                           channels=1, dtype="float32")
            sd.wait()
            yield self.transcribe(chunk[:, 0])
