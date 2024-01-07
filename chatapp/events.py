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

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = (request.sid, colorsett[-1])
    colorsett.pop()

# 收到new message 指令，回傳一行dist給chat
@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    print(users)
    for user in users:
        if users[user][0] == request.sid:
            username = user
            color = users[user][1]

    if message[:2] == "@@":
        tmp = message.split(" ")[1]
        ret = (int(tmp[0]), int(tmp[1])) ## 定位
        print(ret)
        emit("light_table", {"locate":ret, "color":"rgb" + f"{color}"}, broadcast=True)
    else:
        emit("chat", {"message": message, "username": username, "color":"rgb" + f"{color}"}, broadcast=True)