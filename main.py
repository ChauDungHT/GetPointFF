from TournamentScoring import run as getPointCasual
from phongGiai import run as getPointLeague
from point.casualPoint import run as casualPoint
from point.leaguePoint import run as leaguePoint
from selenium.webdriver.chrome.webdriver import WebDriver
import sys

def Casual():
    getPointCasual()
    casualPoint()

def League():
    getPointLeague()
    leaguePoint()

def exit(driver: WebDriver):
    print("Thoát.")
    driver.quit()
    sys.exit()

options = {
    "1": Casual,
    "2": League,
    "3": exit
}

if __name__ == "__main__":
    # Cần sửa lại hàm getInfo() để nhận thông tin nhập từ bàn phím
    while True:
        print("\n===== MENU =====")
        print("1. Tìm kiếm phòng thường")
        print("2. Tìm kiếm phòng giải")
        print("3. Thoát")

        choice = input("Nhập lựa chọn: ").strip()
        action = options.get(choice)
        if action:
            action()
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập lại!")