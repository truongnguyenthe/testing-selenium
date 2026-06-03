"""
TEST 4  Reset giỏ • Thêm 2 sản phẩm • Checkout hoàn chỉnh
Chạy đơn lẻ : python tests/test_checkout.py
Chạy pytest : pytest -k test_checkout
"""

import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIME  = utils.TIMEOUT
DELAY = 1.5


def pause():
    time.sleep(DELAY)


def _add_product(driver, add_id: str, expect_badge: int):
    """TC02 TS-04: Thêm sản phẩm vào giỏ và xác nhận badge."""
    btn = WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.ID, add_id))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    pause()
    driver.execute_script("arguments[0].click();", btn)
    pause()

    # Xác nhận nút chuyển sang "Remove"
    remove_id = add_id.replace("add-to-cart", "remove")
    WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, remove_id))
    )

    # Kiểm tra badge – thử cả 2 selector
    end = time.monotonic() + 8
    badge_text = None
    while time.monotonic() < end:
        els = driver.find_elements(By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
        if not els:
            els = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if els and els[0].is_displayed():
            badge_text = els[0].text
            break
        time.sleep(0.3)

    assert badge_text is not None, f"❌ Badge không xuất hiện sau khi thêm {add_id}"
    assert badge_text == str(expect_badge), \
        f"❌ Badge phải là {expect_badge}, nhưng là {badge_text}"
    print(f" ✅ Đã thêm sản phẩm – badge = {badge_text}")


def test_checkout():
    print("\nTEST 4  THÊM 2 SẢN PHẨM ➜ CHECKOUT")
    d = utils.create_driver()

    try:
        # 1. Đăng nhập
        utils.login(d, "standard_user", "secret_sauce")
        WebDriverWait(d, TIME).until(EC.url_contains("inventory.html"))
        pause()

        # 2. TC01 TS-04: Reset trạng thái app
        utils.reset_app_state(d)

        # TC02 TS-04: Thêm 2 sản phẩm
        _add_product(d, "add-to-cart-sauce-labs-backpack", 1)
        _add_product(d, "add-to-cart-sauce-labs-bike-light", 2)

        # 3. Vào giỏ hàng
        cart_link = WebDriverWait(d, TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='shopping-cart-link']"))
        )
        driver_execute = d.execute_script("arguments[0].click();", cart_link)
        WebDriverWait(d, TIME).until(EC.url_contains("cart.html"))
        print(" ✅ Vào trang giỏ hàng")
        pause()

        # 4. TC03 TS-04: Checkout – điền thông tin
        checkout_btn = WebDriverWait(d, TIME).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        d.execute_script("arguments[0].click();", checkout_btn)
        WebDriverWait(d, TIME).until(EC.url_contains("checkout-step-one.html"))
        print(" ✅ Bước checkout 1 – trang điền thông tin")
        pause()

        # Điền form
        form_data = {
            "first-name":  "Mike",
            "last-name":   "Moe",
            "postal-code": "555"
        }
        for fid, value in form_data.items():
            field = WebDriverWait(d, TIME).until(
                EC.visibility_of_element_located((By.ID, fid))
            )
            d.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
            pause()
            field.clear()
            for c in value:
                field.send_keys(c)
                time.sleep(0.1)
            pause()

        continue_btn = WebDriverWait(d, TIME).until(
            EC.element_to_be_clickable((By.ID, "continue"))
        )
        d.execute_script("arguments[0].click();", continue_btn)

        # Kiểm tra không có lỗi form
        time.sleep(1)
        errors = d.find_elements(By.CSS_SELECTOR, "[data-test='error']")
        assert not errors, f"❌ Form bị lỗi: {errors[0].text if errors else ''}"

        WebDriverWait(d, TIME).until(EC.url_contains("checkout-step-two.html"))
        print(" ✅ TC03 PASS – Chuyển sang trang xác nhận đơn (checkout-step-two.html)")

        # 5. TC04 TS-04: Hoàn tất đơn hàng
        finish_btn = WebDriverWait(d, TIME).until(
            EC.element_to_be_clickable((By.ID, "finish"))
        )
        d.execute_script("arguments[0].click();", finish_btn)
        WebDriverWait(d, TIME).until(
            EC.url_to_be("https://www.saucedemo.com/checkout-complete.html")
        )
        print(" ✅ TC04 PASS – ĐƠN HÀNG HOÀN TẤT! (checkout-complete.html)")

    finally:
        d.quit()
        print("🧹 Đã đóng trình duyệt")


if __name__ == "__main__":
    test_checkout()
