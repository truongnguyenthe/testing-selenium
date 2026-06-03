# Selenium Testing Project

## Giới thiệu

Dự án kiểm thử tự động sử dụng **Selenium WebDriver**, **Pytest** và **Pytest HTML Report** để kiểm thử các chức năng của website:

**Website:** https://www.saucedemo.com

Mục tiêu của dự án là thực hiện kiểm thử tự động các chức năng quan trọng của hệ thống, bao gồm đăng nhập, quản lý giỏ hàng, thanh toán, bảo vệ truy cập và đánh giá hiệu năng.

---

## Công nghệ sử dụng

* Python
* Selenium WebDriver
* Pytest
* Pytest HTML Report
* WebDriver Manager

---

## Cấu trúc dự án

```text
TestingSelenium/
│
├── tests/
│   ├── test_login.py
│   ├── test_cart.py
│   ├── test_inventory.py
│   ├── test_checkout.py
│   ├── test_menu_logout.py
│   ├── test_access_protection.py
│   └── test_performance.py
│
├── conftest.py
├── utils.py
├── run_all.py
├── requirements.txt
├── report.html
└── README.md
```

---

## Cài đặt môi trường

### 1. Clone repository

```bash
git clone https://github.com/truongnguyenthe/testing-selenium.git
cd testing-selenium
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Lệnh trên sẽ tự động cài đặt:

* Selenium
* Pytest
* Pytest HTML
* WebDriver Manager

WebDriver Manager sẽ tự động tải ChromeDriver phù hợp với phiên bản Chrome đang sử dụng.

---

## Chạy toàn bộ test

### Cách 1

```bash
python run_all.py
```

### Cách 2

```bash
pytest tests/ --html=report.html --self-contained-html -v
```

Sau khi chạy xong, mở file:

```text
report.html
```

để xem báo cáo kết quả kiểm thử.

---

## Chạy từng test riêng lẻ

### Test đăng nhập

```bash
pytest tests/test_login.py -v
```

### Test giỏ hàng

```bash
pytest tests/test_cart.py -v
```

### Test sắp xếp sản phẩm

```bash
pytest tests/test_inventory.py -v
```

### Test thanh toán

```bash
pytest tests/test_checkout.py -v
```

### Test menu và đăng xuất

```bash
pytest tests/test_menu_logout.py -v
```

### Test bảo vệ truy cập

```bash
pytest tests/test_access_protection.py -v
```

### Test hiệu năng

```bash
pytest tests/test_performance.py -v
```

---

## Các chức năng được kiểm thử

| STT | Chức năng                    |
| --- | ---------------------------- |
| 1   | Đăng nhập hệ thống           |
| 2   | Thêm sản phẩm vào giỏ hàng   |
| 3   | Sắp xếp danh sách sản phẩm   |
| 4   | Quy trình thanh toán         |
| 5   | Menu và đăng xuất            |
| 6   | Bảo vệ truy cập trái phép    |
| 7   | Đánh giá hiệu năng tải trang |

---

## Báo cáo kiểm thử

Dự án sử dụng:

```bash
pytest-html
```

để sinh báo cáo HTML trực quan.

Ví dụ:

```bash
pytest tests/ --html=report.html --self-contained-html
```

---

## Một số lỗi thường gặp

### Lỗi không tìm thấy Selenium

```text
No module named selenium
```

Khắc phục:

```bash
pip install -r requirements.txt
```

---

### ChromeDriver tải lần đầu chậm

Lần chạy đầu tiên có thể mất nhiều thời gian do WebDriver Manager đang tải ChromeDriver phù hợp.

---

### Chrome bị crash

Có thể chạy chế độ Headless bằng cách thêm:

```python
--headless
```

vào phần cấu hình Chrome Options trong file `utils.py`.

---

## Tác giả

**Trương Nguyễn Thế**

Sinh viên Công nghệ Thông tin – Đại học Phenikaa

Môn học: Software Testing
