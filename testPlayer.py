from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
from login import getInfo, searchMatch, connectWeb

driver = connectWeb()
driver.get("https://congdong.ff.garena.vn/tinh-diem")

print("Đang tìm kiếm trận đấu...")
id, start, end = getInfo()
driver = searchMatch(driver, id, start, end)

# Đóng popup nếu có
try:
    close_btn = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='close' and @data-dismiss='modal']"))
    )
    close_btn.click()
except:
    pass

# Lấy danh sách các trận đấu
spans = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]"))
)

print(f"Đã tìm thấy {len(spans)} trận đấu.")
if not spans:
    print("Không tìm thấy thẻ!")
else:
    for span in spans:
        if not span.text.strip():
            continue

        match_id = span.text.strip()
        print(f"Đang mở trận {match_id}")

        # Click để mở chi tiết trận
        driver = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
        )
        driver.click()
        # Lấy tất cả các div con
        elements = driver.find_elements(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div")

        print(f"Tìm thấy {len(elements)} phần tử.")

        for i, el in enumerate(elements, start=1):
            print(f"Phần tử thứ {i}: {el.get_attribute('outerHTML')}")# Hoặc el.get_attribute('outerHTML')
        
        print("Hoàn tất trận", match_id, "\n")

print("Hoàn tất toàn bộ.")
