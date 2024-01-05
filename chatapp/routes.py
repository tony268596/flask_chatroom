'''
負責路由
'''

from flask import Blueprint, render_template

# 建主要router名稱
main = Blueprint("main", __name__)

@main.route("/")
def index():
    table_data = [[i for i in range(7)] for _ in range(9)]
    return render_template("index.html", table_data=table_data)