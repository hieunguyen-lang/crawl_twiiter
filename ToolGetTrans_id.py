from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os, time, json

# 1) Đóng mọi Chrome cũ
os.system("taskkill /f /im chrome.exe")
time.sleep(1)

# 2) Cấu hình ChromeOptions (bỏ desired_capabilities)
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Thêm các flag bạn cần
chrome_options.add_argument("--remote-allow-origins=*")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--remote-debugging-port=9222")

# Bật performance logging
chrome_options.set_capability(
    "goog:loggingPrefs",
    {"performance": "ALL"}
)

# 3) Khởi ChromeDriver chỉ với options
service = Service(ChromeDriverManager().install(), log_path="chromedriver.log", verbose=True)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 4) Bật CDP Network domain
driver.execute_cdp_cmd("Network.enable", {})

# 5) Load cookies (giữ nguyên code của bạn)
cookies_json ={
    "url": "https://x.com",
    "cookies": [
        {
            "domain": ".x.com",
            "expirationDate": 1782189423.565001,
            "hostOnly": False,
            "httpOnly": False,
            "name": "guest_id_marketing",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "v1%3A174659106509384187"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1782189423.564576,
            "hostOnly": False,
            "httpOnly": False,
            "name": "guest_id_ads",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "v1%3A174659106509384187"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781151063.999978,
            "hostOnly": False,
            "httpOnly": False,
            "name": "guest_id",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "v1%3A174659106509384187"
        },
        {
            "domain": "x.com",
            "expirationDate": 1762143403,
            "hostOnly": True,
            "httpOnly": False,
            "name": "g_state",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "{\"i_l\":0}"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781151429.103078,
            "hostOnly": False,
            "httpOnly": True,
            "name": "kdt",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "PWBkW58Bkv24SyKFEmRBVqzYSsmRkxMXkO914nkw"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781151429.103198,
            "hostOnly": False,
            "httpOnly": True,
            "name": "auth_token",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "c63738f7fed343378353c20d5973fa768ff12f8d"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781151429.465827,
            "hostOnly": False,
            "httpOnly": False,
            "name": "ct0",
            "path": "/",
            "sameSite": "lax",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "9f5f4c079e7f555653aefe6496f10c467dc043c3784ce2814b2d7f6da9e8ba73f0e47f8f21e144a100ecf0dbe234b94ad600708a88b55df44acc044c9d87342b9ec046b62b7c7e49fbb4e4955abbbe0f"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1779165429.478583,
            "hostOnly": False,
            "httpOnly": False,
            "name": "twid",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "u%3D1919969636952768512"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1778142426.617154,
            "hostOnly": False,
            "httpOnly": False,
            "name": "personalization_id",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "\"v1_vso0/8LANYanmeekinOuww==\""
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781333028.445946,
            "hostOnly": False,
            "httpOnly": False,
            "name": "des_opt_in",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "Y"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1778314714,
            "hostOnly": False,
            "httpOnly": False,
            "name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog",
            "path": "/",
            "sameSite": "lax",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "%7B%22distinct_id%22%3A%220196b3c4-707e-7e31-a0d0-94fa9ed32ce9%22%2C%22%24sesid%22%3A%5B1746778714619%2C%220196b41b-7ae3-7798-a837-00408c527787%22%2C1746778421987%5D%7D"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781590841.085397,
            "hostOnly": False,
            "httpOnly": False,
            "name": "_ga",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "GA1.1.205388427.1746772689"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1781590844.954887,
            "hostOnly": False,
            "httpOnly": False,
            "name": "_ga_RJGMY4G45L",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "GS2.1.s1747030841$o3$g0$t1747030844$j57$l0$h0"
        },
        {
            "domain": "x.com",
            "hostOnly": True,
            "httpOnly": False,
            "name": "lang",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": True,
            "storeId": "0",
            "value": "en"
        },
        {
            "domain": ".x.com",
            "expirationDate": 1747634233.349809,
            "hostOnly": False,
            "httpOnly": True,
            "name": "__cf_bm",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "Vm6icjtueflfqGK4mcSh9xHTec6WBZiYI6hPRmw3B0Y-1747632434-1.0.1.1-OB77ZNHiuy0BsgrHWIL5zlP.S.wlmzMFq.WBtRUKLbTD3e6qWH0WjofunoESvR2MlkgZficUpxCwrDzi4dTV10XUxUjFEKWcYDI3sR0SA9U"
        }
    ]
}
 # JSON bạn đã có
driver.get(cookies_json["url"])
time.sleep(1)
driver.delete_all_cookies()
for c in cookies_json["cookies"]:
    cookie = {
        "name": c["name"],
        "value": c["value"],
        "domain": c["domain"],
        "path": c.get("path", "/"),
        "secure": c.get("secure", False),
        "httpOnly": c.get("httpOnly", False),
    }
    if "expirationDate" in c:
        cookie["expiry"] = int(c["expirationDate"])
    driver.add_cookie(cookie)
list_key=[]
# 6) Mở trang cần bắt request
for i in range(30):
    driver.get("https://x.com/search?q=mua%20sh&src=recent_search_click&f=live")
    time.sleep(5)
    
    # 7) Đọc performance log để lấy header của request
    for entry in driver.get_log("performance"):
        msg = json.loads(entry["message"])["message"]
        if msg.get("method") == "Network.requestWillBeSent" and "SearchTimeline" in msg["params"]["request"]["url"]:
            print("Found URL:", msg["params"]["request"]["url"])
            print("Headers:")
            for k, v in msg["params"]["request"]["headers"].items():
                
                if k.lower() == "x-client-transaction-id":

                    print(v)
                    list_key.append(str(v))
            break
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(list_key, f, ensure_ascii=False, indent=4)

driver.quit()
