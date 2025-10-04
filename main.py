from login import connectWeb
from login import getMacth
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def searchMatchs(driver: WebDriver):
    return getMacth(driver)

def exit(driver: WebDriver):
    print("Thoát.")
    driver.quit()
    sys.exit()

options = {
    "1": searchMatchs,
    "2": exit
}

if __name__ == "__main__":

    driver = connectWeb()
    # Cần sửa lại hàm getInfo() để nhận thông tin nhập từ bàn phím
    while True:
        print("\n===== MENU =====")
        print("1. Tìm kiếm trận đấu")
        print("2. Thoát")

        choice = input("Nhập lựa chọn: ").strip()
        action = options.get(choice)
        if action:
            action(driver)
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập lại!")