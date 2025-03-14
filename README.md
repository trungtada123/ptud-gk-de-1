# Thông tin cá nhân:
## Mã số sinh viên: 22719231
## Họ Tên: Nguyễn Chí Trung

# Ứng dụng Flask Blog

Ứng dụng blog đơn giản được xây dựng bằng Python Flask với các tính năng:
- Đăng bài viết với văn bản, hình ảnh và liên kết
- Theo dõi bài viết yêu thích
- Phân quyền admin và người dùng thường
- Quản lý người dùng và bài viết

## Cài đặt và chạy ứng dụng

### Cài đặt mới (sau khi clone từ GitHub)

1. Clone repository từ GitHub:
   ```
   git clone https://github.com/trungtada123/ptud-gk-de-1
   ```
2. Di chuyển đến thư mục chính
   ```
    cd ptud-gk-de-1
   ```
3. Chạy script cài đặt:
   ```
    .\setup.bat
   ```
   Script này sẽ:
   - Tạo môi trường ảo Python
   - Cài đặt thư viện Flask

4. Khôi phục dữ liệu (bài viết và hình ảnh):
     ``` 
   .\restore-data.bat
      ```
   Script này sẽ:
   - Khôi phục cơ sở dữ liệu từ bản sao lưu
   - Khôi phục hình ảnh từ thư mục data

5. Chạy ứng dụng:
   ```
   .\run.bat
   ```
### Sử dụng ứng dụng

Sau khi khởi động, ứng dụng sẽ chạy tại:
- URL: http://localhost:5000
- Tài khoản / Mật khẩu Admin ( mặc định ): admin / trungtada123

## Quản lý dữ liệu

### LƯU Ý QUAN TRỌNG CHO NGƯỜI ĐÓNG GÓP/PHÁT TRIỂN

Khi bạn thêm bài viết mới và muốn đẩy lên GitHub để người khác có thể sử dụng, hãy làm theo các bước sau:

1. **Sao lưu dữ liệu mới trước khi đẩy lên GitHub**:
   ```
   .\pack-data.bat
   ```
   Script này sẽ:
   - Tạo thư mục `data` (nếu chưa có)
   - Sao lưu cơ sở dữ liệu vào `data/flaskr.sqlite.backup`
   - Sao lưu hình ảnh vào `data/images/`

2. **Đẩy lên GitHub để chia sẻ với mọi người**:
   ```
   git add .
   git commit -m "Cập nhật dữ liệu ngày XX/XX/XXXX"
   git push
   ```

### LƯU Ý QUAN TRỌNG CHO NGƯỜI SỬ DỤNG

Khi clone repository về, để lấy được dữ liệu bài viết đã có:

1. **Chạy script cài đặt**:
   ```
   .\setup.bat
   ```

2. **Khôi phục dữ liệu**:
   ```
   .\restore-data.bat
   ```
   
3. **Chạy ứng dụng**:
   ```
   .\run.bat
   ```

## Các script hỗ trợ

- **setup.bat**: Cài đặt môi trường và thư viện
- **restore-data.bat**: Khôi phục dữ liệu từ thư mục data
- **pack-data.bat**: Sao lưu dữ liệu vào thư mục data (chạy trước khi push)
- **init-db.bat**: Khởi tạo cơ sở dữ liệu mới (xóa dữ liệu cũ)
- **run.bat**: Chạy ứng dụng

## Cấu trúc thư mục

```
flask-tiny-app/
├── data/                  # Thư mục chứa dữ liệu sao lưu (đẩy lên GitHub)
│   ├── flaskr.sqlite.backup  # Bản sao lưu cơ sở dữ liệu
│   └── images/            # Bản sao lưu hình ảnh
├── flaskr/                # Mã nguồn ứng dụng
│   ├── static/            # Tài nguyên tĩnh (CSS, JS, hình ảnh)
│   ├── templates/         # Các file HTML
│   ├── __init__.py        # Điểm khởi đầu ứng dụng
│   ├── auth.py            # Xử lý xác thực
│   ├── blog.py            # Xử lý blog
│   ├── db.py              # Kết nối cơ sở dữ liệu
│   └── schema.sql         # Schema cơ sở dữ liệu
├── instance/              # Dữ liệu instance (không đẩy lên GitHub)
│   └── flaskr.sqlite      # Cơ sở dữ liệu SQLite
├── venv/                  # Môi trường ảo Python (không đẩy lên GitHub)
├── setup.bat              # Script cài đặt
├── restore-data.bat       # Script khôi phục dữ liệu
├── pack-data.bat          # Script sao lưu dữ liệu
├── init-db.bat            # Script khởi tạo cơ sở dữ liệu
├── run.bat                # Script chạy ứng dụng
├── requirements.txt       # Danh sách thư viện Python
└── README.md              # File này
```

## Tài khoản admin ( Mặc Định )

- **Username**: admin
- **Password**: trungtada123

## Quy trình làm việc đề xuất

### Người phát triển/đóng góp:

1. Phát triển, thêm bài viết mới
2. Chạy `pack-data.bat` để sao lưu dữ liệu
3. Commit và push lên GitHub

### Người sử dụng:

1. Clone repository
2. Chạy `setup.bat` để cài đặt
3. Chạy `restore-data.bat` để khôi phục dữ liệu
4. Chạy `run.bat` để khởi động ứng dụng

## Giải quyết sự cố

- **Lỗi không tìm thấy database**: Chạy `restore-data.bat` hoặc `init-db.bat`
- **Lỗi thiếu thư viện**: Chạy `pip install -r requirements.txt`
- **Lỗi không hiển thị hình ảnh**: Kiểm tra thư mục `flaskr/static/images`
