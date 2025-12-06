"""
Mô tả: giả sử có 2 team, mỗi team có 4 thành viên, mỗi thành viên có 1 id
Yêu cầu: xác định độ tương đồng giữa 2 team dựa trên id của các thành viên trong team
Ý tưởng: sử dụng thuật toán Jaccard similarity để tính độ tương đồng giữa 2 team
"""
import json
DATABASE = r"E:\GetPoint\url\JSON\matches.json"
RESULT = r"E:\GetPoint\url\JSON\result.json"

# Chuẩn hóa id, trả về danh sách kiểu list dictionary
def normalizeId(text):
    """
    Chuẩn hóa ID từ chuỗi text thành list dictionary
    
    Args:
        text1, text2, text3, text4: Chuỗi chứa ID của các team
    
    Returns:
        List[dict]: Danh sách các team với ID đã chuẩn hóa
    """
    raw_ids = text.split(" - ")

    result = []
    for raw_id in raw_ids:
        # 2. Loại bỏ ký tự thừa "**" ở cuối mỗi ID và xóa khoảng trắng (nếu có)
        clean_id = raw_id.strip().replace("**", "")

        # 3. Tạo dictionary với key là 'id' và thêm vào list result
        if clean_id: # Đảm bảo ID không rỗng
            result.append(clean_id)

    return result

def similarity(team1, team2):
    """
    Tính độ tương đồng Jaccard giữa 2 team
    
    Công thức: J(A,B) = |A ∩ B| / |A ∪ B|
    - A ∩ B: Số thành viên chung
    - A ∪ B: Tổng số thành viên không trùng lặp
    
    Args:
        team1, team2: List ID của 2 team
    
    Returns:
        float: Độ tương đồng (0-1)
    """
    t1 = set(team1)
    t2 = set(team2)
    return len(t1.intersection(t2)) / len(t1.union(t2))

def compare(similarity_score: float):
    """
    So sánh và đưa ra kết luận dựa trên ngưỡng
    
    Args:
        similarity_score: Điểm tương đồng
        threshold: Ngưỡng để xác định giống nhau (mặc định 0.4)
    """
    threshold = 0.01
    if (similarity_score > threshold):
        return True
    else:
        return False

def process():
    with open(DATABASE, 'r', encoding='utf-8') as file:
        allGame = json.load(file)
    result = []
    for game in allGame:
        team1 = normalizeId(game["id"])
        check = 0 # kiểm tra tồn tại Team trong dữ liệu hay chưa
        # Kiem tra neu trong du lieu co None thi dat ve bang 0
        if game["point"] == None:
            game["point"] = "0"
        if game["elim"] == None:
            game["elim"] = "0"
        for r in result:
            team2 = normalizeId(r["id"])
            if r["point"] == None:
                r["point"] = "0"
            if r["elim"] == None:
                r["elim"] = "0"
            if compare(similarity(team1, team2)) == True: # Kiem tra 2 team co phai la 1 hay khong
                point = int(r["point"]) + int(game["point"])
                elim = int(r["elim"]) + int(game["elim"])
                by = int(r["by"]) + int(game["by"])
                r["point"] = str(point)
                r["elim"] = str(elim)
                r["by"] = str(by)
                check+=1
                break
        if check == 0: # Trạng thái khác 0 tức là đã tồn tại Team trong dữ liệu
            result.append({
                "id": game["id"],
                "name": game["name"],
                "by": game["by"],
                "elim": game["elim"],
                "point": game["point"]
            })
    return result

def run():
    result = process()
    sorted_result = sorted(result, key=lambda item: int(item['point']), reverse=True)
    
    with open(RESULT, 'w', encoding='utf-8') as file:
        json.dump(sorted_result, file, ensure_ascii=False, indent=4)
        print("OK!")

    i = 1
    for r in sorted_result:
        print(f"Top {i}")
        i+=1
        print(f"{r["name"]:}\nBOOYAH: {r["by"]}\nElim: {r["elim"]}\nPoint: {r["point"]}\n")
    # delete()

def delete():
    newData = []
    with open(RESULT, 'w', encoding='utf-8') as file:
        json.dump(newData, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run()