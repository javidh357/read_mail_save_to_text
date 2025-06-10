import email
import imaplib
import os
from email.header import decode_header
import PyPDF2
  
# Configuration
EMAIL = "chaitrapaladugula@gmail.com"
PASSWORD = "********"  
IMAP_SERVER = "imap.gmail.com"   
SUBJECT_KEYWORD = "Invoice"
EXTRACTED_TEXT_FILE = "EXTRACTED_TEXT_FILE.TXT"

# 1. Create a function to connect to the IMAP server
def connect_to_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    print("Logged in to Gmail")
    return mail

# 2. Select the mailbox (folder) you want to search - usually 'inbox'
def select_mailbox(mail, folder='inbox'):
    mail.select(folder)
    print(f"Selected mailbox: {folder}")

# 3. Search for emails with the given subject keyword
def search_emails(mail, subject_keyword):
    status, messages = mail.search(None, f'(SUBJECT "{subject_keyword}")')
    if status != "OK":
        print("No messages found.")
        return []
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} emails with subject containing '{subject_keyword}'")
    return email_ids

# 4. Fetch an email by ID and parse it
def fetch_email(mail, email_id):
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    if status != "OK":
        print(f"Failed to fetch email ID {email_id}")
        return None
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    return email_message

# 5. Process the email to extract PDF attachments
def extract_pdfs_from_email(email_message):
    pdf_files = []
    
    if email_message.is_multipart():
        for part in email_message.walk():
            content_disposition = str(part.get("Content-Disposition"))
            
            if "attachment" in content_disposition:
                filename = part.get_filename()
                
                if filename and filename.lower().endswith(".pdf"):
                    print(f"Found PDF attachment: {filename}")
                    pdf_files.append((filename, part.get_payload(decode=True)))
    return pdf_files

# 6. Save PDFs temporarily and extract text using PyPDF2
def extract_text_from_pdfs(pdf_files):
    all_text = ""
    
    for filename, payload in pdf_files:
        # Save PDF temporarily
        temp_pdf_path = f"temp_{filename}"
        with open(temp_pdf_path, "wb") as f:
            f.write(payload)

        try:
            reader = PyPDF2.PdfReader(temp_pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            all_text += f"--- Extracted Text from {filename} ---\n{text}\n\n"
        except Exception as e:
            print(f"Error reading PDF {filename}: {e}")
        finally:
            os.remove(temp_pdf_path)  # Clean up temporary file
    
    return all_text

# 7. Write extracted text to output file
def save_extracted_text(text, output_file=EXTRACTED_TEXT_FILE):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted text saved to {output_file}")

# Main function
def main():
    # Connect to Gmail
    mail = connect_to_gmail()

    # Select inbox
    select_mailbox(mail)

    # Search for emails with the subject keyword
    email_ids = search_emails(mail, SUBJECT_KEYWORD)

    full_extracted_text = ""

    for email_id in email_ids:
        print(f"\nProcessing email ID: {email_id.decode()}")
        email_message = fetch_email(mail, email_id)
        
        if email_message:
            pdf_attachments = extract_pdfs_from_email(email_message)
            if pdf_attachments:
                extracted_text = extract_text_from_pdfs(pdf_attachments)
                full_extracted_text += extracted_text

    # Save all extracted text to file
    if full_extracted_text:
        save_extracted_text(full_extracted_text, EXTRACTED_TEXT_FILE)
    else:
        print("No PDFs or text extracted.")

    # Logout
    mail.logout()
    print("Logged out from Gmail")

if __name__ == "__main__":
    main()