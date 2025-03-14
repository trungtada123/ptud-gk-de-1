# Flask Blog App

Ứng dụng blog đơn giản được xây dựng bằng Flask.

## Cài đặt

### Cài đặt tự động

1. Chạy file `install.bat` để cài đặt ứng dụng
2. Script sẽ tự động:
   - Tạo môi trường ảo Python
   - Cài đặt các thư viện cần thiết
   - Phát hiện và khôi phục dữ liệu từ Git nếu có
   - Hoặc hỏi bạn có muốn khởi tạo database mới hay không
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

4. Khôi phục dữ liệu từ Git (nếu có):
   ```
   restore-data.bat
   ```
   
5. Hoặc khởi tạo database mới (nếu cần):
   ```
   flask --app flaskr init-db
   ```

6. Chạy ứng dụng:
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

### Đóng gói dữ liệu cho Git

Khi bạn muốn đưa dữ liệu và hình ảnh lên GitHub:

1. Chạy script `pack-data.bat`
2. Script sẽ sao chép database và hình ảnh vào thư mục `data/`
3. Commit thư mục `data/` lên GitHub

### Khôi phục dữ liệu từ Git

Khi người khác clone repository về:

1. Chạy `install.bat` - script sẽ tự động phát hiện và khôi phục dữ liệu
2. Hoặc chạy `restore-data.bat` để khôi phục dữ liệu một cách thủ công

## Tài khoản mặc định

- Tên đăng nhập: `admin`
- Mật khẩu: `trungtada123`
