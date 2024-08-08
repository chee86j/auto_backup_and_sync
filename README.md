Python Automated Backup & Sync Script
Welcome to the Automated Backup & Sync Script! 
This script is made to automate backing up your files from a specified source directory to a backup directory & sends email notifications w/ a detailed backup Report upon completion.

## Key Features
1. **Automated File Backup**: Automatically backs up new & modified files from the source directory to the backup directory.
2. **Email Notifications**: Sends an email notification upon successful backup or in case of an error.
3. **Detailed Backup Report**: Generates & Emails a Report listing all backed-up files.
4. **Daily Scheduling**: Automatically runs the backup process daily at a specified time.

## Technologies & Libraries
1. `os` for Interacting w/ the Operating System.
2. `shutil` for High-level File Operations like Moving & Copying Files.
3. `logging` for Error Logging & Debugging.
4. `schedule` for Scheduling Tasks.
5. `smtplib` & `email.mime` for Sending Email Notifications.

## Prerequisites
Before running the script, ensure you have the following installed:

1. **Python**: Ensure Python 3.x is installed on your system. [Download Python](https://www.python.org/downloads/).

## Configuration
Before running the script, you need change these setting in the script:

1. **Source Directory**: The Directory from which files will be backed up.
    ```python
    SOURCE_DIR = 'C:/Users/username/Documents'  # Replace w/ your source directory
    BACKUP_DIR = 'D:/Backup/Documents'  # Replace w/ your backup directory

1. **Email Function**: The Email Settings to which you will Send & Receive Report
    ```python
    EMAIL_SENDER = 'your_email@example.com'  # Replace w/ your email
    EMAIL_RECEIVER = 'receiver_email@example.com'  # Replace w/ the receiver's email
    EMAIL_SUBJECT = 'Backup Report'  # Subject of the email
    EMAIL_SMTP_SERVER = 'smtp.example.com'  # Replace w/ your email SMTP server
    EMAIL_SMTP_PORT = 587  # Replace w/ your email SMTP port
    EMAIL_USERNAME = 'your_email@example.com'  # Replace w/ your email username
    EMAIL_PASSWORD = 'your_password'  # Replace w/ your email password

## Running The Script
To execute the script, run the command `python3 BackupAndSync.py` or `python BackupAndSync.py` in the terminal once you have navigated to the directory containing `BackupAndSync.py`