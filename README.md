# AI-mortgage-data-extraction
🏦 Overview

This project automates the extraction of critical mortgage information from scanned PDF documents.
Manually handling mortgage files is slow, error-prone, and not scalable. With this system, we combine OCR (Optical Character Recognition) and AI-powered parsing to automatically extract borrower, loan, and lender details into a structured JSON format.

⚡ Key Features

🔍 OCR Integration → Uses Tesseract OCR to convert scanned PDFs into text.

📑 Multi-page Support → Extracts data from PDFs with 1 page or 100+ pages.

🤖 Hybrid Pipeline → Regex for quick detection, Gemini AI fallback for missing details.

📊 Structured Output → Final results saved as clean JSON.

📂 Batch Processing → Supports one or multiple PDFs in a single run.

🏢 Scalable Design → Enterprise-ready architecture to process large datasets.

📂 Extracted Fields

The pipeline extracts the following information from mortgage documents:

👤 Borrowers (names + relationship)

💰 Loan Amount

📅 Recording Date

🏛 Recording Location (County Clerk)

🏦 Lender Name

🆔 Lender NMLS ID

🧑‍💼 Broker Name (if available)

👨‍💼 Loan Originator Name

🆔 Loan Originator NMLS ID

🖥️ Sample JSON Output
{
  "borrowers": [
    {
      "name": "ELIZABETH HOWERTON",
      "relationship": "Spouse"
    },
    {
      "name": "TRAVIS HOWERTON",
      "relationship": "Spouse"
    }
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

⚙️ Tech Stack

Python 3.11+

Tesseract OCR → Text extraction from scanned PDFs

LangChain + Google Gemini AI → AI fallback for unstructured fields

Regex → Rule-based text matching for accuracy

pdf2image → PDF to image conversion

📌 Workflow

Upload one or multiple mortgage PDFs

OCR converts each page into text

Regex extracts structured fields

Missing fields auto-filled using Gemini AI

Final results stored as JSON files

🚀 Future Enhancements

Cloud deployment (AWS/GCP) for enterprise scale

Web dashboard to upload & track PDF processing

Database integration (MongoDB / PostgreSQL)

REST API for fintech integration

Advanced NLP for relationship detection

🎯 Why This Matters

⏳ Saves time → Automates a task that takes hours manually

✅ Reduces errors → AI ensures accuracy in key legal/financial data

📈 Scalable → Can handle 1 or 1000 PDFs

💼 Business impact → Useful for banks, mortgage companies, legal firms, HR & compliance teams

📖 Conclusion

As a Data Analyst, I designed this system to demonstrate how AI + OCR can transform real-world document processing.
This project highlights my ability to:

Understand a business problem

Build a technical pipeline (OCR + AI + Regex)

Deliver enterprise-ready, scalable, and accurate solutions
