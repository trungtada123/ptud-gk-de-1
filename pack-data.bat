@echo off
echo =================================================
echo            DONG GOI DU LIEU CHO GIT
echo =================================================

:: Tạo thư mục data nếu chưa tồn tại
if not exist data mkdir data

:: Sao lưu database
echo Dang sao luu database...
copy instance\flaskr.sqlite data\flaskr.sqlite.backup

:: Tạo thư mục cho hình ảnh
if not exist data\images mkdir data\images

:: Sao lưu hình ảnh
echo Dang sao luu hinh anh...
if exist flaskr\static\images (
    xcopy /E /Y flaskr\static\images data\images\
)

echo Da hoan tat dong goi du lieu!
echo.
echo Bay gio ban co the commit thu muc "data" len GitHub.
pause 