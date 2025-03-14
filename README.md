# Flask Blog App

Ứng dụng blog đơn giản được xây dựng bằng Flask.

## Cài đặt

### Cài đặt tự động

1. Chạy file `install.bat` để cài đặt ứng dụng
2. Script sẽ tự động:
   - Tạo môi trường ảo Python
   - Cài đặt các thư viện cần thiết
   - Kiểm tra và hỏi bạn có muốn khởi tạo database mới hay không
   - Khởi động ứng dụng ở chế độ debug

### Cài đặt thủ công

1. Tạo môi trường ảo Python:
   ```
   python -m venv venv
   ```

2. Kích hoạt môi trường ảo:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Cài đặt các thư viện:
   ```
   pip install -r requirements.txt
   pip install flask
   ```

4. Khởi tạo database (chỉ khi cần tạo mới):
   ```
   flask --app flaskr init-db
   ```

5. Chạy ứng dụng:
   ```
   flask --app flaskr run --debug
   ```

## Quản lý dữ liệu

### Sao lưu dữ liệu

Để sao lưu dữ liệu hiện tại:

1. Đảm bảo ứng dụng không đang chạy
2. Chạy file `backup.bat`
3. File sao lưu sẽ được lưu trong thư mục `backups/` với tên bao gồm ngày giờ

### Khôi phục dữ liệu

Để khôi phục từ bản sao lưu:

1. Đảm bảo ứng dụng không đang chạy
2. Chạy file `restore.bat`
3. Làm theo hướng dẫn để chọn bản sao lưu cần khôi phục

### Triển khai trên máy mới với dữ liệu cũ

1. Sao lưu file `instance/flaskr.sqlite` từ máy cũ
2. Cài đặt ứng dụng trên máy mới bằng `install.bat` (chọn KHÔNG khởi tạo database mới)
3. Sau khi cài đặt, sao chép file database đã sao lưu vào thư mục `instance/` của máy mới

## Tài khoản mặc định

- Tên đăng nhập: `admin`
- Mật khẩu: `trungtada123`
