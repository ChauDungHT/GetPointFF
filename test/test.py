from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import sys
import pandas as pd
from url.process import connectWeb, getInfo, parse_date_time, cookiejar_to_selenium, searchMatch
def getMacth(driver: WebDriver):
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
    #spans = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]")))
    # spans trả về danh sách id
    span = str("1969680846346506240")
    matchInfo(driver, span)
    return driver

def matchInfo(driver: WebDriver, match_id: str):
    # Tìm thẻ <a> chứa match_id
    match_link = driver.find_element(By.XPATH, f"//a[text()='{match_id}']")
    match_link.click()
    # Thẻ cha .match
    match_container = match_link.find_element(By.XPATH, "./ancestor::div[@class='col-3 match']")
    # Từ thẻ cha match, đi ra ngoài (row chứa thông tin)
    row = match_container.find_element(By.XPATH, "./ancestor::div[@class='row']")
    # Danh sách team/Rank
    ranks = row.find_elements(By.XPATH, ".//div[contains(@class,'no-border')]//span")
    print(f"Đã tìm thấy {len(ranks)} đội.")
    print(row.text)
    return driver

if __name__ == "__main__":
    # 1969654135433187329 OK
    # 1969658887353126912
    # 1969663950817579008
    # 1969669102458884096
    # 1969674483440537600
    # 1969680846346506240
    # 1969681059748499456
    driver = connectWeb()
    driver.get("https://congdong.ff.garena.vn/tinh-diem")
    id = str('1969680846346506240')
    driver = getMacth(driver)

    if(input("Nhập 'e' để kết thúc") == ord('e')):
        driver.quit()
        sys.exit()