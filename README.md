# Flask Tiny App

## Thông tin:
- Họ tên: Nguyễn Chí Trung
- Mã sinh viên: 22719231


## Mô tả
Ứng dụng web quản lý bài viết đơn giản bằng Flask bao gồm 2 tác nhân chính là Admin và User. Trong đó Admin có quyền block, unblock, reset mật khẩu cho người dùng. Các bài viết được phân trang theo số lượng bài: 10 bài / trang,....

## Hướng dẫn cài đặt và chạy
```bash
Bước 1: Clone về máy
git clone https://github.com/trungtada123/flask-tiny-app.git

Bước 2: Di chuyển đến thư mục app
cd flask-tiny-app


Bước 3: Có thể dùng lệnh terminal để khởi chạy tự động:
.\install.bat

Hoặc thực hiệ thủ công như sau:

Bước 3: Tạo môi trường ảo
python -m venv venv # Tạo môi trường ảo
venv\Scripts\activate trên Windows

pip install -r requirements.txt
Bước 4: Cài đặt Flask bằng cmd: pip install flask

Bước 5: Chỉ định thư mục để khởi chạy flask app 
export FLASK_APP=flaskr  # set FLASK_APP=flaskr trên Windows

Bước 6: Khởi tạo database
flask --app flaskr init-db

Bước 7: Run app
flask --app flaskr run --debug



Hoặc cũng có thể chạy tự động bằng docker
B1: docker build -t flask-tiny-app .
B2: docker run -p 5000:5000 flask-tiny-app
