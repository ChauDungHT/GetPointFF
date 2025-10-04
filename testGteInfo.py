def getInfo():
    id = 1240104899
    start = "21/09/2025 13:30"
    end = "22/09/2025 00:00"
    return id, start, end

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

if __name__ == "__main__":
    id, start, end = getInfo()

    start_info = parse_date_time(start)
    end_info = parse_date_time(end)

    print(start_info['day'], start_info['month'], start_info['year'], start_info['hour24'], start_info['minute'])
    print(end_info['day'], end_info['month'], end_info['year'], end_info['hour24'], end_info['minute'])




    # Nhấn "Tìm kiếm"
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Tìm kiếm']"))
    )
    search_button.click()