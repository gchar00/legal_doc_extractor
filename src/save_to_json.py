#Libraries
import streamlit as st
import json 
import os 

def save_to_json(parsed_text, output_dir="output"):
    """
    Save  into a JSON file.

    Arguments:
    - parsed_text: (Dict) Key info from parsed text
    - output_dir: (Str) Directory to save the JSON file
    Returns:
    - output_path: (Str) Path of saved JSON file
    """
    os.makedirs(output_dir, exist_ok=True)

    # File name with timestamp for uniqueness
    filename = f"legal_document_extraction.json"
    output_path = os.path.join(output_dir, filename)
    # Save dictionary as JSON with Greek support
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_text, f, ensure_ascii=False, indent=4)

    return output_path