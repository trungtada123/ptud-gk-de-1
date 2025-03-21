@echo off
echo ==========================================
echo ==========================================

:: Tạo môi trường ảo mới nếu chưa tồn tại
if not exist venv (
    echo Dang tao moi truong ao moi...
    python -m venv venv
)

:: Kích hoạt môi trường ảo và cài đặt Flask
echo Dang cai dat Flask...
call venv\Scripts\activate.bat
pip install flask

echo.
echo Cai dat hoan tat!
echo.
echo De khoi phuc du lieu, hay chay: restore-data.bat
echo De chay ung dung, hay chay: run.bat
echo.
pause 