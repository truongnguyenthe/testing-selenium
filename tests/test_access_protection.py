import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_access_protection():
    print("\nTEST 6: CHẶN TRUY CẬP KHI CHƯA LOGIN")
    driver = utils.create_driver()
    try:
        # Thử truy cập trang inventory khi chưa đăng nhập
        driver.get("https://www.saucedemo.com/inventory.html")
        time.sleep(2)

        # SauceDemo chuyển hướng về trang login khi chưa xác thực
        current_url = driver.current_url
        page_source = driver.page_source.lower()

        # Kiểm tra bị chuyển về login hoặc trang có form login
        is_redirected = "saucedemo.com/" == current_url or "inventory" not in current_url
        has_login_form = "login" in page_source or "username" in page_source

        assert is_redirected or has_login_form, \
            "❌ Có thể truy cập trang sản phẩm khi chưa đăng nhập!"
        print(" ✅ Không login, không truy cập được sản phẩm")

        # Xác nhận trang login hiển thị form
        assert driver.find_elements(By.ID, "user-name"), \
            "❌ Trang login không hiển thị form đăng nhập"
        print(" ✅ Form đăng nhập hiển thị đúng")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_access_protection()
