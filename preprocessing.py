import pandas as pd
import numpy as np
import re
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

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

# Using category definitions for categorising facet by embedding generation and finding cosine similarity
# Took help of AI for these category definitions.
CATEGORY_DEFINITIONS = {
    "Core Personality Traits": "Describes fundamental, stable aspects of an individual's character, temperament, and enduring patterns of behavior. Includes traits like bravery, shyness, determination, honesty, cynicism, optimism, risk-taking, or caution.",
    "Emotional States & Affect": "Pertains to transient feelings, moods, and affective experiences. Includes happiness, anger, sadness, compassion fatigue, irritability, elation, contentment, and the general emotional tone of the text.",
    "Social & Interpersonal Dynamics": "Involves interactions between people, social skills, communication styles, and relationship patterns. Includes assertiveness, cooperation, sociability, aloofness, empathy, conflict resolution, and romantic or group dynamics.",
    "Cognitive Abilities & Thinking Styles": "Concerns mental processes like analytical thinking, memory, logic, problem-solving, perception, and learning. Includes statistical reasoning, critical thinking, creativity, and preferred ways of knowing (epistemology).",
    "Skills, Competencies & Knowledge": "Refers to specific, learned, practical abilities and areas of expertise. This includes technical skills like data analysis, physical skills like dance, and specific knowledge bases like anatomy or network basics.",
    "Work, Productivity & Leadership": "Relates to professional environments, work habits, productivity, leadership styles, meeting deadlines, and collaboration in a goal-oriented context.",
    "Motivation, Goals & Drives": "Concerns the underlying reasons for actions, ambitions, desires, and personal goals. This is about the 'why' behind behavior, like the need for achievement, power, or affiliation.",
    "Ethics, Values & Morality": "Relates to an individual's moral compass, principles, and beliefs about right and wrong. Includes concepts like justice, fairness, integrity, and adherence to ethical standards.",
    "Health, Biology & Wellness Habits": "Pertains to physical and mental health, biological traits, medical conditions, and daily lifestyle choices like diet, sleep, and exercise. Includes specific biological markers and health-related behaviors.",
    "Spirituality, Religion & Esoterica": "Involves faith, religious practices, meditation, philosophical beliefs, and esoteric or mystical systems. Includes specific doctrines, scripture, astrology, or new-age practices.",
    "Self-Concept & Personal Management": "Concerns how an individual views themselves, their self-worth, personal identity, and their ability to manage their own life. Includes self-esteem, self-awareness, self-improvement, and personal organization.",
    "Hobbies, Interests & Personal History": "Describes a person's leisure activities, hobbies, personal experiences, and demographic information. Includes travel history, artistic interests, personal background, and engagement with media or culture.",
    "Abstract & Qualitative Judgments": "A category for highly abstract or qualitative concepts that don't fit elsewhere, such as 'Structure', 'Brevity', 'Coarseness', or 'Classiness'. This is for concepts that describe the quality or form of something."
}

if __name__ == "__main__":
    
    try:
        print("----- Initializing embedding model (using Ollama) ----")
        embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
        
        print("---- cleaning raw facet data ------")
        raw_df = pd.read_csv('data/Facets_Assignment.csv')
        processed_df = pd.DataFrame()
        processed_df['facet_name'] = raw_df['Facets'].apply(clean_facets)
        facets_list = processed_df['facet_name'].tolist()

        print("----- Generating embeddings for category descriptions --------")
        category_names = list(CATEGORY_DEFINITIONS.keys())
        category_descriptions = list(CATEGORY_DEFINITIONS.values())
        category_embeddings = embeddings_model.embed_documents(category_descriptions)

        print(f"------ Generating embeddings for all {len(facets_list)} facets ----------")
        facet_embeddings = embeddings_model.embed_documents(facets_list)

        print("----- Calculating similarity between facets and categories ------")

        similarity_matrix = cosine_similarity(facet_embeddings, category_embeddings)

        best_category_indices = np.argmax(similarity_matrix, axis=1)
        assigned_categories = []
        for i in range(len(facets_list)):
            scores = similarity_matrix[i]
            best_score = np.max(scores)
            best_category_index = np.argmax(scores)
            
            # Applying the threshold
            if best_score >= 0.5:
                assigned_categories.append(category_names[best_category_index])
            else:
                # If not above threshold, assign to a 'General' category
                assigned_categories.append("General & Abstract Concepts")
        processed_df['category'] = assigned_categories

        output_path = 'data/processed_facets.parquet'
        processed_df.to_parquet(output_path, index=False)
        print(f"----- categorization complete. Data saved to '{output_path}'. ------")

        print("Final Columns:", processed_df.columns.tolist())
        print("Category Distribution:")
        print(processed_df['category'].value_counts().to_string())

    except Exception as e:
        print(f"[ERROR] : {e}")