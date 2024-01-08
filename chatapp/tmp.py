import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def init_table(file_path, arr):
    data = read_json_file(file_path)

    # 檢查 "table" 鍵是否存在，如果不存在則創建一個空列表
    if "table" not in data:
        data["table"] = []

    # 向 "table" 列表中添加新項目
    data["table"] = arr
    # 將更新後的數據寫回 JSON 文件
    write_json_file(file_path, data)

## 將message寫進.json
def add_to_chat(file_path, dic):
    data = read_json_file(file_path)
    data["message"].append(dic)
    write_json_file(file_path, data)

## 將locate存入table
def write_to_table(file_path, usr):
    data = read_json_file(file_path)
    data["table"] = usr
    write_json_file(file_path, data)

def load_table(file_path):
    data = read_json_file(file_path)
    return data["table"]

def user_color(file_path, usr, color):
    data = read_json_file(file_path)
    data["user"][usr] = color
    write_json_file(file_path, data)

def reset_storage(file_path, zz):
    write_json_file(file_path, zz)
