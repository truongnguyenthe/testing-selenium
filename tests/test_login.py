"""
TEST 1  Đăng nhập
•  Chạy pytest : pytest -k test_login
•  Chạy         : python tests/test_login.py
"""

import sys, os, time, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# ────────────────────────────────────────────────────────────

import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = utils.TIMEOUT
DELAY   = 2.0          

def pause(): time.sleep(DELAY)

def _wait_error(driver, timeout=10):
    """Đợi text lỗi (nếu có) và trả lại, None nếu không thấy."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        return driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    except:       
        return None


@pytest.mark.parametrize(
    "username, password, expect_ok, label",
    [
        ("standard_user", "secret_sauce", True,  "Hợp lệ"),
        ("standard_user", "sai",          False, "Sai mật khẩu"),
        ("sai_user",      "secret_sauce", False, "Sai username"),
        ("",              "secret_sauce", False, "Trống username"),
        ("standard_user", "",             False, "Trống password"),
    ]
)
def test_login(username, password, expect_ok, label):
    print(f"\nTEST 1  ĐĂNG NHẬP  ➜  {label}")
    dr = utils.create_driver()
    try:
        utils.login(dr, username, password)

        try:
            WebDriverWait(dr, 3).until(EC.url_contains("inventory.html"))
        except:
            pass
        pause()

        if expect_ok:
            assert "inventory.html" in dr.current_url, "Đăng nhập hợp lệ nhưng không chuyển trang"
            print(" ✅ Đăng nhập thành công")
        else:
            err = _wait_error(dr, 7)
            assert err is not None, "Không hiển thị lỗi cho trường hợp sai"
            print(f" ✅ Hiển thị lỗi: {err}")

    finally:
        dr.quit()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
