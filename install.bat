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

:: Kiểm tra xem có dữ liệu backup từ Git không
if exist data\flaskr.sqlite.backup (
    echo:
    echo Phát hiện dữ liệu backup từ Git.
    set /p RESTORE_DATA="Bạn có muốn khôi phục dữ liệu từ Git không? (Y/n): "
    if not /i "%RESTORE_DATA%"=="n" (
        echo Đang khôi phục dữ liệu từ Git...
        
        :: Tạo thư mục instance nếu chưa tồn tại
        if not exist instance mkdir instance
        
        :: Khôi phục database
        copy data\flaskr.sqlite.backup instance\flaskr.sqlite
        
        :: Tạo thư mục cho hình ảnh
        if not exist flaskr\static\images mkdir flaskr\static\images
        
        :: Khôi phục hình ảnh
        if exist data\images (
            xcopy /E /Y data\images flaskr\static\images\
        )
        
        echo Đã khôi phục dữ liệu thành công!
    )
) else (
    :: Kiểm tra xem file database đã tồn tại chưa
    if exist instance\flaskr.sqlite (
        echo:
        echo ======== CẢNH BÁO ========
        echo Database đã tồn tại (instance\flaskr.sqlite)
        echo Khởi tạo lại database sẽ xóa tất cả dữ liệu hiện có.
        echo:
        set /p INIT_DB="Bạn có muốn khởi tạo lại database không? (y/N): "
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
)

echo:
echo ====================================================
echo Thiết lập hoàn tất!
echo:
echo Chạy ứng dụng Flask...
echo:
flask --app flaskr run --debug
