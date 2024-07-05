import streamlit as st
from PIL import Image
import pytesseract
import re
import pandas as pd
import os

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path if needed

# Function to extract text from image using pytesseract
def extract_text(image, lang='eng'):
    return pytesseract.image_to_string(image, lang=lang)

# Function to parse extracted text to find name, email, phone, and address
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

# Ensure the directory to save images exists
image_save_path = 'uploaded_images'
if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)

# Streamlit app interface
st.title("Business Card Scanner")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    # Save the uploaded file to the directory
    image_path = os.path.join(image_save_path, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Open the image
    image = Image.open(image_path)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Select language for OCR
    language = st.selectbox('Select OCR Language', ['eng', 'jpn'])

    st.write("Extracting text from image...")
    extracted_text = extract_text(image, lang=language)
    st.write("Extracted Text:", extracted_text)

    st.write("Parsing extracted text...")
    parsed_data = parse_text(extracted_text)
    st.write("Parsed Data:", parsed_data)

    if st.button("Save to Database"):
        df = pd.DataFrame([parsed_data])
        
        # Check if file exists
        csv_file_path = 'business_cards.csv'
        if not os.path.isfile(csv_file_path):
            df.to_csv(csv_file_path, index=False)
        else:
            df.to_csv(csv_file_path, mode='a', header=False, index=False)
        
        st.write("Data saved to database")

# Add a button to download the CSV file
if os.path.exists('business_cards.csv'):
    with open('business_cards.csv', 'rb') as f:
        st.download_button(
            label="Download CSV",
            data=f,
            file_name='business_cards.csv',
            mime='text/csv'
        )

