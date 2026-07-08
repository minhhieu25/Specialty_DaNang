# Specialty DaNang Project

Dự án website đặc sản Đà Nẵng được xây dựng bằng Django.

## Yêu cầu hệ thống
- Python 3.x
- Hệ quản trị cơ sở dữ liệu SQL Server (Project đang cấu hình kết nối SQL Server)
- Git

## Hướng dẫn cài đặt và chạy project

### Bước 1: Clone project về máy
Mở terminal (hoặc Command Prompt/PowerShell) và chạy lệnh sau:
```bash
git clone <đường_dẫn_repository_của_bạn>
cd Specialty_DaNang
```

### Bước 2: Thiết lập môi trường ảo (Virtual Environment)
Việc sử dụng môi trường ảo giúp tách biệt các thư viện của project này với các project khác trên máy bạn.

**Tạo môi trường ảo (chỉ làm 1 lần đầu tiên):**
```bash
python -m venv venv
```

**Kích hoạt môi trường ảo:**
- **Trên Windows** (Command Prompt hoặc PowerShell):
  ```bash
  .\venv\Scripts\activate
  ```
- **Trên MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```
*(Dấu hiệu nhận biết thành công là bạn sẽ thấy chữ `(venv)` xuất hiện ở đầu dòng lệnh).*

### Bước 3: Cài đặt các thư viện phụ thuộc
Đảm bảo bạn đã kích hoạt môi trường ảo, sau đó chạy lệnh sau để cài đặt các package từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình file biến môi trường (.env)
Project sử dụng file `.env` để lưu trữ các cấu hình bảo mật. Do file này không được push lên Github, bạn cần tự tạo nó.

Tạo một file có tên là `.env` ở thư mục gốc của project (nằm ngang hàng với file `manage.py`) và copy nội dung sau vào (bạn hãy thay đổi thông tin `DB_PASSWORD` và các thông tin khác cho khớp với cấu hình SQL Server trên máy bạn):

```env
DEBUG = True
SECRET_KEY = django-insecure-c-1gvswxdkojqr+b#je461io40+e-k7t2y41gz$wld&t#fbk5d
DB_NAME = Specialty_DaNang_DB
DB_USER = sa
DB_PASSWORD = 123456789
DB_HOST = 127.0.0.1
DB_PORT = 1433
```
*Lưu ý: Hãy đảm bảo bạn đã tạo sẵn một Database trống có tên `Specialty_DaNang_DB` trong SQL Server của bạn.*

### Bước 5: Chạy Migrate (Tạo bảng trong Database)
Chạy lệnh sau để Django tạo các bảng cần thiết vào trong database:
```bash
python manage.py migrate
```

### Bước 6: Thêm dữ liệu mẫu (Seed Data - Tùy chọn)
Nếu bạn muốn có sẵn dữ liệu mẫu (bài viết, sản phẩm...) để test giao diện, hãy chạy các script sau:
```bash
python populate_db.py
python seed_blog.py
```

### Bước 7: Khởi động Server
Cuối cùng, chạy lệnh sau để bật server:
```bash
python manage.py runserver
```

Mở trình duyệt và truy cập vào địa chỉ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---
**💡 Lưu ý quan trọng:** 
- Mỗi khi bạn tắt terminal và mở lại để code hoặc chạy project, hãy luôn nhớ thực hiện lại lệnh **kích hoạt môi trường ảo** (Bước 2) trước khi chạy lệnh `python manage.py ...` nhé!
