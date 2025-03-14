@echo off
echo ==========================================
echo          CHAY UNG DUNG FLASK
echo ==========================================

:: Kích hoạt môi trường ảo và chạy ứng dụng Flask
call venv\Scripts\activate.bat
python -m flask --app flaskr run --debug

pause 