from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import getInfo, searchMatch, matchInfo, connectWeb
from selenium.common.exceptions import StaleElementReferenceException
import time

driver = connectWeb()
driver.get("https://congdong.ff.garena.vn/tinh-diem")

print("Đang tìm kiếm trận đấu...")
id, start, end = getInfo()
driver = searchMatch(driver, id, start, end)
try:
    close_btn = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='close' and @data-dismiss='modal']"))
    )
    close_btn.click()
except:
    pass
spans = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]")))
# spans trả về danh sách id
print(f"Đã tìm thấy {len(spans)} trận đấu.")
if not spans:
    print("Không tìm thấy thẻ!")
else:
    for i in range(len(spans)):
        if not spans[i].text.strip():
            continue
        match_id = int(spans[i].text)
        print(match_id)
        match_link = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f"//a[text()='{match_id}']")))
        match_link.click()
        match_container = match_link.find_element(By.XPATH, "./ancestor::div[@class='col-3 match']")
        row = match_container.find_element(By.XPATH, "./ancestor::div[@class='row']")
        # Danh sách team/Rank
        ranks = row.find_elements(By.XPATH, ".//div[contains(@class,'no-border')]//span")
        for rank in ranks:
            players = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-5']//span[not(contains(@style,'visibility: hidden'))]")))
            for player in players: 
                if not player.text or not player:
                    continue
                else:
                    print(f"{player.text}")
        print("\n")
    print("Done.")