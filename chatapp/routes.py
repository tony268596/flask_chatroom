'''
負責路由
'''
import chatapp.tmp
from flask import Blueprint, render_template

# 建主要router名稱
main = Blueprint("main", __name__)

@main.route("/")
def index():
    tmp = chatapp.tmp.read_json_file("tmp.json")
    return render_template("index.html", data = tmp)