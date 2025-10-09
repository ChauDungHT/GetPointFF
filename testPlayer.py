from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from login import getInfo, searchMatch, connectWeb
import re

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

        match_id = int(span.text.strip())
        print(f"Đang mở trận {match_id}")

        # Click để mở chi tiết trận
        driver = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
        )
        driver.click()
        time.sleep(1)
        # Lấy tất cả các div con
        elements = driver.find_elements(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div")

        print(f"Tìm thấy {len(elements)} phần tử.")

        for i, el in enumerate(elements, start=1):
            p = el.get_attribute('outerHTML')
            pattern = re.compile(
                r'<span>(Top\s*\d+)</span>.*?'
                r'<span style="margin: 0px 50px;">(.*?)</span>'
                r'<span style="margin: 0px 50px;">(.*?)</span>.*?'
                r'<div class="col-1">(\d+)</div>'
                r'<div class="col-2">(\d+)</div>'
                r'<div class="col-2">(\d+)</div>',
                re.DOTALL
            )

            match = pattern.search(p)
            if match:
                top, team1, team2, BY, elim, point = match.groups()
                print(top, team2, BY, elim, point)
        
        print("Hoàn tất trận", match_id, "\n")

print("Hoàn tất toàn bộ.")
