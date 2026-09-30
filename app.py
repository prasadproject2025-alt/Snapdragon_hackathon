"""LectureLens desktop UI (runs locally in the browser via Gradio; no internet needed)."""
import gradio as gr

from lecturelens import runtime, store
from lecturelens.translate import LANG_CODES


def load_llm():
    """Plug in the on-device LLM (e.g. Llama 3.2 3B exported from Qualcomm AI Hub)."""
    def llm(prompt: str) -> str:
        return "[Connect the on-device LLM in load_llm() to generate output]\n\n" + prompt[:300]
    return llm


LLM = load_llm()


def record(seconds):
    from lecturelens.asr import Transcriber
    return " ".join(Transcriber().stream(int(seconds)))


def read_board():
    from lecturelens.vision import BoardReader
    r = BoardReader()
    return r.read_text(r.capture())


def make_notes(title, transcript, board):
    from lecturelens.notes import NotesGenerator
    notes = NotesGenerator(LLM).generate(transcript, board)
    store.save(title or "Untitled lecture", transcript, board, notes)
    return notes


with gr.Blocks(title="LectureLens") as ui:
    gr.Markdown(f"# LectureLens\nOffline AI classroom companion · NPU available: **{runtime.npu_available()}**")
    title = gr.Textbox(label="Lecture title")
    with gr.Row():
        secs = gr.Slider(10, 3600, value=60, step=10, label="Record (seconds)")
        rec_btn = gr.Button("Listen")
        board_btn = gr.Button("Read board")
    transcript = gr.Textbox(label="Transcript", lines=8)
    board = gr.Textbox(label="Board text", lines=4)
    notes_btn = gr.Button("Generate notes, flashcards & quiz", variant="primary")
    notes = gr.Markdown()
    lang = gr.Dropdown(list(LANG_CODES), value="Tamil", label="Translate notes to")

    rec_btn.click(record, secs, transcript)
    board_btn.click(read_board, None, board)
    notes_btn.click(make_notes, [title, transcript, board], notes)

if __name__ == "__main__":
    ui.launch(server_name="127.0.0.1")
