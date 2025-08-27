#Libraries
import streamlit as st
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #Download the Tesseract_OCR 
#print(pytesseract.get_tesseract_version())
from pdf2image import convert_from_bytes
import pdfplumber
from PIL import Image


#Based on the below the chosen libraries  for pdf extraction tools, including Greek content
#and integration with the Streamlit interface are:
#https://www.metriccoders.com/post/a-guide-to-pdf-extraction-libraries-in-python
#https://ploomber.io/blog/pdf-ocr/

#----------1. pdfplumber ----------------------------- 
#https://pypi.org/project/pdfplumber/#extracting-text
#- Used for text-based PDFs only   TEXT-BASED PDF  

#---------2. pdf2image + pytesseract -------------     
#- Used for scanned PDFs and images.                         SCANNED_PDF AND IMAGES
#- pdf2image converts PDF pages into images for OCR.  
#- pytesseract performs OCR to extract text from images.  

#---------3. ?? Alternative: PyMuDPF(fitz) ??? ----------
#- A bit more complex and not fully handle scanned-PDF

def extract_text(file, file_type):
    '''
    Extracts text from either PDF file or image
    
    Arguments:
    - file: (ByteIO object) Desired file for extraction 
    - file_type: (Str) "pdf" or "image"
    Return:
    - text: (Str) Text extracted from file 
    '''
    text = ""
    if file_type == "pdf":
        #Trying to extract text from text-based PDF first
        empty = True  #Flag in order to check if the text is empty
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True)    
                if page_text and page_text.strip(): #Remove extra indices or "\n"
                    text = page_text
                    empty = False
        
        if empty: #If text not found, probably scanned PDF so try OCR
            st.warning("Scanned-PDF detected, extracting using OCR....")
            file.seek(0)  # Pointer to the beginning of the file
            pages = convert_from_bytes(file.read(), dpi=200)  # Convert pages to images
            page_text = [pytesseract.image_to_string(page, lang="ell") for page in pages]
            text += "\n".join(page_text) 
            #print(len(text))

    elif file_type == "image":
        img = Image.open(file)
        text = pytesseract.image_to_string(img, lang="eng")

    return text

