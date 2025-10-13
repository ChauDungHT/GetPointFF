"""
Mô tả: giả sử có 2 team, mỗi team có 4 thành viên, mỗi thành viên có 1 id
Yêu cầu: xác định độ tương đồng giữa 2 team dựa trên id của các thành viên trong team
Ý tưởng: sử dụng thuật toán Jaccard similarity để tính độ tương đồng giữa 2 team
"""

# Kết quả đúng: 4 team đều là 1 team
text1 = "5252523** - 15313170** - 33755893** - 12712366**"
text2 = "5252523** - 5979934** - 15313170** - 33755893**"
text3 = "1260584** - 33755893** - 15313170** - 5252523**"
text4 = "15313170** - 5252523** - 12712366** - 33755893**"

text = [text1, text2, text3, text4]

# Chuẩn hóa id, trả về danh sách kiểu list dictionary
def normalizeId(text):
    """
    Chuẩn hóa ID từ chuỗi text thành list dictionary
    
    Args:
        text1, text2, text3, text4: Chuỗi chứa ID của các team
    
    Returns:
        List[dict]: Danh sách các team với ID đã chuẩn hóa
    """
    list_player = []
    teamNumber = 1
    for i in text:
        players = i.split("** - ")
        players[3] = players[3].strip("**")
        list_player.append({
            "TeamID": teamNumber,
            "id1": players[0],
            "id2": players[1],
            "id3": players[2],
            "id4": players[3]
        })
        teamNumber+=1
    return list_player


def vectorID(list):
    """
    Chuyển đổi dictionary thành vector (list) để dễ xử lý
    
    Args:
        list: Danh sách team dạng dictionary
    
    Returns:
        List[List[str]]: Danh sách các team dạng vector
    """
    vector = []
    for l in list:
        team = [
            l["id1"],
            l["id2"],
            l["id3"],
            l["id4"]
        ]
        vector.append(team)
    return vector


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
    threshold = 0.4
    if (similarity_score > threshold):
        print("Hai team giống nhau")
    else:
        print("Không cùng một team")

if __name__ == "__main__":
    list = normalizeId(text)
    vector = vectorID(list)
    compare(similarity(vector[1], vector[0]))