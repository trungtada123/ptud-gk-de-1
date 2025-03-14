@echo off
echo =================================================
echo            ĐÓNG GÓI DỮ LIỆU CHO GIT
echo =================================================

:: Tạo thư mục data nếu chưa tồn tại
if not exist data mkdir data

:: Sao lưu database
echo Đang sao lưu database...
copy instance\flaskr.sqlite data\flaskr.sqlite.backup

:: Tạo thư mục cho hình ảnh
if not exist data\images mkdir data\images

:: Sao lưu hình ảnh
echo Đang sao lưu hình ảnh...
if exist flaskr\static\images (
    xcopy /E /Y flaskr\static\images data\images\
)

echo Đã hoàn tất đóng gói dữ liệu!
echo.
echo Bây giờ bạn có thể commit thư mục "data" lên GitHub.
pause 