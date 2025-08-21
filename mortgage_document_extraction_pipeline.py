#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install paddleocr pdf2image pillow langchain langchain-google-genai google-generativeai


# In[2]:


get_ipython().system('pdftoppm -v')


# In[3]:


get_ipython().system('pip install pytesseract')


# In[4]:


get_ipython().system('tesseract -v')


# In[5]:


import pytesseract


# In[6]:


from pdf2image import convert_from_path
import pytesseract
import re, json


# In[7]:


# Tesseract Path (update if installed somewhere else)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_pdf_to_text(pdf_path, dpi=200):
    """Convert full PDF to text using OCR"""
    pages = convert_from_path(pdf_path, dpi=dpi)
    all_text = ""
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang="eng")
        all_text += f"\n\n===== PAGE {i} =====\n\n{text}\n"
        print(f" OCR Done for page {i}")
    return all_text


# In[30]:


import re

def extract_mortgage_fields(text):
    data = {
        "borrowers": None,
        "loan_amount": None,
        "recording_date": None,
        "recording_location": None,
        "lender_name": None,
        "lender_nmls_id": None,
        "broker_name": None,
        "loan_originator_name": None,
        "loan_originator_nmls_id": None
    }

    # Borrowers (search in Party1 section or Capitalized names)
    borrowers = re.findall(r"Party1:?\s*(.+)", text, re.IGNORECASE)
    if borrowers:
        data["borrowers"] = borrowers[0].strip()

    # Loan Amount
    amt = re.search(r"(Mtg Amt|Loan Amount)[: ]\s*\$?([\d,]+\.\d{2}|\d+)", text, re.IGNORECASE)
    if amt:
        data["loan_amount"] = "$" + amt.group(2).replace(",", "")

    # Recording Date
    date = re.search(r"Rec Date[: ]\s*([\d/]{8,10})", text, re.IGNORECASE)
    if date:
        data["recording_date"] = date.group(1)

    # Recording Location (County Clerk)
    loc = re.search(r"([A-Z]+ COUNTY).*CLERK", text, re.IGNORECASE)
    if loc:
        data["recording_location"] = loc.group(1).title() + " Clerk's Office"

    # Lender Name (Party2 section)
    lender = re.search(r"Party2:?\s*(.+)", text, re.IGNORECASE)
    if lender:
        data["lender_name"] = lender.group(1).strip()

    # Lender NMLS ID
    lender_id = re.search(r"Lender NMLS\s*#?\s*(\d+)", text, re.IGNORECASE)
    if lender_id:
        data["lender_nmls_id"] = lender_id.group(1)

    # Broker Name
    broker = re.search(r"Broker[: ]\s*(.+)", text, re.IGNORECASE)
    if broker:
        data["broker_name"] = broker.group(1).strip()

    # Loan Originator Name
    originator = re.search(r"Loan Originator[: ]\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if originator:
        data["loan_originator_name"] = originator.group(1).strip()

    # Loan Originator NMLS ID
    originator_id = re.search(r"Originator NMLS\s*#?\s*(\d+)", text, re.IGNORECASE)
    if originator_id:
        data["loan_originator_nmls_id"] = originator_id.group(1)

    return data


# In[31]:


# ==== RUN PIPELINE ====
pdf_path = r"C:\Users\patil\OneDrive\Desktop\Mortgage_PDF\0a5edada-aefc-4392-86e1-f712fcd73b97-howerton_albany_doc1.pdf"

print(" Running OCR on PDF...")
ocr_text = ocr_pdf_to_text(pdf_path)

print("\n Extracting fields...")
final_json = extract_mortgage_fields(ocr_text)

print("\n Final JSON Output:")
print(json.dumps(final_json, indent=2))


# In[32]:


# ==== RUN PIPELINE ====
pdf_path = r"C:\Users\patil\OneDrive\Desktop\Mortgage_PDF\40d0d5a2-4092-42a7-964a-fa3f327c36fc-tusi_albany_doc1.pdf"

print(" Running OCR on PDF...")
ocr_text = ocr_pdf_to_text(pdf_path)

print("\n Extracting fields...")
final_json = extract_mortgage_fields(ocr_text)

print("\n Final JSON Output:")
print(json.dumps(final_json, indent=2))


# In[33]:


# ==== RUN PIPELINE ====
pdf_path = r"C:\Users\patil\OneDrive\Desktop\Mortgage_PDF\775756e0-fc28-4da1-a9de-999c9df71131-howerton_albany_doc1.pdf"

print(" Running OCR on PDF...")
ocr_text = ocr_pdf_to_text(pdf_path)

print("\n Extracting fields...")
final_json = extract_mortgage_fields(ocr_text)

print("\n Final JSON Output:")
print(json.dumps(final_json, indent=2))


# In[64]:


import os, re, json
from pdf2image import convert_from_path
import pytesseract
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# In[65]:


# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["GOOGLE_API_KEY"] = "AIzaSyAuL1R9djGa56b-dTDBGw8iMD1TuUsUJNA"   # apna key daalna


# In[66]:


# === OCR FUNCTION ===
def ocr_pdf_to_text(pdf_path, dpi=200):
    pages = convert_from_path(pdf_path, dpi=dpi)
    all_text = ""
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang="eng")
        all_text += f"\n\n===== PAGE {i} =====\n\n{text}\n"
        print(f" OCR Done for {os.path.basename(pdf_path)} - Page {i}")
    return all_text


# In[75]:


# === GEMINI FALLBACK (Safe JSON Parse) ===
def gemini_fallback(text, current_data):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    # ✅ FIXED: Escaped curly braces with double {{ }}
    template = """
    You are an expert in U.S. mortgage documents.
    Extract the following fields in STRICT JSON format:

    {{
      "borrowers": [
        {{ "name": "string", "relationship": "string" }}
      ],
      "loan_amount": "string",
      "recording_date": "string",
      "recording_location": "string",
      "lender_name": "string",
      "lender_nmls_id": int,
      "broker_name": "string or null",
      "loan_originator_name": "string",
      "loan_originator_nmls_id": int
    }}

    Current JSON:
    {current_json}

    Fill missing values from the text below if possible.
    Return STRICT JSON only.

    Text:
    {text}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["text", "current_json"]
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    raw_output = chain.run({"text": text, "current_json": json.dumps(current_data)})

    # Debug print
    print("\n Gemini Raw Output (first 300 chars):\n", raw_output[:300])

    # Extract JSON safely
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if match:
        clean_json = match.group(0)
    else:
        raise ValueError(" Gemini did not return valid JSON!")

    return json.loads(clean_json)


# In[76]:


# === RUN FOR ALL PDFs IN A FOLDER ===
pdf_folder = r"C:\Users\patil\OneDrive\Desktop\Mortgage_PDF"
all_results = []

for file in os.listdir(pdf_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        print(f"\n Processing PDF: {file}")
        
        ocr_text = ocr_pdf_to_text(pdf_path)
        regex_data = extract_mortgage_fields(ocr_text)
        final_data = gemini_fallback(ocr_text, regex_data)

        result_entry = {
            "pdf": file,
            "data": final_data
        }
        all_results.append(result_entry)

        # Print each PDF result nicely
        print("\n Extracted Data:")
        print(json.dumps(result_entry, indent=2))

# === SAVE ONE COMBINED JSON FILE ===
output_file = os.path.join(pdf_folder, "all_mortgages.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"\n ALL PDFs Processed Successfully!")
print(f" Combined JSON saved at: {output_file}")

