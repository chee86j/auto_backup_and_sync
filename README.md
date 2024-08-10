Python Automated Backup & Sync Script w/GUI
Welcome to the Automated Backup & Sync Script!
This script is made to automate backing up your files from a specified source directory to a backup directory & sends email notifications w/ a detailed backup Report upon completion.

## Key Features

1. **Automated File Backup**: Automatically backs up new & modified files from the source directory to the backup directory.
2. **Email Notifications**: Sends an email notification upon successful backup or in case of an error.
3. **Detailed Backup Report**: Generates & Emails a Report listing all backed-up files.
4. **Daily Scheduling**: Automatically runs the backup process daily at a specified time.
5. **Graphical User Interface (GUI)**: A user-friendly interface to configure backup settings, schedule, and email notifications.

## Technologies & Libraries

1. `os` for Interacting w/ the Operating System.
2. `shutil` for High-level File Operations like Moving & Copying Files.
3. `logging` for Error Logging & Debugging.
4. `schedule` for Scheduling Tasks.
5. `smtplib` & `email.mime` for Sending Email Notifications.
6. `PySide6` for Creating the User Interface.

## Prerequisites

Before running the script, ensure you have the following installed:

1. **Python**: Ensure Python 3.x is installed on your system. [Download Python](https://www.python.org/downloads/).
2. **Install Required Libraries**: Install the necessary libraries using `pip`:
   ```bash
   pip install schedule
   pip install PySide6
   ```

## Running The Script

To execute the script, run the command `python3 BackupAndSync.py` or `python BackupAndSync.py` in the terminal once you have navigated to the directory containing `BackupAndSync.py`
