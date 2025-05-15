from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os
# Dọn dẹp: Kill tất cả tiến trình chrome.exe
os.system("taskkill /f /im chrome.exe")
options = Options()

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

options.add_argument(r"--user-data-dir=C:\Users\hieunk\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Default")  
#options.add_argument('--headless')  # Xóa nếu bạn muốn xem trình duyệt thật
# Gỡ automation flags (hạn chế bị detect là bot)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument(f"user-agent={user_agent}")
# Bật log performance (nếu cần bắt header request)
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Khởi tạo driver tự động quản lý ChromeDriver đúng version
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Mở web
print("Mở X.com...")
driver.get("https://x.com/search?q=Du%20l%E1%BB%8Bch&src=typed_query&f=live")

# Đợi vài giây để các request chạy xong
time.sleep(5)

# Lấy toàn bộ log từ CDP
logs = driver.get_log("performance")

# Lọc các API request bạn quan tâm (ví dụ: jot/client_event.json)
for entry in logs:
    message = json.loads(entry["message"])["message"]
    if message["method"] == "Network.requestWillBeSent":
        url = message["params"]["request"]["url"]
        if "https://x.com/i/api/graphql/zrQl4v8IM8Now-qkpHmDLQ/SearchTimeline" in url:
            headers = message["params"]["request"]["headers"]
            print(f"\n🔍 Request to: {url}")
            for k, v in headers.items():
                print(f"{k}: {v}")

driver.quit()
