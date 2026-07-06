import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalizza una stringa per confronti:
    - minuscole
    - rimozione accenti
    - rimozione spazi iniziali/finali
    """

    if text is None:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    return text.lower().strip()