@echo off
echo =================================================
echo            KHÔI PHỤC DỮ LIỆU TỪ GIT
echo =================================================

:: Kiểm tra xem thư mục data có tồn tại không
if not exist data (
    echo Không tìm thấy thư mục data!
    echo Vui lòng đảm bảo bạn đã clone toàn bộ repository.
    goto :end
)

:: Kiểm tra xem có file database backup không
if not exist data\flaskr.sqlite.backup (
    echo Không tìm thấy file database backup!
    goto :end
)

:: Tạo thư mục instance nếu chưa tồn tại
if not exist instance mkdir instance

:: Khôi phục database
echo Đang khôi phục database...
copy data\flaskr.sqlite.backup instance\flaskr.sqlite

:: Tạo thư mục cho hình ảnh
if not exist flaskr\static\images mkdir flaskr\static\images

:: Khôi phục hình ảnh
echo Đang khôi phục hình ảnh...
if exist data\images (
    xcopy /E /Y data\images flaskr\static\images\
)

echo Đã hoàn tất khôi phục dữ liệu!
echo.
echo Bây giờ bạn có thể chạy ứng dụng với dữ liệu đầy đủ.

:end
pause 