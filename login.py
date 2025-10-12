import browser_cookie3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import sys
from http.cookiejar import CookieJar, Cookie
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException

def parse_date_time(date_time_str):
    date_part, time_part = date_time_str.split(' ')
    day, month, year = date_part.split('/')
    hour, minute = time_part.split(':')
    return {
        'day': day,
        'month': month,
        'year': year,
        'hour24': hour,
        'minute': minute
    }

def cookiejar_to_selenium(driver: WebDriver, cj: CookieJar, current_domain: str):
    """
    Chuyển cookie từ CookieJar (browser_cookie3) -> selenium driver.
    driver phải đã load một trang trên same-domain trước khi add_cookie.
    """
    print(f"Bắt đầu chuyển cookie cho domain: {current_domain}")
    for c in cj:
        try:
            # Chỉ thêm các cookie có domain phù hợp với trang đang mở
            if current_domain in c.domain:
                cookie_dict = {
                    "name": c.name,
                    "value": c.value,
                    "domain": c.domain,
                    "path": c.path or "/"
                }
                if getattr(c, "expires", None):
                    cookie_dict["expiry"] = int(c.expires)

                driver.add_cookie(cookie_dict)
                print(f"Đã thêm cookie thành công: {c.name}")
        except Exception as e:
            # Bỏ qua các cookie không thể thêm
            print(f"Không thể thêm cookie {c.name}: {e}")
    print("Hoàn tất chuyển cookie.")

def getInfo():
    id = 2300459705
    start = "11/10/2025 15:00"
    end = "12/10/2025 00:00"
    return id, start, end

def connectWeb():
    # URL của trang web bạn muốn truy cập (phải có same-domain)
    target_url = "https://congdong.ff.garena.vn/tinh-diem"
    target_domain = "congdong.ff.garena.vn"

    # Lấy cookies từ trình duyệt Brave
    # Đối với Chrome, sử dụng browser_cookie3.chrome()
    try:
        cj = browser_cookie3.brave(domain_name=target_domain)
        print(f"Đã lấy {len(cj)} cookie từ Brave cho domain {target_domain}.")
    except Exception as e:
        print(f"Không thể lấy cookie từ Brave: {e}. Hãy đảm bảo Brave đang mở và bạn có đủ quyền truy cập.")
        sys.exit()

    # Khởi tạo Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Bắt buộc: Truy cập trang web trước để có domain phù hợp để add cookie
    driver.get(target_url)

    # Gọi hàm để chuyển đổi và thêm cookie vào driver
    cookiejar_to_selenium(driver, cj, target_domain)
    # Tải lại trang để áp dụng cookie và kiểm tra trạng thái đăng nhập
    driver.refresh()
    return driver

def searchMatch(driver: WebDriver, id: int, start: str, end: str):
    driver.get("https://congdong.ff.garena.vn/tinh-diem")
    # Đến đây bắt đầu chọn form
    start_info = parse_date_time(start)
    end_info = parse_date_time(end)
    # Điền form với thông tin đã nhập
    # Điền Account
    input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "account_id")))
    input_box.send_keys(id)
    input_box.send_keys(Keys.TAB)
    
    day = driver.find_elements(By.NAME, 'day')
    month = driver.find_elements(By.NAME, 'month')
    year = driver.find_elements(By.NAME, 'year')
    hour = driver.find_elements(By.NAME, 'hour24')
    minute = driver.find_elements(By.NAME, 'minute')

    # Điền thời gian kết thúc
    day[0].send_keys(start_info['day'])
    month[0].send_keys(start_info['month'])
    year[0].send_keys(start_info['year'])
    hour[0].send_keys(start_info['hour24'])
    minute[0].send_keys(start_info['minute'], Keys.TAB, Keys.TAB)
    
    day[1].send_keys(end_info['day'])
    month[1].send_keys(end_info['month'])
    year[1].send_keys(end_info['year'])
    hour[1].send_keys(end_info['hour24'])
    minute[1].send_keys(end_info['minute'], Keys.TAB, Keys.TAB, Keys.ENTER)
    # Ở đây có thể thay list tìm kiếm find_elements bằng cách .send_keys(Keys.TAB)
    return driver

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
    spans = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]")))
    # spans trả về danh sách id
    print(f"Đã tìm thấy {len(spans)} trận đấu.")
    if not spans:
        print("Không tìm thấy thẻ!")
    else:
        for i, _ in enumerate(spans, start=1):
            if i <= len(spans) and i % 2 == 1:
                match = matchInfo(driver, str(spans[i-1].text))
                name = getName(driver, str(spans[i-1].text))
                sum = []
                if (len(match) == len(name)):
                    for i in range(len(match)):
                        sum.append({
                            "match_id": match[i]["match_id"],
                            "rank": match[i]["rank"],
                            "id": match[i]["id"],
                            "name": name[i]["name"],
                            "by": match[i]["by"],
                            "elim": match[i]["elim"],
                            "point": match[i]["point"]
                        })
                    for i in sum:
                        print(i)
            else:  
                match = matchInfo(driver, str(spans[i-1].text))
                name = getName(driver, str(spans[i-1].text))
                sum = []
                if (len(match) == len(name)):
                    for i in range(len(match)):
                        sum.append({
                            "match_id": match[i]["match_id"],
                            "rank": match[i]["rank"],
                            "id": name[i]["name"],
                            "name": match[i]["id"],
                            "by": match[i]["by"],
                            "elim": match[i]["elim"],
                            "point": match[i]["point"]
                        })
                    for i in sum:
                        # Chuyển dữ liệu thành file JSON hoặc ném vào DB ở đây!
                        print(i)
        print("Done.")
    return driver

def getName(driver: WebDriver, match_id: str):
    try:
        # Tìm và click vào match
        match_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
        )
        match_link.click()
        time.sleep(0.5)
        name_click = driver.find_element(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/a")
        name_click.click()
        time.sleep(0.5)
        # Đợi cho elements xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"))
        )
        
        # Lấy số lượng elements
        info = driver.find_elements(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div")
        total_info = len(info)
        
        results = []
        
        # Lặp qua từng element bằng index để tránh stale element
        for i in range(total_info):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    el = info[i]
                    # Lấy outerHTML
                    p = el.get_attribute('outerHTML')
                    # Parse với BeautifulSoup
                    soup = BeautifulSoup(p, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)
                    list_data = text.splitlines()
                    # Kiểm tra độ dài list trước khi lấy dữ liệu
                    if len(list_data) >= 6:
                        name = list_data[1]
                        results.append({
                            "name": name
                        })
                    else:
                        continue
                    break  # Thành công thì thoát vòng retry
                except StaleElementReferenceException:
                    if attempt == max_retries - 1:
                        print(f"Không thể lấy team {i+1} sau {max_retries} lần thử")
                    else:
                        print(f"Thử lại lần {attempt + 2} cho team {i+1}")
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"Lỗi tại team {i+1}: {e}")
                    break
        
        return results
    except Exception as e:
        print(f"Lỗi chung trong matchInfo: {e}")
        return []

def matchInfo(driver: WebDriver, match_id: str):
    try:
        # Tìm và click vào match
        match_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
        )
        match_link.click()
        
        # Đợi trang load xong sau khi click
        time.sleep(1)
        
        # Đợi cho elements xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"))
        )
        
        # Lấy số lượng elements
        info = driver.find_elements(By.XPATH, "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div")
        total_info = len(info)
        print(f"Trận này có {total_info} team.")
        
        results = []
        
        # Lặp qua từng element bằng index để tránh stale element
        for i in range(total_info):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    el = info[i]
                    # Lấy outerHTML
                    p = el.get_attribute('outerHTML')
                    # Parse với BeautifulSoup
                    soup = BeautifulSoup(p, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)
                    list_data = text.splitlines()
                    # Kiểm tra độ dài list trước khi lấy dữ liệu
                    if len(list_data) >= 6:
                        ranks = list_data[0]
                        id_val = list_data[1]
                        by = list_data[3]
                        elim = list_data[4]
                        point = list_data[5]
                        
                        results.append({
                            "match_id": match_id,
                            "rank": ranks,
                            "id": id_val,
                            "by": by,
                            "elim": elim,
                            "point": point
                        })
                    else:
                        continue
                    break  # Thành công thì thoát vòng retry
                except StaleElementReferenceException:
                    if attempt == max_retries - 1:
                        print(f"Không thể lấy team {i+1} sau {max_retries} lần thử")
                    else:
                        print(f"Thử lại lần {attempt + 2} cho team {i+1}")
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"Lỗi tại team {i+1}: {e}")
                    break
        
        return results
        
    except Exception as e:
        print(f"Lỗi chung trong matchInfo: {e}")
        return []

if __name__ == "__main__":
    driver = connectWeb()
    driver.get("https://congdong.ff.garena.vn/tinh-diem")

    driver = getMacth(driver)

    if(input("Nhập 'e' và Enter để kết thúc\n") == ord('e')):
        driver.quit()
        sys.exit()