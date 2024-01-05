'''
負責路由
'''

from flask import Blueprint, render_template

# 建主要router名稱
main = Blueprint("main", __name__)

@main.route("/")
def index():

    return render_template("index.html")