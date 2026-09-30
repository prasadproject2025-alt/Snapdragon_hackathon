"""Capture the whiteboard/slides from the webcam and extract text."""
import cv2


class BoardReader:
    def __init__(self, languages=("en",)):
        import easyocr
        self.reader = easyocr.Reader(list(languages), gpu=False)

    def capture(self, camera_index: int = 0):
        cam = cv2.VideoCapture(camera_index)
        ok, frame = cam.read()
        cam.release()
        if not ok:
            raise RuntimeError("Could not read from webcam")
        return frame

    def read_text(self, frame) -> str:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lines = self.reader.readtext(gray, detail=0, paragraph=True)
        return "\n".join(lines)
