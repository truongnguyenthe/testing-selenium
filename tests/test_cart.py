"""
TEST 2  Chức năng giỏ hàng
Chạy: python tests/test_cart.py
"""
import sys, os, time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils

TIME = utils.TIMEOUT
DELAY = 2.0


def pause():
    time.sleep(DELAY)


def wait_badge(driver, timeout=10):
    """Đợi badge giỏ hàng xuất hiện – thử cả 2 selector phòng trường hợp DOM thay đổi."""
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        # Selector ưu tiên: data-test attribute
        els = driver.find_elements(By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
        if not els:
            # Fallback: class name
            els = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if els and els[0].is_displayed():
            return els[0].text
        time.sleep(0.3)
    raise AssertionError("❌ Badge giỏ hàng không xuất hiện sau khi thêm sản phẩm")


def badge_gone(driver, timeout=8):
    """Xác nhận badge đã biến mất."""
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        els = driver.find_elements(By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
        if not els:
            els = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if not els or not els[0].is_displayed():
            return True
        time.sleep(0.3)
    return False


def test_cart_functionality():
    print("\nTEST 2: CHỨC NĂNG GIỎ HÀNG")
    driver = utils.create_driver()
    try:
        # 1️ Đăng nhập (TC01 TS-01 đã kiểm thử riêng, dùng lại để setup)
        utils.login(driver, "standard_user", "secret_sauce")
        WebDriverWait(driver, TIME).until(EC.url_contains("inventory.html"))
        assert "inventory.html" in driver.current_url, "❌ Đăng nhập thất bại"
        print(" ✅ Đăng nhập thành công")
        pause()

        # 2️ TC01 TS-02: Thêm sản phẩm → badge hiển thị số 1
        print("\n🛒 TC01 – Thêm sản phẩm vào giỏ")
        btn = WebDriverWait(driver, TIME).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", btn)   # JS click tránh intercept

        badge_text = wait_badge(driver)
        assert badge_text == "1", f"❌ Badge phải là '1', nhưng là '{badge_text}'"
        print(f" ✅ TC01 PASS – Badge hiển thị: {badge_text}")

        # 3️ TC02 TS-02: Vào trang giỏ hàng → cart.html
        print("\n📦 TC02 – Vào trang giỏ hàng")
        cart_link = WebDriverWait(driver, TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='shopping-cart-link']"))
        )
        driver.execute_script("arguments[0].click();", cart_link)
        WebDriverWait(driver, TIME).until(EC.url_contains("cart.html"))
        assert "cart.html" in driver.current_url, "❌ Không vào được trang giỏ hàng"
        print(" ✅ TC02 PASS – Đã vào trang cart.html")

        # Kiểm tra có đúng 1 sản phẩm trong giỏ
        WebDriverWait(driver, TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 1, f"❌ Giỏ hàng phải có 1 sản phẩm, nhưng có {len(items)}"
        print(f" ✅ Giỏ hàng có {len(items)} sản phẩm")

        # 4️ TC03 TS-02: Xóa sản phẩm → badge biến mất
        print("\n🗑 TC03 – Xóa sản phẩm khỏi giỏ")
        remove_btn = WebDriverWait(driver, TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test^='remove']"))
        )
        remove_btn.click()
        pause()

        assert badge_gone(driver), "❌ Badge vẫn còn sau khi xóa sản phẩm"
        print(" ✅ TC03 PASS – Badge đã biến mất")

        items_after = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items_after) == 0, f"❌ Giỏ hàng vẫn còn {len(items_after)} sản phẩm"
        print(" ✅ Giỏ hàng đã trống")

    finally:
        driver.quit()
        print("\n🧹 Đã đóng trình duyệt.")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
