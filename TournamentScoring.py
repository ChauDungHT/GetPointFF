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
from database import Database

TARGET_URL = "https://congdong.ff.garena.vn/tinh-diem"
TARGET_DOMAIN = "congdong.ff.garena.vn"

class TournamentScoring:
    def __init__(self, target_url, tager_domain):
        self.target_url = target_url
        self.target_domain = tager_domain
        self.driver = None

    def parse_date_time(self, date_time_str):
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

    def cookiejar_to_selenium(self, cj: CookieJar, current_domain: str):
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

                    self.driver.add_cookie(cookie_dict)
                    print(f"Đã thêm cookie thành công: {c.name}")
            except Exception as e:
                # Bỏ qua các cookie không thể thêm
                print(f"Không thể thêm cookie {c.name}: {e}")
        print("Hoàn tất chuyển cookie.")

    def getInfo(self):
        id = input("Nhập ID: ")
        start = input("Thời gian bắt đầu: ")
        end = input("Thời gian kết thúc: ")
        return id, start, end

    def connectWeb(self, target_domain=TARGET_DOMAIN, target_url=TARGET_URL):
        # Lấy cookies từ trình duyệt Brave
        try:
            cj = browser_cookie3.brave(domain_name=target_domain)
            print(f"Đã lấy {len(cj)} cookie từ Brave cho domain {target_domain}.")
        except Exception as e:
            print(f"Không thể lấy cookie từ Brave: {e}. Hãy đảm bảo Brave đang mở và bạn có đủ quyền truy cập.")
            sys.exit()

        # Khởi tạo Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

        # Bắt buộc: Truy cập trang web trước để có domain phù hợp để add cookie
        self.driver.get(TARGET_URL)

        # Gọi hàm để chuyển đổi và thêm cookie vào driver
        self.cookiejar_to_selenium(cj, TARGET_DOMAIN)
        
        # Tải lại trang để áp dụng cookie và kiểm tra trạng thái đăng nhập
        self.driver.refresh()
        return self.driver

    def searchMatch(self, id: int, start: str, end: str):
        self.driver.get("https://congdong.ff.garena.vn/tinh-diem")
        
        # Đến đây bắt đầu chọn form
        start_info = self.parse_date_time(start)
        end_info = self.parse_date_time(end)
        
        # Điền form với thông tin đã nhập
        # Điền Account
        input_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "account_id"))
        )
        input_box.send_keys(id)
        input_box.send_keys(Keys.TAB)
        
        day = self.driver.find_elements(By.NAME, 'day')
        month = self.driver.find_elements(By.NAME, 'month')
        year = self.driver.find_elements(By.NAME, 'year')
        hour = self.driver.find_elements(By.NAME, 'hour24')
        minute = self.driver.find_elements(By.NAME, 'minute')

        # Điền thời gian bắt đầu
        day[0].send_keys(start_info['day'])
        month[0].send_keys(start_info['month'])
        year[0].send_keys(start_info['year'])
        hour[0].send_keys(start_info['hour24'])
        minute[0].send_keys(start_info['minute'], Keys.TAB, Keys.TAB)
        
        # Điền thời gian kết thúc
        day[1].send_keys(end_info['day'])
        month[1].send_keys(end_info['month'])
        year[1].send_keys(end_info['year'])
        hour[1].send_keys(end_info['hour24'])
        minute[1].send_keys(end_info['minute'], Keys.TAB, Keys.TAB, Keys.ENTER)
        
        return self.driver

    def getMatch(self):
        """
        Tìm kiếm và lưu thông tin trận đấu
        
        Args:
            file_name: Tên file để lưu dữ liệu (mặc định: matches.json)
        
        Returns:
            WebDriver: Driver instance sau khi xử lý
        """
        print("Đang tìm kiếm trận đấu...")
        
        # Lấy thông tin và tìm kiếm
        id, start, end = self.getInfo()
        self.searchMatch(id, start, end)
        
        # Đóng modal nếu có
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='close' and @data-dismiss='modal']"))
            )
            close_btn.click()
        except Exception:
            pass
        
        # Lấy danh sách các trận đấu
        spans = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'match__id')]"))
        )
        
        print(f"Đã tìm thấy {len(spans)} trận đấu.")
        
        if not spans:
            print("Không tìm thấy trận đấu nào!")
            return self.driver
        
        # Xử lý từng trận đấu
        all_matches_data = []
        
        for index, span in enumerate(spans, start=1):
            match_id_text = str(span.text)
            print(f"Đang xử lý trận {index}/{len(spans)}: {match_id_text}")
            
            # Lấy thông tin trận đấu và tên người chơi
            match = self.matchInfo(match_id_text)
            name = self.getName(match_id_text)
            
            # Kiểm tra độ dài dữ liệu
            if len(match) != len(name):
                print(f"⚠️  Cảnh báo: Độ dài dữ liệu không khớp cho trận {match_id_text}")
                print(f"   Match: {len(match)}, Name: {len(name)}")
            
            # Xử lý dữ liệu dựa trên index (lẻ/chẵn)
            match_data = []
            min = len(match) if len(match) < len(name) else len(name)
            if index % 2 == 1:  # Index lẻ
                for i in range(min): # Sử dụng min để tránh lỗi index
                    match_data.append({
                        "match_id": match[i]["match_id"],
                        "rank": match[i]["rank"],
                        "id": match[i]["id"],
                        "name": name[i]["name"],
                        "by": match[i]["by"],
                        "elim": match[i]["elim"],
                        "point": match[i]["point"]
                    })
            else:  # Index chẵn (hoán đổi id và name)
                for i in range(min): # Sử dụng min để tránh lỗi index
                    match_data.append({
                        "match_id": match[i]["match_id"],
                        "rank": match[i]["rank"],
                        "id": name[i]["name"],  # Hoán đổi
                        "name": match[i]["id"],  # Hoán đổi
                        "by": match[i]["by"],
                        "elim": match[i]["elim"],
                        "point": match[i]["point"]
                    })
            
            all_matches_data.extend(match_data)
        
        # Lưu tất cả dữ liệu vào file một lần
        if all_matches_data:
            Database.save_to_json(all_matches_data)
        
        print("Done.")
        return self.driver

    def getName(self, match_id: str):
        try:
            # Tìm và click vào match
            match_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
            )
            match_link.click()
            time.sleep(0.5)
            
            name_click = self.driver.find_element(
                By.XPATH, 
                "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/a"
            )
            name_click.click()
            time.sleep(0.5)
            
            # Đợi cho elements xuất hiện
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((
                    By.XPATH, 
                    "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"
                ))
            )
            
            # Lấy số lượng elements
            info = self.driver.find_elements(
                By.XPATH, 
                "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"
            )
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
                            name = list_data[2]
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
            print(f"Lỗi chung trong getName: {e}")
            return []

    def get_nonempty(ld, idx):
        return ld[idx].strip() if len(ld) > idx and ld[idx].strip() else None
    
    def matchInfo(self, match_id: str):
        try:
            # Tìm và click vào match
            match_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{match_id}']"))
            )
            match_link.click()
            
            # Đợi trang load xong sau khi click
            time.sleep(1)
            
            # Đợi cho elements xuất hiện
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((
                    By.XPATH, 
                    "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"
                ))
            )
            
            # Lấy số lượng elements
            info = self.driver.find_elements(
                By.XPATH, 
                "/html/body/div/section/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div"
            )
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
                        id_candidate_1 = get_nonempty(list_data, 1)
                        id_candidate_2 = get_nonempty(list_data, 2)

                        if id_candidate_2:  # list_data[2] tồn tại và không rỗng
                            ranks = f"Top {attempt + 1}"
                            id_val = id_candidate_1
                            by = get_nonempty(list_data, 3)
                            elim = get_nonempty(list_data, 4)
                            point = get_nonempty(list_data, 5)
                        elif id_candidate_1:  # fallback nếu [2] rỗng nhưng [1] có
                            ranks = f"Top {attempt + 1}"
                            id_val = id_candidate_2
                            by = get_nonempty(list_data, 4)
                            elim = get_nonempty(list_data, 5)
                            point = get_nonempty(list_data, 6)
                        else:
                            # không đủ dữ liệu, bỏ qua hoặc gán mặc định
                            print(f"Không đủ dữ liệu cho team {i+1}: {list_data}")
                            continue
                            
                        results.append({
                            "match_id": match_id,
                            "rank": ranks,
                            "id": id_val,
                            "by": by,
                            "elim": elim,
                            "point": point
                        })
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
    
    def run(self):
        try:
            this = self.connectWeb()
            this.get("https://congdong.ff.garena.vn/tinh-diem")
            req = self.getMatch()
        except Exception as e:
            print(f"Lỗi: {e}")
            import traceback
            traceback.print_exc
        finally:
            if self.driver:
                time.sleep(2)
                self.driver.quit()
                print("Đã đóng trình duyệt.\n")

def get_nonempty(ld, idx):
        return ld[idx].strip() if len(ld) > idx and ld[idx].strip() else None
        
def run():
    target_url=TARGET_URL
    target_domain=TARGET_DOMAIN
    driver = TournamentScoring(target_url, target_domain)
    driver.run()

if __name__ == "__main__":
    run()