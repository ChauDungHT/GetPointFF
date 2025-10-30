from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from url.TournamentScoring import TournamentScoring
from selenium.common.exceptions import StaleElementReferenceException
import time

TARGET_URL = "https://congdong.ff.garena.vn/tinh-diem"
TARGET_DOMAIN = "congdong.ff.garena.vn"

driver = TournamentScoring(TARGET_URL, TARGET_DOMAIN)
bot = driver.connectWeb()
bot.get("https://congdong.ff.garena.vn/tinh-diem")

print("Đang tìm kiếm trận đấu...")
id, start, end = driver.getInfo()
bot = driver.searchMatch(bot, id, start, end)
try:
    close_btn = WebDriverWait(bot, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='close' and @data-dismiss='modal']"))
    )
    close_btn.click()
except:
    pass
spans = WebDriverWait(bot, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]")))
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
        for y in range(len(ranks)):
            print(f"{y+1}: {ranks[y].text}")
        print("\n")
    print("Done.")