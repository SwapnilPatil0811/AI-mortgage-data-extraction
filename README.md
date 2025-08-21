# AI-mortgage-data-extraction
This project demonstrates an AI-powered pipeline that extracts structured information from scanned mortgage PDFs.

Most mortgage documents are scanned images, making data entry slow and error-prone. This solution combines OCR (Tesseract), Regex parsing, and Google Gemini LLM to deliver accurate, structured JSON outputs from raw PDFs.

✨ Key Highlights

Handles multiple PDFs at once 📂

Extracts borrowers, loan details, lender, broker, and originator info

Hybrid approach → OCR + Regex + LLM fallback for higher accuracy

Output is stored in clean JSON format, ready for databases or downstream apps

Designed to be scalable for enterprise use cases

🔍 Extracted Fields

Borrowers (names + relationships)

Loan amount

Recording date & location

Lender name & NMLS ID

Broker name (if available)

Loan originator name & NMLS ID

⚙️ Tech Stack

Python 🐍

Tesseract OCR (text extraction from scanned pages)

LangChain + Gemini API (AI-powered extraction)

Regex (fast rule-based matching)

🚀 How It Works

Upload PDF(s) → system runs OCR on every page

Regex extracts known fields

AI (Gemini) fills missing details

Final result saved as a single JSON file

📊 Sample JSON Output
{
  "borrowers": [
    { "name": "ELIZABETH HOWERTON", "relationship": "Spouse" },
    { "name": "TRAVIS HOWERTON", "relationship": "Spouse" }
  ],
  "loan_amount": "$475950.00",
  "recording_date": "04/01/2025",
  "recording_location": "Albany County Clerk's Office",
  "lender_name": "US MORTGAGE CORPORATION",
  "lender_nmls_id": 3901,
  "broker_name": null,
  "loan_originator_name": "William John Lane",
  "loan_originator_nmls_id": 65175
}

🌍 Real-World Impact

Reduces manual data entry time ⏳

Improves accuracy in mortgage processing ✅

Scales to handle hundreds of PDFs daily

Saves cost for lenders, brokers, and enterprises 💡
