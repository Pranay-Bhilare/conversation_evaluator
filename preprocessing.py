import pandas as pd
import re
import json

def clean_faucets(name:str) -> str :
    """Cleaning dataset , making it more readable
       - Removing trail whitespaces , colons
       - Converts suchCasing/SuchCasing into seperate words (e.g., "SelfEsteem" -> "Self Esteem")
       - Removing prefix numbers for example : "723. I Ching hexagram 5 resonance level" -> "I Ching hexagram 5 resonance level"
       """
    
    name = name.strip()
    name = re.sub(r'^\d+\.\s*', '', name)

    if name.endswith(':'):
        name = name[:-1].strip()

    # Mainly handling the suchCasing (camelCase) and SuchCasing(PascalCase) using regex
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    
    return name