# invoice_input.py
import os
from PyPDF2 import PdfReader
from email import message_from_string

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def read_pdf(file_path):
    pdf = PdfReader(file_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def read_email(email_file):
    with open(email_file, 'r') as f:
        msg = message_from_string(f.read())
    return msg.get_payload()

def read_scanned_doc(file_path):
    # Placeholder for OCR (see AI Layer)
    return file_path



def read_image_pdf(pdf_path):
    """
    Convert each page of PDF into an image, then OCR it
    """
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text