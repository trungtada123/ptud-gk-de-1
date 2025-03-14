@echo off
echo ==================================================
echo       THIẾT LẬP ỨNG DỤNG FLASK BLOG APP
echo ==================================================

echo Tạo môi trường ảo...
python -m venv venv

echo Kích hoạt môi trường ảo...
call venv\Scripts\activate

echo Cài đặt các thư viện cần thiết...
pip install -r requirements.txt

echo Cài đặt Flask...
pip install flask

echo Cấu hình biến môi trường cho Flask...
set FLASK_APP=flaskr

:: Kiểm tra xem file database đã tồn tại chưa
if exist instance\flaskr.sqlite (
    echo:
    echo ======== CẢNH BÁO ========
    echo Database đã tồn tại (instance\flaskr.sqlite)
    echo Khởi tạo lại database sẽ xóa tất cả dữ liệu hiện có.
    echo:
    set /p INIT_DB="Ban co muon khoi tao lai database khong? (y/N): "
    if /i "%INIT_DB%"=="y" (
        echo Đang khởi tạo lại database...
        flask --app flaskr init-db
    ) else (
        echo Giữ nguyên database hiện tại...
    )
) else (
    echo Database chưa tồn tại, đang khởi tạo...
    flask --app flaskr init-db
)

echo:
echo ====================================================
echo Thiết lập hoàn tất!
echo:
echo Chạy ứng dụng Flask...
echo:
flask --app flaskr run --debug
