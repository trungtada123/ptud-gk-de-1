@echo off
echo Đang sao lưu database...

:: Tạo thư mục backups nếu chưa tồn tại
if not exist backups mkdir backups

:: Tạo tên file backup với timestamp
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_FILE=backups\flaskr_%TIMESTAMP%.sqlite

:: Sao chép file database
copy instance\flaskr.sqlite "%BACKUP_FILE%"

echo Sao lưu thành công tại: %BACKUP_FILE%
pause 