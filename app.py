#Libraries
import streamlit as st
import json
from src.extractor import extract_text
from src.parser import clean_ocr_noise, parse_text
from src.save_to_json import save_to_json

#Open browser at http://localhost:8501 and create your UI app
st.title("Welcome to Streamlit! :)")
name = st.text_input("Enter your name:")
if name:
    st.success(f"Welcome, {name}!")
    ###############  Upload your desired file--> simbolaio-agorapolisias-public.pdf ##################
    #Ensure the type of the file is either pdf or image 
    document = st.file_uploader("Upload your desired file(PDF or image): ", type =["pdf","png","jpg","jpeg"])
    if document: #BytesIO object 
        st.success(f"File uploaded successfully! Ready to extract text")
        #Debugging
        #print(document.type) #Output will be "application/pdf" or "image/*image_type*"
        try:
############  Extract text from the file using the extractor.py ###############
            with st.spinner("Extracting text...", show_time=True):
                #st.info("Extracting text...")
                if document.type == "application/pdf": 
                    text = extract_text(document,"pdf")
                else: 
                    text = extract_text(document,"image")
            st.success(f"Extraction from File Completed!")
            st.text_area("Extracted Text (Preview)", text, height=200)
############  Parsing text using the parser.py ###############
            with st.spinner("Cleaning OCR noise and formatting text...",show_time=True):
                clean_text = clean_ocr_noise(text)
                st.text_area("Cleaned Text (Preview)", clean_text, height=200)
                parsed_text = parse_text(clean_text)
            st.success(f"Parsing completed!!")
            st.text_area("Parsed Text (Preview)", parsed_text, height=200)
############# Saving key info to JSON using save_to_json.py and display #############
            with st.spinner("Saving JSON...",show_time=True):
                json_path = save_to_json(parsed_text)
            st.success(f"Structured JSON data saved successfully! {json_path}")
            # Display JSON content
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            st.json(data)
        
        except Exception as e:
            st.error(f"Problem with the extraction or parsing process: {e}")
        
