import re

def is_valid_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_experience(input_text):
    pattern = r'^\s*\d+(\.\d+)?\s*(years?|months?)\s*$'
    return re.match(pattern, input_text.strip(), re.IGNORECASE) is not None