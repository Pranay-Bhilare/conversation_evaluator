import pandas as pd
import re
import json

def clean_facets(name:str) -> str :
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

# Took help of multiple AI's for fnal categorization of faucets
CATEGORY_KEYWORDS = {
    # --- Foundational & Abstract ---
    "Psychological Models & Constructs": [
        'psychological construct', 'hexaco', 'big five', 'enneagram', 'dep', 'hy', 'ma', 'iq', 'depr'
    ],
    "Ethics & Values": [
        'ethic', 'moral', 'honesty', 'justice', 'value', 'dignity', 'decency', 'satya', 'impartial', 'fairness'
    ],
    "Spirituality & Religion": [
        'spiritual', 'religious', 'sufi', 'buddhist', 'jewish', 'hindu', 'ching', 'kabbalah', 'sacred', 
        'quran', 'gita', 'seerah', 'zohar', 'shabbat', 'faith'
    ],

    # --- Cognitive & Skills ---
    "Cognitive Functions": [
        'memory', 'attention', 'reasoning', 'cognition', 'perception', 'focus', 'working memory', 'comprehension', 
        'logic', 'calculation', 'mental arithmetic', 'synthesis of information', 'identifying', 'evaluating solutions'
    ],
    "Skills & Competencies": [
        'skill', 'ability', 'competency', 'knowledge', 'expertise', 'literacy', 'proficiency', 'aptitude', 'craft', 
        'technical', 'soft skill', 'filing', 'culinary', 'computer'
    ],

    # --- Social & Emotional ---
    "Social & Interpersonal": [
        'social', 'relationship', 'friendship', 'interaction', 'cooperation', 'collaboration', 'community', 
        'bonding', 'attachment', 'empathy', 'talkativeness', 'support', 'civility', 'chivalrousness'
    ],
    "Leadership & Influence": [
        'leader', 'delegation', 'participation', 'influence', 'activator', 'managing'
    ],
    "Emotional State": [
        'emotion', 'feeling', 'mood', 'affect', 'sadness', 'happiness', 'anger', 'fear', 'joy', 'guilt', 
        'shame', 'grief', 'elation', 'hostility', 'irritability', 'vivacity', 'merriness', 'contentment'
    ],
    
    # --- Behavioral & Personal ---
    "Behavioral Patterns": [
        'behavior', 'pattern', 'habit', 'routine', 'lifestyle', 'sleeping', 'eating', 'volunteering', 
        'working', 'commuting', 'coping mechanism', 'response pattern', 'activities'
    ],
    "Motivation & Drives": [
        'motivation', 'desire', 'need', 'drive', 'orientation', 'excellence', 'ambition'
    ],
    "Self-Perception": [
        'self-', 'self '
    ],
    "Personality & Character Traits": [
        'character', 'trait', 'personality', 'temperament', 'virtue', 'vice', 'introversion', 'extroversion', 
        'conscientiousness', 'agreeableness', 'neuroticism', 'openness', 'grit', 'kindness', 'patience', 
        'perseverance', 'boldness', 'courage'
    ],

    # --- Physical & Health ---
    "Health & Wellness": [
        'health', 'medical', 'symptoms', 'diagnosis', 'pain', 'dietary', 'sleep', 'hormone', 'basophil', 
        'polygenic', 'caffeine', 'serotonin', 'well-being'
    ]
}


def categorise_facet(facet_name : str) -> str :
    f_lower = facet_name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in f_lower for keyword in keywords):
            return category
    return "General Attributes"
