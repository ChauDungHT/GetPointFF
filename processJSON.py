import json

def save_to_json(data: list, file_name: str, mode: str = "append"):
    """
    Lưu dữ liệu vào file JSON
    
    Args:
        data: Danh sách dữ liệu cần lưu
        file_name: Tên file
        mode: "append" để thêm vào file cũ, "overwrite" để ghi đè
    """
    try:
        existing_data = []
        
        # Đọc dữ liệu cũ nếu mode là append
        if mode == "append":
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = []
            except FileNotFoundError:
                pass  # File chưa tồn tại
            except json.JSONDecodeError:
                print("File JSON bị lỗi, sẽ ghi đè file mới")
        
        # Gộp dữ liệu mới
        existing_data.extend(data)
        
        # Ghi vào file
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        
        print(f"Đã lưu {len(data)} bản ghi vào file: {file_name}")
        print(f"Tổng số bản ghi trong file: {len(existing_data)}")
        
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")


def save_to_json_individual(data: list, file_name: str):
    """
    Lưu từng trận đấu vào file riêng biệt (alternative approach)
    
    Args:
        data: Dữ liệu trận đấu
        file_name: Tên file gốc
    """
    if not data:
        return
    
    match_id = data[0].get("match_id", "unknown")
    individual_file = f"{file_name.rsplit('.', 1)[0]}_{match_id}.json"
    
    try:
        with open(individual_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Đã lưu trận {match_id} vào file: {individual_file}")
    except Exception as e:
        print(f"Lỗi khi lưu file {individual_file}: {e}")