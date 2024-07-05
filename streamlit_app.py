import streamlit as st
from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def extract_text(image):
    return pytesseract.image_to_string(image)

def parse_text(text):
    name, email, phone, address = None, None, None, None

    # Using regex to find email and phone
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'\+?\d[\d -]{8,}\d', text)
    
    if email_match:
        email = email_match.group(0)
    if phone_match:
        phone = phone_match.group(0)

    # Assuming the first line is the name and the rest is address (a simple assumption)
    lines = text.split('\n')
    if lines:
        name = lines[0]
        address = ' '.join(lines[1:])

    return {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Address': address
    }

st.title("Business Card Scanner")

uploaded_file = st.file_uploader("Choose a visiting card image to scan...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    st.write("Extracting text from image...")
    extracted_text = extract_text(image)
    st.write("Extracted Text:", extracted_text)

    st.write("Parsing extracted text...")
    parsed_data = parse_text(extracted_text)
    st.write("Parsed Data:", parsed_data)

    if st.button("Save to Database"):
        # Here you can add code to save parsed_data to a database
        st.write("Data saved to database")

