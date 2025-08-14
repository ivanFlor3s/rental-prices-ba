def normalized_neighborhood_name(name: str) -> str:
    """
    Normalize neighborhood names by removing white space and replace using -.
    
    Args:
        name (str): The neighborhood name to normalize.
        
    Returns:
        str: The normalized neighborhood name.
    """
    
    # Remove extra spaces
    return '-'.join(name.split())