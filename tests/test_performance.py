"""
TEST 7  Đo hiệu năng: login, inventory, add-to-cart
Chạy: python tests/test_performance.py
"""

import time, sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils

MAX_LOGIN_LOAD   = 2000
MAX_INVENTORY_UI = 1500
MAX_ADD_TO_CART  = 800
TIME = utils.TIMEOUT


def get_navigation_time(driver, metric="loadEventEnd"):
    """Lấy thời gian hiệu năng từ Performance API."""
    script = f"""
    try {{
        let nav = performance.getEntriesByType('navigation')[0];
        if (nav && nav['{metric}'] !== undefined)
            return nav['{metric}'] - nav['startTime'];
        let t = performance.timing;
        return t['{metric}'] - t['navigationStart'];
    }} catch (e) {{
        return null;
    }}
    """
    return driver.execute_script(script)


def test_performance():
    print("\nTEST 7  ĐO HIỆU NĂNG")
    driver = utils.create_driver()
    utils.login(driver, "standard_user", "secret_sauce")

    WebDriverWait(driver, TIME).until(EC.url_contains("inventory.html"))

    # TC01 TS-07: Login → Inventory ≤ 2000ms
    login_time = get_navigation_time(driver, "loadEventEnd")
    assert login_time is not None, "❌ Không lấy được thời gian Login → Inventory"
    ket_qua = "✅ NHANH" if login_time <= MAX_LOGIN_LOAD else "❌ CHẬM"
    print(f"  Login → Inventory: {login_time:.0f} ms  {ket_qua}")
    assert login_time <= MAX_LOGIN_LOAD, \
        f"❌ TC01: Thời gian login ({login_time:.0f} ms) vượt ngưỡng {MAX_LOGIN_LOAD} ms"
    print("  ✅ TC01 PASS")

    # TC02 TS-07: Inventory UI ready ≤ 1500ms
    ui_time = get_navigation_time(driver, "responseEnd")
    assert ui_time is not None, "❌ Không lấy được thời gian Inventory UI"
    ket_qua = "✅ NHANH" if ui_time <= MAX_INVENTORY_UI else "❌ CHẬM"
    print(f"  Inventory UI ready: {ui_time:.0f} ms  {ket_qua}")
    assert ui_time <= MAX_INVENTORY_UI, \
        f"❌ TC02: Thời gian UI ready ({ui_time:.0f} ms) vượt ngưỡng {MAX_INVENTORY_UI} ms"
    print("  ✅ TC02 PASS")

    # TC03 TS-07: Add-to-Cart phản hồi ≤ 800ms
    btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )
    t0 = time.perf_counter()
    driver.execute_script("arguments[0].click();", btn)

    # Đợi badge với dual selector (data-test ưu tiên, fallback class)
    end_wait = time.monotonic() + 3
    badge_found = False
    while time.monotonic() < end_wait:
        els = driver.find_elements(By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
        if not els:
            els = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if els:
            badge_found = True
            break
        time.sleep(0.1)

    duration = (time.perf_counter() - t0) * 1000
    assert badge_found, "❌ TC03: Badge không xuất hiện sau khi Add to Cart"
    ket_qua = "✅ NHANH" if duration <= MAX_ADD_TO_CART else "❌ CHẬM"
    print(f"  Add-to-Cart phản hồi: {duration:.0f} ms  {ket_qua}")
    assert duration <= MAX_ADD_TO_CART, \
        f"❌ TC03: Thời gian Add-to-Cart ({duration:.0f} ms) vượt ngưỡng {MAX_ADD_TO_CART} ms"
    print("  ✅ TC03 PASS")

    driver.quit()


if __name__ == "__main__":
    test_performance()
