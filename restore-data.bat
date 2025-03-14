@echo off
echo =================================================
echo            KHOI PHUC DU LIEU TU GIT
echo =================================================

:: Kiểm tra xem thư mục data có tồn tại không
if not exist data (
    echo Khong tim thay thu muc data!
    echo Vui long dam bao ban da clone toan bo repository.
    goto :end
)

:: Kiểm tra xem có file database backup không
if not exist data\flaskr.sqlite.backup (
    echo Khong tim thay file database backup!
    goto :end
)

:: Tạo thư mục instance nếu chưa tồn tại
if not exist instance mkdir instance

:: Khôi phục database
echo Dang khoi phuc database...
copy data\flaskr.sqlite.backup instance\flaskr.sqlite

:: Tạo thư mục cho hình ảnh
if not exist flaskr\static\images mkdir flaskr\static\images

:: Khôi phục hình ảnh
echo Dang khoi phuc hinh anh...
if exist data\images (
    xcopy /E /Y data\images flaskr\static\images\
)

echo Da hoan tat khoi phuc du lieu!
echo.
echo Bay gio ban co the chay ung dung voi du lieu day du.

:end
pause 