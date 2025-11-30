@echo off
REM Chạy im lặng, không hiện thông báo

REM Thư mục Startup của người dùng hiện tại
set "startupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Thư mục chứa các file exe cần copy
set "sourceFolder=%~dp0build-exe"

REM Lặp qua tất cả file .exe trong thư mục build-exe
for %%F in ("%sourceFolder%\*.exe") do (
    if exist "%%F" (
        copy /Y "%%F" "%startupFolder%\%%~nxF" >nul 2>&1
    )
)

exit
