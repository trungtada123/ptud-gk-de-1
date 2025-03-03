# Sử dụng Python 3.10 làm base image
FROM python:3.10

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ project vào container
COPY . /app

# Cài đặt các package cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Chạy Flask (giả sử file chính là `flaskr`)
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0"]
