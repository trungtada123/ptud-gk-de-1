@echo off
echo ==========================================
echo           CHAY UNG DUNG FLASK
echo ==========================================

:: Kich hoat moi truong ao neu chua duoc kich hoat
if not defined VIRTUAL_ENV (
    call venv\Scripts\activate
)

:: Dat bien moi truong Flask
set FLASK_APP=flaskr

:: Chay ung dung
flask --app flaskr run --debug

pause 