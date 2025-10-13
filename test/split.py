import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from url.process import connectWeb, getInfo, searchMatch
from bs4 import BeautifulSoup

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
match_id = int("1975591568364523520")
print(f"Đang mở trận {match_id}")
match_link = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f"//a[text()='{match_id}']")))
match_link.click()
time.sleep(1)
# Click để mở chi tiết trận
name_click = driver.find_element(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/a")
name_click.click()
time.sleep(1)
elements = driver.find_elements(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div")
for i, el in enumerate(elements, start=1):
    p = el.get_attribute('outerHTML')
    soup = BeautifulSoup(p, "html.parser")
    # Lấy toàn bộ text hiển thị
    text = soup.get_text(separator="\n", strip=True)
    list = text.splitlines()
    player = list[1]
    print(f"{player}")
        
print("Hoàn tất trận", match_id, "\n")