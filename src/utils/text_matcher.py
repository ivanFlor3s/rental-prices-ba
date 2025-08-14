import unicodedata
from difflib import SequenceMatcher

def normalize_text(text: str) -> str:
    # Pasar a minúsculas
    text = text.lower()
    # Quitar acentos
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    )
    return text

def text_match_score(text1: str, text2: str) -> float:
    # Normalizar
    t1 = normalize_text(text1)
    t2 = normalize_text(text2)
    # Calcular similitud
    score = SequenceMatcher(None, t1, t2).ratio()
    return score
