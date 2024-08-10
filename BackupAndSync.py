import sys
import os
import shutil
import logging
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QTimeEdit, QHBoxLayout
from PySide6.QtCore import QTime

# BackupApp Class to Create the GUI
class BackupApp(QWidget):
    def __init__(self):
        super().__init__() # Call the parent class constructor
        self.initUI() # Call the initUI method to build the GUI

    # Intialize the UI Elements & Layout
    def initUI(self):
        self.setWindowTitle('Backup and Sync Settings') # Set the Window Title
        layout = QVBoxLayout() # Create a Vertical Box Layout

        # Source Directory Elements
        self.source_label = QLabel('Source Directory:')
        self.source_input = QLineEdit()
        self.source_button = QPushButton('Browse')
        self.source_button.clicked.connect(self.browse_source)
        
        # Backup Directory Elements
        self.backup_label = QLabel('Backup Directory:')
        self.backup_input = QLineEdit()
        self.backup_button = QPushButton('Browse')
        self.backup_button.clicked.connect(self.browse_backup)

        # Email Settings Elements - Labels & Inputs
        self.email_label = QLabel('Sender Email:')
        self.email_input = QLineEdit()

        self.receiver_label = QLabel('Receiver Email:')
        self.receiver_input = QLineEdit()

        self.smtp_label = QLabel('SMTP Server:')
        self.smtp_input = QLineEdit()

        self.port_label = QLabel('SMTP Port:')
        self.port_input = QLineEdit()

        self.username_label = QLabel('Email Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Email Password:')
        self.password_input = QLineEdit()

        # Backup Time Elements
        self.time_label = QLabel('Backup Time:')
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(2, 0))

        # Save & Run Backup Button
        self.save_button = QPushButton('Save and Run Backup')
        self.save_button.clicked.connect(self.save_settings)

        # Add Widgets to the Layout
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_input)
        layout.addWidget(self.source_button)

        layout.addWidget(self.backup_label)
        layout.addWidget(self.backup_input)
        layout.addWidget(self.backup_button)

        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        layout.addWidget(self.receiver_label)
        layout.addWidget(self.receiver_input)

        layout.addWidget(self.smtp_label)
        layout.addWidget(self.smtp_input)

        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)

        layout.addWidget(self.save_button)

        self.setLayout(layout) # Set Layout for the Main Window

    # Browse Source Directory to Select Folder
    def browse_source(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if dir_path:
            self.source_input.setText(dir_path)

    # Browse Backup Directory to Select Folder
    def browse_backup(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Backup Directory')
        if dir_path:
            self.backup_input.setText(dir_path)

    # Save Settings to a File & Start the Backup Script
    def save_settings(self):
        # Collect all the settings from the input fields
        settings = {
            'SOURCE_DIR': self.source_input.text(),
            'BACKUP_DIR': self.backup_input.text(),
            'EMAIL_SENDER': self.email_input.text(),
            'EMAIL_RECEIVER': self.receiver_input.text(),
            'EMAIL_SMTP_SERVER': self.smtp_input.text(),
            'EMAIL_SMTP_PORT': self.port_input.text(),
            'EMAIL_USERNAME': self.username_input.text(),
            'EMAIL_PASSWORD': self.password_input.text(),
            'BACKUP_TIME': self.time_input.time().toString("HH:mm")
        }

        # Write the settings to a file 'settings.ini'
        with open('settings.ini', 'w') as f:
            for key, value in settings.items():
                f.write(f"{key}={value}\n")

        # Show a message box to confirm that the settings have been saved
        QMessageBox.information(self, 'Settings Saved', 'Settings have been saved successfully!')

        run_backup_script() # Start the Backup Script

# Read the settings from the saved file & start the backup script
def run_backup_script():
    settings = {}
    with open('settings.ini', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            settings[key] = value

    # Load the settings into global variables into backup script
    global SOURCE_DIR, BACKUP_DIR, EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_SUBJECT, EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, BACKUP_TIME
    SOURCE_DIR = settings['SOURCE_DIR']
    BACKUP_DIR = settings['BACKUP_DIR']
    EMAIL_SENDER = settings['EMAIL_SENDER']
    EMAIL_RECEIVER = settings['EMAIL_RECEIVER']
    EMAIL_SUBJECT = 'Backup Report'
    EMAIL_SMTP_SERVER = settings['EMAIL_SMTP_SERVER']
    EMAIL_SMTP_PORT = int(settings['EMAIL_SMTP_PORT'])
    EMAIL_USERNAME = settings['EMAIL_USERNAME']
    EMAIL_PASSWORD = settings['EMAIL_PASSWORD']
    BACKUP_TIME = settings['BACKUP_TIME']

    # Schedule the Backup Script to Run Daily at the Specified Time
    schedule.every().day.at(BACKUP_TIME).do(backup_files)

    while True:
        schedule.run_pending()
        time.sleep(1)

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

if __name__ == '__main__':
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    
    app = QApplication(sys.argv)
    ex = BackupApp()
    ex.show()
    sys.exit(app.exec())
