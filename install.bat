@echo off
echo ==================================================
echo       THIET LAP UNG DUNG FLASK BLOG APP
echo ==================================================

echo Tao moi truong ao...
python -m venv venv

echo Kich hoat moi truong ao...
call venv\Scripts\activate

echo Cai dat cac thu vien can thiet...
pip install -r requirements.txt

echo Cau hinh bien moi truong cho Flask...
set FLASK_APP=flaskr

:: Kiểm tra xem có dữ liệu backup từ Git không
if exist data\flaskr.sqlite.backup (
    echo:
    echo Phat hien du lieu backup tu Git.
    set /p RESTORE_DATA="Ban co muon khoi phuc du lieu tu Git khong? (Y/n): "
    if /i not "%RESTORE_DATA%"=="n" (
        echo Dang khoi phuc du lieu tu Git...
        
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
        
        echo Da khoi phuc du lieu thanh cong!
    )
) else (
    :: Kiểm tra xem file database đã tồn tại chưa
    if exist instance\flaskr.sqlite (
        echo:
        echo ======== CANH BAO ========
        echo Database da ton tai (instance\flaskr.sqlite)
        echo Khoi tao lai database se xoa tat ca du lieu hien co.
        echo:
        set /p INIT_DB="Ban co muon khoi tao lai database khong? (y/N): "
        if /i "%INIT_DB%"=="y" (
            echo Dang khoi tao lai database...
            flask --app flaskr init-db
        ) else (
            echo Giu nguyen database hien tai...
        )
    ) else (
        echo Database chua ton tai, dang khoi tao...
        flask --app flaskr init-db
    )
)

echo:
echo ====================================================
echo Thiet lap hoan tat!
echo:
echo Chay ung dung Flask...
echo:
flask --app flaskr run --debug
