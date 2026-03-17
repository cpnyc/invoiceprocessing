# ai_extraction.py
import os

import pytesseract
from PIL import Image
from openai import OpenAI

# Load OpenAI API key from environment variable
from dotenv import load_dotenv


load_dotenv()  # This loads the variables from .env into os.environ

# Make sure to set it in your OS or terminal: export OPENAI_API_KEY="your_key"
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

def ocr_extract(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def parse_invoice_with_llm(invoice_text):
    prompt = f"""
    Extract the following fields from this invoice:
    - Vendor Name
    - Invoice Number
    - Date
    - Total Amount
    - PO Number

    Invoice Text:
    {invoice_text}

    Output as JSON.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    # Uncomment below line to view LLM raw output in console
    #print("LLM RAW OUTPUT:\n", response.choices[0].message.content)

    import json
    return json.loads(response.choices[0].message.content)