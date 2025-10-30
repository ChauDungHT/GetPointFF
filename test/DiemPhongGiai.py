"""
Mô tả: giả sử có 2 team, mỗi team có 4 thành viên, mỗi thành viên có 1 id
Yêu cầu: xác định độ tương đồng giữa 2 team dựa trên id của các thành viên trong team
Ý tưởng: sử dụng thuật toán Jaccard similarity để tính độ tương đồng giữa 2 team
"""
import json
DATABASE = r"E:\GetPoint\url\matches.json"
RESULT = r"E:\GetPoint\url\result.json"

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
    threshold = 0.9
    if (similarity_score > threshold):
        return True
    else:
        return False

def process():
    with open(DATABASE, 'r', encoding='utf-8') as file:
        allGame = json.load(file)
    result = []
    for game in allGame:
        team1 = game["name"]
        check = 0
        if game["point"] == None:
            game["point"] = "0"
        if game["elim"] == None:
            game["elim"] = "0"
        for r in result:
            team2 = r["name"]
            if r["point"] == None:
                r["point"] = "0"
            if r["elim"] == None:
                r["elim"] = "0"
            if compare(similarity(team1, team2)) == True:
                point = int(r["point"]) + int(game["point"])
                elim = int(r["elim"]) + int(game["elim"])
                by = int(r["by"]) + int(game["by"])
                r["point"] = str(point)
                r["elim"] = str(elim)
                r["by"] = str(by)
                check+=1
                break
        if check == 0:
            result.append({
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
        print(f"{r["name"]:}\nBOOYAH: {r["by"]}\npoint: {r["point"]}\nelim: {r["elim"]}\n")
        i+=1
    delete()

def delete():
    newData = []
    with open(RESULT, 'w', encoding='utf-8') as file:
        json.dump(newData, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run()