## Bước 1:install python 3.8

https://www.python.org/downloads/release/python-3810/
chọn phiên bản và cài
=> nhớ tích vào thêm environment biến trong khi cài đặt

sau đó cài gói:
pip install selenium
pip install webdriver_manager

## Bước 2: down chromedriver để điều khiển web
check phiên bản chrome hiện tại:
vào chrome gõ : chrome://version/ => DÒNG ĐẦU TIÊN CHO THẤY PHIÊN BẢN CHROME HIỆN TẠI

Giả sử là : 132.0.6834.111

Thì thay phiên bản vào đường dẫn sau:

- Đối với window:

https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.111/win64/chromedriver-win64.zip

- đối với Linux:
https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.111/linux64/chromedriver-linux64.zip


Giải nén file zip vừa down

## Bước 3: Download code
https://github.com/bibo-home/bibo-one 
Có thể dùng git clone hoặc download zip

## Bước 4: copy file chromedriver(linux) hoặc chromedriver.exe(window) (download ở bước 2) vào cùng thư mục code (download ở bước 3)

## Bước 5: Chỉnh các tham số sau trong code cho phù hợp của bạn

```python
# config.json
"profile_path_windows": "C:\\Users\\nguye\\AppData\\Local\\Google\\Chrome\\User Data", # đường dẫn tới Chrome User Data- đối với windows
"profile_directory" : "Profile 3",      # Check thứ tự profile
"chrome_profile_path": "/home/{username}/.config/google-chrome/",           # đường dẫn đối với linux
"passMetamask":"",      # password đăng nhập metamask
```

```python
# main.py
book = 1             # Đang hỗ trợ cho symmetric quest book 1 và book 3
```

## Bước 6: cd vào thư mục code và run câu lệnh sau

#### Cho window

```bash
python main.py
```

#### Cho Linux

```bash
python3 main.py
```

### Statistic

Quest book 1 - Symmetric swap USDT/WTLOS: 1000 lan = 80 TLOS
Quest book 2 - Swapsicle swap WTLOS/SLUS: 1000 lan = 120 TLOS
Quest book 2 - Symmetric swap STLOS/TLOS: 1000 lan = 80 TLOS