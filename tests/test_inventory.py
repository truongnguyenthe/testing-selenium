import sys, os, time, traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

import utils


def lay_danh_sach_san_pham(driver):
    """Lấy danh sách tên và giá sản phẩm hiện tại."""
    ten_elems = WebDriverWait(driver, utils.TIMEOUT).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name"))
    )
    gia_elems = WebDriverWait(driver, utils.TIMEOUT).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price"))
    )
    ten_list = [t.text for t in ten_elems]
    gia_list = [float(g.text.replace("$", "")) for g in gia_elems]
    return ten_list, gia_list


def in_danh_sach(ten_list, gia_list):
    for t, g in zip(ten_list, gia_list):
        print(f"   {t} - ${g}")


def test_inventory_sort_only():
    print("\nTEST 3: SẢN PHẨM & SẮP XẾP")
    driver = utils.create_driver()
    utils.login(driver, "standard_user", "secret_sauce")

    try:
        WebDriverWait(driver, utils.TIMEOUT).until(EC.url_contains("inventory.html"))
        WebDriverWait(driver, utils.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        print("✅ Hiển thị danh sách sản phẩm")

        # --- Sắp xếp A → Z ---
        while True:
            try:
                Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (A to Z)")
                break
            except StaleElementReferenceException:
                time.sleep(0.2)
        time.sleep(1)
        ten_list, gia_list = lay_danh_sach_san_pham(driver)
        print("Sắp xếp: Name (A to Z)")
        in_danh_sach(ten_list, gia_list)
        assert ten_list == sorted(ten_list), f"❌ Sắp xếp A→Z sai: {ten_list}"
        print("✅ A → Z đúng thứ tự")

        # --- Sắp xếp Z → A ---
        while True:
            try:
                Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (Z to A)")
                break
            except StaleElementReferenceException:
                time.sleep(0.2)
        time.sleep(1)
        ten_list, gia_list = lay_danh_sach_san_pham(driver)
        print("Sắp xếp: Name (Z to A)")
        in_danh_sach(ten_list, gia_list)
        assert ten_list == sorted(ten_list, reverse=True), f"❌ Sắp xếp Z→A sai: {ten_list}"
        print("✅ Z → A đúng thứ tự")

        # --- Sắp xếp giá thấp → cao ---
        while True:
            try:
                Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (low to high)")
                break
            except StaleElementReferenceException:
                time.sleep(0.2)
        time.sleep(1)
        ten_list, gia_list = lay_danh_sach_san_pham(driver)
        print("Sắp xếp: Price (low to high)")
        in_danh_sach(ten_list, gia_list)
        assert gia_list == sorted(gia_list), f"❌ Sắp xếp giá thấp→cao sai: {gia_list}"
        print("✅ Giá thấp → cao đúng thứ tự")

        # --- Sắp xếp giá cao → thấp ---
        while True:
            try:
                Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (high to low)")
                break
            except StaleElementReferenceException:
                time.sleep(0.2)
        time.sleep(1)
        ten_list, gia_list = lay_danh_sach_san_pham(driver)
        print("Sắp xếp: Price (high to low)")
        in_danh_sach(ten_list, gia_list)
        assert gia_list == sorted(gia_list, reverse=True), f"❌ Sắp xếp giá cao→thấp sai: {gia_list}"
        print("✅ Giá cao → thấp đúng thứ tự")

    except Exception as e:
        print("ĐÃ XẢY RA LỖI:", type(e), repr(e))
        traceback.print_exc(file=sys.stdout)
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    test_inventory_sort_only()
