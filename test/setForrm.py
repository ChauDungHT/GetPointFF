import test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def getInfo():
    id = input("Nhap id: ")
    start = input("Nhap thoi gian bat dau: ")
    end = input("Nhap thoi gian ket thuc: ")
    return id, start, end

def parse_date_time(date_time_str):
    date_part, time_part = date_time_str.split(' ')
    day, month, year = date_part.split('/')
    hour, minute = time_part.split(':')
    return {
        'day': day,
        'month': month,
        'year': year,
        'hour24h': hour,
        'minute': minute
    }

if __name__ == "__main__":
    id, start, end = 1240104899, "21/09/2025 13:30", "22/09/2025 00:00"
    start_info = parse_date_time(start)
    end_info = parse_date_time(end)

    driver = webdriver.Chrome()

    driver.get("congdong.ff.garena.vn/tinh-diem")

    # Tìm và điền Account ID
    driver.find_element(By.NAME, "account_id").send_keys(id)

    # Tìm và điền thời gian bắt đầu
    driver.find_element(By.NAME, "day_start").send_keys(start_info['day'])
    driver.find_element(By.NAME, "month_start").send_keys(start_info['month'])
    driver.find_element(By.NAME, "year_start").send_keys(start_info['year'])
    driver.find_element(By.NAME, "hour24h_start").send_keys(start_info['hour24h'])
    driver.find_element(By.NAME, "minute_start").send_keys(start_info['minute'])

    # Tìm và điền thời gian kết thúc
    driver.find_element(By.NAME, "day_end").send_keys(end_info['day'])
    driver.find_element(By.NAME, "month_end").send_keys(end_info['month'])
    driver.find_element(By.NAME, "year_end").send_keys(end_info['year'])
    driver.find_element(By.NAME, "hour24h_end").send_keys(end_info['hour24h'])
    driver.find_element(By.NAME, "minute_end").send_keys(end_info['minute'])

    # Nhấn "Tìm kiếm"
    driver.find_element(By.XPATH, "//button[text()='Tìm kiếm']").click()

from selenium.webdriver.support.ui import Select
province = Select(driver.find_element(By.ID, "gender"))
province.select_by_value("male")  # hoặc select_by_visible_text("Nam")