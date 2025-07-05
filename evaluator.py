import pandas as pd
import json
from typing import Dict
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import asyncio
import os

try:
    facets_df = pd.read_parquet('data/processed_facets.parquet')
    UNIQUE_CATEGORIES = facets_df['category'].unique().tolist()
except FileNotFoundError:
    print("file not found.")
    exit()

IS_DOCKER = os.environ.get("RUNNING_IN_DOCKER") == "1"

OLLAMA_HOST = (
    "http://host.docker.internal:11434" if IS_DOCKER else "http://localhost:11434"
)
llm = ChatOllama(
    model="llama3",
    temperature=0.0,
    format="json",
    request_timeout=120.0,
    base_url = OLLAMA_HOST
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

async def evaluate_category_async(category: str, text: str) -> Dict:
    facets_in_category = facets_df[facets_df['category'] == category]['facet_name'].tolist()
    facet_list_str = "\n- ".join(facets_in_category)

    print(f"Evaluating category: '{category}'...")
    try:
        result = await chain.ainvoke({
            "text_to_evaluate": text,
            "category_name": category,
            "facet_list": facet_list_str
        })
        print(f" Finished evaluating category: '{category}'")
        return result
    except Exception as e:
        print(f" ERROR in category '{category}': {e}")
        return {facet: {"error": str(e)} for facet in facets_in_category}

async def evaluate_conversation_turn_async(text: str) -> Dict:
    if not text.strip():
        print("Empty text !")
        return {}

    print(f"Evaluating for: \"{text[:50]}...\"")
    tasks = [evaluate_category_async(cat, text) for cat in UNIQUE_CATEGORIES]
    results = await asyncio.gather(*tasks)

    combined = {}
    for partial in results:
        combined.update(partial)

    print("All categories evaluated.")
    return combined

# if __name__ == '__main__':
#     async def main():
#         test_text = "This service is terrible. I have been on hold for 45 minutes and I am extremely angry."
#         results = await evaluate_conversation_turn_async(test_text)
#         print("\n--- FINAL RESULTS ---")
#         print(json.dumps(results, indent=2))

#     asyncio.run(main())