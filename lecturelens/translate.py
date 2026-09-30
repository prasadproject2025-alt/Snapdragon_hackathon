"""Translate notes into Indian languages (IndicTrans2)."""

LANG_CODES = {"Tamil": "tam_Taml", "Hindi": "hin_Deva", "Telugu": "tel_Telu",
              "Kannada": "kan_Knda", "Malayalam": "mal_Mlym"}


class Translator:
    def __init__(self, model):
        """model: callable (text, target_code) -> translated text."""
        self.model = model

    def translate(self, text: str, language: str) -> str:
        code = LANG_CODES[language]
        return "\n".join(self.model(p, code) if p.strip() else "" for p in text.split("\n"))
