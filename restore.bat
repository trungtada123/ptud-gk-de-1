@echo off
echo ================================================
echo              KHÔI PHỤC DATABASE
echo ================================================

:: Kiểm tra xem thư mục backups có tồn tại không
if not exist backups (
    echo Không tìm thấy thư mục backups!
    echo Vui lòng đảm bảo bạn đã thực hiện sao lưu trước đó.
    goto :end
)

:: Liệt kê các file sao lưu
echo Các bản sao lưu hiện có:
echo ------------------------------------------------
set COUNT=0
for %%i in (backups\*.sqlite) do (
    set /a COUNT+=1
    echo !COUNT!. %%~ni %%~ti
)

if %COUNT%==0 (
    echo Không tìm thấy bản sao lưu nào!
    goto :end
)

:: Yêu cầu người dùng nhập tên file sao lưu
echo:
echo Nhập tên đầy đủ của file sao lưu muốn khôi phục:
echo Ví dụ: flaskr_20240314_120000
set /p BACKUP_NAME="Tên file: "

if not exist backups\%BACKUP_NAME%.sqlite (
    echo File không tồn tại: %BACKUP_NAME%.sqlite
    goto :end
)

:: Kiểm tra xem ứng dụng có đang chạy không
echo Đảm bảo ứng dụng Flask đã dừng trước khi khôi phục.
set /p CONTINUE="Tiếp tục khôi phục? (y/N): "
if /i not "%CONTINUE%"=="y" goto :end

:: Tạo bản sao lưu của database hiện tại (nếu có)
if exist instance\flaskr.sqlite (
    echo Tạo bản sao lưu của database hiện tại...
    set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set TIMESTAMP=%TIMESTAMP: =0%
    copy instance\flaskr.sqlite "backups\flaskr_current_%TIMESTAMP%.sqlite"
)

:: Khôi phục từ bản sao lưu
echo Đang khôi phục database từ %BACKUP_NAME%.sqlite...
copy "backups\%BACKUP_NAME%.sqlite" instance\flaskr.sqlite

echo:
echo Khôi phục hoàn tất!

:end
pause 