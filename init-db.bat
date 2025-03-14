@echo off
echo =================================================
echo            KHOI TAO CO SO DU LIEU
echo =================================================

:: Kich hoat moi truong ao neu chua duoc kich hoat
if not defined VIRTUAL_ENV (
    call venv\Scripts\activate
)

:: Dat bien moi truong Flask
set FLASK_APP=flaskr

:: Xác nhận từ người dùng
echo CANH BAO: Hanh dong nay se xoa toan bo du lieu hien tai!
echo.
set /p confirm=Ban co chac chan muon khoi tao lai co so du lieu? (y/n): 

if /i "%confirm%"=="y" (
    flask --app flaskr init-db
    echo.
    echo Da khoi tao lai co so du lieu.
    echo Tai khoan mac dinh: admin / trungtada123
) else (
    echo.
    echo Huy bo khoi tao co so du lieu.
)

pause 