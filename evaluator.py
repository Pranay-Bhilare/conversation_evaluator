import pandas as pd
import json
from typing import Dict
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

try:
    facets_df = pd.read_parquet('data/processed_facets.parquet')
    UNIQUE_CATEGORIES = facets_df['category'].unique().tolist()
except FileNotFoundError:
    print("file not found.")
    exit()

llm = ChatOllama(
    model="llama3",
    temperature=0.0,
    format="json",
    request_timeout=120.0
)

json_parser = JsonOutputParser()

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """
    You are a precise and objective conversation analyst. Your task is to evaluate a piece of text against a list of related facets from a specific category.

    --- INSTRUCTIONS ---
    For each facet in the 'Facet List' below, you must provide a structured evaluation containing three keys:
    1. "score": An integer score from 1 to 5, where 1 means the text shows a complete absence of the facet, and 5 means the text strongly and clearly demonstrates the facet.
    2. "justification": A brief, one-sentence justification for your score.
    3. "confidence": An integer score from 1 (low confidence) to 5 (high confidence) in your evaluation.

    --- OUTPUT FORMAT ---
    You MUST provide your response ONLY as a single, valid JSON object. Do not include any other text, explanations, or markdown formatting like ```json. The JSON object's keys should be the exact facet names from the list.

    Example Format:
    {{
    "Facet Name 1": {{ "score": <int>, "justification": "<string>", "confidence": <int> }},
    "Facet Name 2": {{ "score": <int>, "justification": "<string>", "confidence": <int> }}
    }}
    """),
    ("human", """
    --- TEXT TO EVALUATE ---
    {text_to_evaluate}
    ---

    --- FACET LIST (Category: {category_name}) ---
    {facet_list}
    """)
])

chain = PROMPT_TEMPLATE | llm | json_parser

def evaluate_conversation_turn(text: str) -> Dict:
    if not text.strip():
        print("Input text is empty.")
        return {}

    print(f"Evaluating for text: \"{text[:50]}...\"")
    full_results = {}
    total_facets = len(facets_df)
    processed_facets = 0

    for i, category in enumerate(UNIQUE_CATEGORIES):
        print(f"  ({i+1}/{len(UNIQUE_CATEGORIES)}) Evaluating category: '{category}'...")

        facets_in_category = facets_df[facets_df['category'] == category]['facet_name'].tolist()
        facet_list_str = "\n- ".join(facets_in_category)

        try:
            response_data = chain.invoke({
                "text_to_evaluate": text,
                "category_name": category,
                "facet_list": facet_list_str
            })

            full_results.update(response_data)
            processed_facets += len(facets_in_category)
            print(f" category: '{category}' : {processed_facets}/{total_facets} facets scored.")

        except (OutputParserException, json.JSONDecodeError) as e:
            print(f" ERROR: Parsing failed for category '{category}'. ERROR DETAILS : {e}")
            for facet_name in facets_in_category:
                full_results[facet_name] = {"error": "Failed to parse LLM response."}

        except Exception as e:
            print(f" ERROR: for '{category}'. Details: {e}")
            for facet_name in facets_in_category:
                full_results[facet_name] = {"error": f"Unexpected error: {e}"}

    print("Evaluation complete.")
    return full_results

if __name__ == '__main__':
    test_text = "This service is terrible. I have been on hold for 45 minutes and I am extremely angry."
    results = evaluate_conversation_turn(test_text)
    
    print("--- FULL EVALUATION RESULTS ---")
    print(json.dumps(results, indent=2))