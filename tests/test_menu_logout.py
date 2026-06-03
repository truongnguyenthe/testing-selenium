"""
TEST 5  MENU & ĐĂNG XUẤT
Chạy: python tests/test_menu_logout.py
"""
import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIME  = utils.TIMEOUT
DELAY = 1.2


def pause():
    time.sleep(DELAY)


def test_sidebar_and_logout():
    print("\nTEST 5 – MENU & ĐĂNG XUẤT")
    driver = utils.create_driver()
    try:
        # Đăng nhập
        utils.login(driver, "standard_user", "secret_sauce")
        WebDriverWait(driver, TIME).until(EC.url_contains("inventory.html"))
        assert "inventory.html" in driver.current_url, "❌ Đăng nhập thất bại"
        pause()

        # TC01 TS-05: Mở menu sidebar – dùng open_menu() đợi aria-hidden="false"
        print("\n☰ TC01 – Mở menu sidebar")
        utils.open_menu(driver)

        # Xác nhận các mục menu hiển thị đầy đủ
        assert driver.find_element(By.ID, "inventory_sidebar_link").is_displayed(), \
            "❌ Menu thiếu mục 'All Items'"
        assert driver.find_element(By.ID, "logout_sidebar_link").is_displayed(), \
            "❌ Menu thiếu mục 'Logout'"
        assert driver.find_element(By.ID, "reset_sidebar_link").is_displayed(), \
            "❌ Menu thiếu mục 'Reset App State'"
        print(" ✅ TC01 PASS – Menu hiển thị đầy đủ bên trái")

        # TC02 TS-05: Reset app từ menu
        print("\n🔄 TC02 – Reset app từ menu")
        reset_link = WebDriverWait(driver, TIME).until(
            EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))
        )
        driver.execute_script("arguments[0].click();", reset_link)
        time.sleep(1)
        print(" ✅ TC02 PASS – Đã reset trạng thái ứng dụng")

        # TC03 TS-05: Logout – mở lại menu nếu đã đóng sau reset
        print("\n🚪 TC03 – Logout")
        # Kiểm tra menu còn mở không
        is_open = driver.find_element(By.CLASS_NAME, "bm-menu-wrap") \
                        .get_attribute("aria-hidden") == "false"
        if not is_open:
            utils.open_menu(driver)

        logout_link = WebDriverWait(driver, TIME).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        driver.execute_script("arguments[0].click();", logout_link)

        # Xác nhận chuyển về trang login
        WebDriverWait(driver, TIME).until(
            EC.url_to_be("https://www.saucedemo.com/")
        )
        assert driver.current_url == "https://www.saucedemo.com/", \
            f"❌ URL sau logout sai: {driver.current_url}"
        assert driver.find_element(By.ID, "login-button").is_displayed(), \
            "❌ Không thấy nút Login sau khi đăng xuất"
        print(" ✅ TC03 PASS – Đăng xuất thành công, về đúng trang login")

    except Exception as e:
        pytest.fail(f"❌ Lỗi: {e}")

    finally:
        driver.quit()
        print("🧹 Đã đóng trình duyệt")


if __name__ == "__main__":
    test_sidebar_and_logout()
