@echo off
echo ==========================================
echo          CHAY UNG DUNG FLASK
echo ==========================================

:: Kích hoạt môi trường ảo và chạy ứng dụng Flask
call venv\Scripts\activate.bat
flask --app flaskr run --debug

pause 