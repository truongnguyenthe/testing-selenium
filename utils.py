"""
utils.py — Dùng chung cho toàn bộ test
- Tự động tải ChromeDriver đúng phiên bản (không cần cài tay)
- Dùng webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL     = "https://www.saucedemo.com/"
TIMEOUT = 15
DELAY   = 1.5


def pause():
    time.sleep(DELAY)


def create_driver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Tắt infobars và notifications
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def login(driver, username: str, password: str):
    """Đăng nhập vào SauceDemo với tài khoản chỉ định."""
    print(f"[LOGIN DEBUG] username='{username}', password='{password}'")
    driver.get(URL)
    pause()
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "password").clear()
    pause()
    driver.find_element(By.ID, "user-name").send_keys(username)
    pause()
    driver.find_element(By.ID, "password").send_keys(password)
    pause()
    driver.find_element(By.ID, "login-button").click()


def open_menu(driver, timeout=15):
    """
    Mở sidebar menu và đợi đến khi menu thực sự hiển thị.
    SauceDemo dùng CSS animation + aria-hidden nên KHÔNG dùng visibility_of_element_located.
    """
    btn = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    driver.execute_script("arguments[0].click();", btn)
    # Đợi aria-hidden chuyển từ "true" → "false"
    WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(By.CLASS_NAME, "bm-menu-wrap")
                   .get_attribute("aria-hidden") == "false"
    )
    time.sleep(0.5)  # buffer nhỏ cho animation hoàn tất


def close_menu(driver, timeout=10):
    """Đóng sidebar menu."""
    try:
        cross_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "react-burger-cross-btn"))
        )
        driver.execute_script("arguments[0].click();", cross_btn)
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.CLASS_NAME, "bm-menu-wrap")
                       .get_attribute("aria-hidden") == "true"
        )
    except Exception:
        pass  # Menu có thể đã tự đóng


def reset_app_state(driver):
    """Mở menu → Reset App State → đóng menu."""
    open_menu(driver)
    reset_link = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
    )
    driver.execute_script("arguments[0].click();", reset_link)
    time.sleep(0.5)
    close_menu(driver)
    print(" ✅ Đã RESET trạng thái ứng dụng")


def get_navigation_time(driver, metric: str = "loadEventEnd") -> float:
    """Trả về thời gian (ms) của metric so với navigationStart."""
    script = (
        "try {"
        "  let nav = performance.getEntriesByType('navigation')[0];"
        f"  if (nav && nav['{metric}'] !== undefined) return nav['{metric}'] - nav['startTime'];"
        "  let t = performance.timing;"
        f"  return t['{metric}'] - t['navigationStart'];"
        "} catch(e) { return null; }"
    )
    return driver.execute_script(script)


def slow_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5)


def slow_send_keys(element, text, delay_per_char=0.1):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay_per_char)
