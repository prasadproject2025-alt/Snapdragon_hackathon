"""ONNX Runtime session factory that prefers the Snapdragon Hexagon NPU (QNN EP)."""
from pathlib import Path
import onnxruntime as ort

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def create_session(model_name: str) -> ort.InferenceSession:
    """Load models/<model_name>.onnx on the NPU, falling back to CPU."""
    path = MODELS_DIR / f"{model_name}.onnx"
    providers = []
    if "QNNExecutionProvider" in ort.get_available_providers():
        providers.append(("QNNExecutionProvider", {
            "backend_path": "QnnHtp.dll",          # Hexagon NPU backend
            "htp_performance_mode": "burst",
        }))
    providers.append("CPUExecutionProvider")
    return ort.InferenceSession(str(path), providers=providers)


def npu_available() -> bool:
    return "QNNExecutionProvider" in ort.get_available_providers()
