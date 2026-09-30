"""Generate notes, flashcards and a quiz with a small on-device LLM."""

NOTES_PROMPT = """You are a helpful study assistant. Using the lecture transcript and
board text below, write:
1. A 5-line summary
2. Structured notes with headings
3. 8 key terms with one-line definitions
4. 5 flashcards (Q/A)
5. A 5-question multiple-choice quiz with answers

TRANSCRIPT:
{transcript}

BOARD TEXT:
{board}
"""


class NotesGenerator:
    def __init__(self, llm):
        """llm: any callable prompt -> text (e.g. Llama 3.2 3B via Qualcomm AI Hub / Genie)."""
        self.llm = llm

    def generate(self, transcript: str, board: str = "") -> str:
        return self.llm(NOTES_PROMPT.format(transcript=transcript[-12000:], board=board[-3000:]))
