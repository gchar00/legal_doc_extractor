# Legal Document Data Extractor

A Streamlit application that extracts structured data from Greek legal documents, such as property deeds. The app aims to handle both text-based PDFs and scanned documents using OCR.

## Overall Approach & Design Decisions

1) **User Input via Streamlit**:
    - Users enter their name for a personalized experience.
    - Users upload a legal document (PDF or image).
  
2. **Text Extraction**:
    - **Text-based PDFs** are processed using  library `pdfplumber`.
    - **Scanned PDFs or images** are processed using `pdf2image` to convert pages into images, and then `pytesseract` performs OCR with Greek language support (`ell`).

3. **Text Cleaning**:
    - Remove OCR noise, extra whitespace, page markers, and hyphenation.

4. **Parsing & Data Extraction**:
    - Regex-based extraction identifies:
        - **Involved parties**: sellers, buyers, notary details.
        - **Property details**: type, address, area, floor, building permit number.
    - The parsed data is structured into a Python dictionary and can be saved as JSON.


## Tools, Frameworks & Libraries

| Library / Tool | Purpose |
|----------------|---------|
| **Streamlit** | Web interface for interactive file upload and data display. |
| **pdfplumber** | Extract text from text-based PDFs. |
| **pdf2image** | Convert PDF pages to images for OCR processing. |
| **pytesseract** | OCR engine to extract text from images (supports Greek). |
| **Pillow (PIL)** | Image processing. |
| **re (regex)** | Pattern matching for parsing structured data. |
| **Docker (optional)** | Containerized deployment for reproducibility. |

## Assumptions

- Legal documents follow a typical Greek property template.
- File language is assumed to be Greek only.
- Regex parsing is written based on keywords for each group. It is not fully robust, but demonstrative. 
- Sellers/Βuyers may be represented by legal representatives or proxies.




## How to Use the Streamlit App

1. **Run the app** locally:

```bash
streamlit run app.py

2. Open the app in your browser:

http://localhost:8501

3. Enter your name and upload a PDF or image file (e.g., `simbolaio-agorapolisias-public.pdf`).

4. The app will:
   - Extract text from the document (OCR if needed)
   - Clean the text from OCR noise
   - Parse the key structured information
   - Display extracted text, cleaned text, and structured JSON

