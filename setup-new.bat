@echo off
echo ==========================================
echo          CAI DAT UNG DUNG FLASK
echo ==========================================

:: Tạo môi trường ảo mới nếu chưa tồn tại
if not exist venv (
    echo Dang tao moi truong ao moi...
    python -m venv venv
)

:: Kích hoạt môi trường ảo và cài đặt các gói từ requirements.txt
echo Dang cai dat cac goi can thiet...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Cai dat hoan tat!
echo.
echo De khoi phuc du lieu, hay chay: restore-data.bat
echo De chay ung dung, hay chay: run-new.bat
echo.
pause 