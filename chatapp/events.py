from flask import request
from flask_socketio import emit

from .extensions import socketio

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

# 收到new message 指令，回傳一行dist給chat
@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    if message[:2] == "@@":
        tmp = message.split(" ")[1]
        ret = (int(tmp[0]), int(tmp[1])) ## 定位
        print(ret)
        emit("light_table", {"locate":ret})
    else:
        username = None 
        for user in users:
            if users[user] == request.sid:
                username = user
        emit("chat", {"message": message, "username": username}, broadcast=True)