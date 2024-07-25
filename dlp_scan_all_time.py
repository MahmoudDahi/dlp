import os
import time
import pandas as pd
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(filepath):
    # Email configurations
    sender_email = 'dlptestproject@hotmail.com'
    receiver_email = 'mahmoudadahi@hotmail.com'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # or 465 for SSL/TLS

    # Email credentials (replace with your own)
    email_username = 'dlptestproject@hotmail.com'
    email_password = '#iTestProject'

    subject = 'Log Report'
    body = "This is a test email log report \n FilePath= " +filepath

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(email_username, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def scan_for_credit_cards(data):
    # Regular expression for matching credit card numbers
    pattern = r'\b(?:\d[ -]*?){13,16}\b'
    matches = re.findall(pattern, data)
    return matches

def redact_credit_cards(data):
    # Replace credit card numbers with asterisks
    # pattern = r'\b(?:\d[ -]*?){13,16}\b'
    pattern = r'(?:\d[ -]*?){12}'
    redacted_data = re.sub(pattern, '*' * 12, data)
    return redacted_data

# Function to scan Excel file for sensitive data
def scan_excel_file(file_path):
    foundSenstivieNum = False
    df = pd.read_excel(file_path)
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Iterate over each cell in the DataFrame
        for column in df.columns:
            for index, cell in df[column].items():
                # Scan cell for credit card numbers
                credit_cards = scan_for_credit_cards(str(cell))
                if credit_cards:
                    foundSenstivieNum = True
                    print(f"Sensitive data detected in cell {index} of column {column}: {credit_cards}")
                    # Redact credit card numbers
                    df.at[index, column] = redact_credit_cards(str(cell))
                
                    
        if foundSenstivieNum:       
        # Save the modified DataFrame back to the Excel file
             df.to_excel(file_path, index=False)
             send_email(file_path)

             print("Excel file processed successfully.")
             foundSenstivieNum = False
    else:
        print("File not found.")
    # Implement your scanning logic here
    # For example, scan specific columns for credit card numbers
    # If sensitive data is found, take appropriate action

def main():
    
        # Directory to monitor
    directory_to_monitor = '/home/dahi/Downloads'
    
    # Dictionary to store modification times of Excel files
    excel_files_modification_times = {}
    
    while True:
        # Get list of Excel files in the directory
        excel_files = [file for file in os.listdir(directory_to_monitor) if file.endswith('.xlsx')]
    
        for excel_file in excel_files:
            file_path = os.path.join(directory_to_monitor, excel_file)
            modification_time = os.path.getmtime(file_path)
    
            # Check if the file is new or modified since last check
            if excel_file not in excel_files_modification_times or modification_time > excel_files_modification_times[excel_file]:
                excel_files_modification_times[excel_file] = modification_time
                print(f"Scanning Excel file: {excel_file}")
                scan_excel_file(file_path)
    
        # Sleep for some time before checking again
        time.sleep(60)  # Sleep for 1 minute before checking again    

main()
