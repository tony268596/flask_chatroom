from flask import request
from flask_socketio import emit

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
        print("userfull")
    else:
        users[username] = (request.sid, colorsett[-1])
        colorsett.pop()

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
        tmptime = time.split(",")
        time1, time2 = tmptime[0], tmptime[0] if len(tmptime) == 1 else tmptime[1]
        if tmp != "add"and tmp != "del" and tmp != "pri":
            emit("error", f"syntax error")
        else:
            if tmp == "add":
                y_lael = weektolocate(date)
                start, end = timetolocate(time)
                for i in range(start, end+1):
                    #找list中有沒有這時間使用者
                    check = find_username((i, y_lael), lock[str(y_lael)])
                    if check:
                        emit("error", f"collison with {check}'s private time")
                    else:
                        emit("light_table", {"locate":(i, y_lael), "color":"rgb" + "(241, 167, 167)"}, broadcast=True)
                        emit("chat", {"message":f"{user} add project time {time1} to {time2}", "color":"rgb" + "(241, 167, 167)"}, broadcast=True)
            elif tmp == "del":
                y_lael = weektolocate(date)
                start, end = timetolocate(time)
                for i in range(start, end+1):
                    tmp = find_username((i, y_lael), lock[str(y_lael)])
                    if username == tmp:
                        lock[str(y_lael)].pop((i, y_lael, tmp))
                        emit("light_table", {"locate":(i, y_lael), "color":"white"}, broadcast=True)
                        emit("chat", {"message":f"{tmp} add project time {time1} to {time2}", "color":"black"}, broadcast=True)
                    ## username不在lock 中 == 沒有東西/是lab的東西
                    # elif tmp == False:
                    #     emit("light_table", {"locate":(i, y_lael), "color":"white"}, broadcast=True)
                    else:
                        emit("error", f"can't delete {tmp}'s private time")
            elif tmp == "pri":
                y_lael = weektolocate(date)
                start, end = timetolocate(time)
                for i in range(start, end+1):
                    lock[str(y_lael)].append((i, y_lael, username))
                    emit("light_table", {"locate":(i, y_lael), "color":"rgb" + f"{color}"}, broadcast=True)
                    emit("chat", {"message":f"{user} add project time {time1} to {time2}", "color":"rgb" + f"{color}"}, broadcast=True)
    else:
        emit("chat", {"message": message, "username": username, "color":"rgb" + f"{color}"}, broadcast=True)

# @socketio.on("last_message")
# def backtolastmessage():


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

