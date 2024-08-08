import os
import shutil
import logging
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration to be set by user
SOURCE_DIR = 'C:/Users/username/Documents'  # Replace with your source directory
BACKUP_DIR = 'D:/Backup/Documents'  # Replace with your backup directory
EMAIL_SENDER = 'your_email@example.com' # Replace with your email
EMAIL_RECEIVER = 'receiver_email@example.com' # Replace with the email of the receiver
EMAIL_SUBJECT = 'Backup Report' # Subject of the email
EMAIL_SMTP_SERVER = 'smtp.example.com' # Replace with your email SMTP server
EMAIL_SMTP_PORT = 587 # Replace with your email SMTP port
EMAIL_USERNAME = 'your_email@example.com' # Replace with your email username
EMAIL_PASSWORD = 'your_password' # Replace with your email password

# Email Function
def send_email(subject, body):
    msg = MIMEMultipart() # Create a message using MIMEText
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Try and Except block to send the email
    try:
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) # this is the SMTP server and port
        server.starttls() # this is the secure connection
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD) # login to the email server
        text = msg.as_string() # convert the message to a string
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text) # send the email
        server.quit() # logout from the server
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Function to get all files in a directory
def get_all_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

# Backup Function
def backup_files():
    try:
        source_files = get_all_files(SOURCE_DIR)
        backup_files = get_all_files(BACKUP_DIR)
        
        # Create Dictionary w/Relative Path as Key and Full Path as Value for Quick Lookup
        backup_files_dict = {os.path.relpath(file, BACKUP_DIR): file for file in backup_files}
        
        files_backed_up = [] # List to keep track of backed up files

        for file in source_files:
            rel_path = os.path.relpath(file, SOURCE_DIR)
            backup_file_path = os.path.join(BACKUP_DIR, rel_path)
            
            # Create Directory if it does not exist
            if not os.path.exists(os.path.dirname(backup_file_path)):
                os.makedirs(os.path.dirname(backup_file_path))
                
            # If File not in Backup Directory or is Outdated, Copy it
            if (rel_path not in backup_files_dict or
                os.path.getmtime(file) > os.path.getmtime(backup_files_dict[rel_path])):
                shutil.copy2(file, backup_file_path)
                files_backed_up.append(file) # Add File to List of Backed Up Files
                logging.info(f"Backed up: {file} -> {backup_file_path}")
        
        # Generate and send backup report
        report = generate_backup_report(files_backed_up)
        send_email(EMAIL_SUBJECT, report)
        logging.info("Backup completed successfully")
    except Exception as e:
        logging.error(f"Error during backup: {e}")
        send_email(EMAIL_SUBJECT, f"Backup failed: {e}")

# Function to Generate a Backup Report
def generate_backup_report(files):
    report = "Backup Report:\n\n"
    report += f"Total files backed up: {len(files)}\n\n"
    report += "Files:\n"
    for file in files:
        report += f"{file}\n"
    return report

# Scheduling to Run the Backup at Specific Time
def run_scheduler():
    schedule.every().day.at("02:00").do(backup_files)  # Backup Files Daily at 2:00 AM
    
    while True:  # Condition to keep the script running
        schedule.run_pending()  # Check if any scheduled tasks are due
        time.sleep(1)  # Sleep for 1 second before checking again

# Main Function to Run the Scheduler
if __name__ == '__main__':
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    # The Line above creates a log file named backup.log in the same directory as the script w/th log file containg 
    # the time, log level, and message using the format specified
    run_scheduler()
