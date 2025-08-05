def get_number(text: str) -> int:
    """
    Extrae un número de un texto dado.
    
    Args:
        text (str): El texto del cual se extraerá el número.
    
    Returns:
        int: El número extraído del texto.
    """
    import re
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0