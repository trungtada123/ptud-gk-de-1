@echo off
echo ==========================================
echo           CAI DAT UNG DUNG FLASK
echo ==========================================

:: Tao moi truong ao
python -m venv venv

:: Kich hoat moi truong ao
call venv\Scripts\activate

:: Cai dat cac thu vien
pip install flask

echo Cai dat hoan tat!
echo.
echo De khoi phuc du lieu, hay chay: restore-data.bat
echo De chay ung dung, hay chay: run.bat
echo.
pause 