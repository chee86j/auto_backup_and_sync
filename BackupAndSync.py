import os
import shutil
import logging
import schedule
import time

SOURCE_DIR = 'C:\Users\Admin\Documents\Scanned Documents' #Replace with your source directory
BACKUP_DIR = 'D:\Users\Admin\Documents\Backup Scanned Documents' # Replace with your backup directory

def get_all_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

# Backup Function
def backup_files():
    source_files = get_all_files(SOURCE_DIR)
    backup_files = get_all_files(BACKUP_DIR)
    
    # Create Dictionary w/Relative Path as Key and Full Path as Value for Quick Lookup
    backup_files_dict = {os.path.relpath(file, BACKUP_DIR): file for file in backup_files}
    
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
            logging.info(f"Backed up: {file} -> {backup_file_path}")
            
# Scheduling
def run_scheduler():
    schedule.every().day.at("02:00").do(backup_files) # Backup Files Daily at 2:00 AM
    
    while True: # Condition to keep the script running
        schedule.run_pending() # Check if any scheduled tasks are due
        time.sleep(1) # Sleep for 1 second before checking again
        
if __name__ == '__main__':
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    run_scheduler()