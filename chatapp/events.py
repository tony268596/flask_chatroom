from flask import request
from flask_socketio import emit
import chatapp.tmp as trans
import chatapp.setting as setting
from .extensions import socketio

users = {}
colorsett = [(16,109,156),
             (90,146,173),
             (0,162,222),
             (8,186,255),
             (255,97,0),
             (61,89,171),
             (128,42,42)]

# 用dict存他搜尋比較快
lock = {"1":[], "2":[], "3":[],"4":[], "5":[], "6":[],"7":[]}
lastcommand = []

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    if len(colorsett) == 0:
        emit("error", "userfull")
    else:
        users[username] = (request.sid, colorsett[-1])
        trans.user_color(setting.storage, username, f"rgb{colorsett[-1]}")
        colorsett.pop()

        data = trans.read_json_file(setting.storage)
        usr = data.get("user", [])
        emit("update_users", usr, broadcast=True)

# 收到new message 指令，回傳一行dist給chat
@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    lastcommand.append(message)
    username = None 
    for user in users:
        if users[user][0] == request.sid:
            username = user
            color = users[user][1]
    print(lock)
    if message[:2] == "@@":
        message = message[2:]
        tmp = message.split(" ")[0]
        date = message.split(" ")[1]
        time = message.split(" ")[2]
        ## 
        time1, time2 = timetolocate(time)
        ## 這裡把table存進來了
        mat = trans.load_table(setting.storage)
        ccc = 0 # 衝突check
        if tmp != "add"and tmp != "del" and tmp != "pri":
            emit("error", f"syntax error")
        else:
            if tmp == "add":
                y_lael = weektolocate(date)
                start, end = timetolocate(time)

                # check 是否有使用者
                for i in range(start, end+1):
                    if mat[i][y_lael]:
                        ccc = 1
                if ccc: #有衝突
                    emit("error", f"collison with {mat[i][y_lael]}'s private time")#############################################
                else: #無衝突
                    for i in range(start, end+1):
                        mat[i][y_lael].append("Project")
                        emit("light_table", {"locate":(i, y_lael), "color":"rgb" + "(241, 167, 167)"}, broadcast=True)
                    trans.write_to_table(setting.storage, mat) # 卡進.json
                    emit("chat", {"message":f"{username} add project time {time1+7} to {time2+7}", "color":"rgb" + "(241, 167, 167)"}, broadcast=True)
                ccc = 0
            elif tmp == "del":
                y_lael = weektolocate(date)
                start, end = timetolocate(time)
                for i in range(start, end+1):
                    if mat[i][y_lael]:
                        ccc = 1
                if username not in mat[i][y_lael]: # 有衝突
                        emit("error", f"can't delete {mat[i][y_lael]}'s private time")
                else: # 無衝突
                    for i in range(start, end+1):
                        mat[i][y_lael].remove(username)
                        emit("light_table", {"locate":(i, y_lael), "color":"white"}, broadcast=True)
                    trans.write_to_table(setting.storage, mat)
                    emit("chat", {"message":f"{username} delete time {time1+7} to {time2+7}", "color":"black"}, broadcast=True)
                ccc = 0
            elif tmp == "pri":
                # done
                y_lael = weektolocate(date)
                start, end = timetolocate(time)
                for i in range(start, end+1):
                    mat[i][y_lael].append(username)
                    emit("light_table", {"locate":(i, y_lael), "color":"rgb" + f"{color}"}, broadcast=True)
                emit("chat", {"message":f"{username} add private time {time1+7} to {time2+7}", "color":"rgb" + f"{color}"}, broadcast=True)
                trans.write_to_table(setting.storage, mat)
    else:
        # done
        text = {"message": message, "username": username, "color":"rgb" + f"{color}"}
        emit("chat", text, broadcast=True)
        trans.add_to_chat(setting.storage, text)



def weektolocate(str):
    tmp = str.lower()
    if tmp == "mon" or  tmp =="mo":
        return 1
    elif tmp == "tues" or tmp == "tu":
        return 2
    elif tmp == "wed" or  tmp =="we":
        return 3
    elif tmp == "thur" or tmp == "th":
        return 4
    elif tmp == "fri" or  tmp =="fr":
        return 5
    elif tmp == "sat" or  tmp =="sa":
        return 6
    elif tmp == "sun" or  tmp =="su":
        return 7
    else:
        emit("error", "date is not valid")

def timetolocate(str):
    tmp = [int(i)-7 for i in str.split(",")]
    if tmp[0] < 1:
        emit("error", "time is not valid")
    if len(tmp) == 1:
        return tmp[0], tmp[0]
    else:
        return tmp[0], tmp[1]
    
def find_username(start_end, time_list):
    for i in time_list:
        start = i[0]
        end = i[1]
        username = i[2]
        if (start, end) == start_end:
            return username
    return False

