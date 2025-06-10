# read_mail_save_to_text

# 📥 Gmail PDF Invoice Extractor

This Python script automatically logs into a Gmail account, searches for emails with a specific subject (like "Invoice"), downloads attached PDF files, extracts their text using PyPDF2, and saves the text to a `.txt` file.

## 🚀 Features

- Connects securely to Gmail using IMAP
- Searches emails by subject keyword (default: "Invoice")
- Automatically fetches PDF attachments
- Extracts readable text from each PDF using PyPDF2
- Saves all extracted text into one text file
- Cleans up temporary files after processing

---

## 🧰 Requirements

- Python 3.6+
- Required Libraries:
  - `imaplib`
  - `email`
  - `PyPDF2`
  - `os`

You can install the required library with:

```bash
pip install PyPDF2
