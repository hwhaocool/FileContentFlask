#coding:utf-8

from flask import Flask, render_template, url_for, render_template_string
import sys, os
import re
from MyMarkDown import MyMarkDown

app = Flask(__name__)
# Markdown(app)

html = """
<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Log Type For %s</title>
    </head> 
    <body>
    %s
    </body>
</html>
"""

#public static enum LogType 的正则表达式
log_enum_pattern = re.compile("public\s+static\s+enum\s+LogType\s*{")

def getB():
    print("get b")
    return getFileContent("b")

def getC():
    print("get c")
    return getFileContent("c")

def getFileContent(log_type):
    if log_type == "b":
        file_path = "/home/jenkins/workspace/xxxx/api/constant/Constants.java"
        type_name = "B"
    else:
        file_path = "/home/jenkins/workspace/xxx/constant/Constants.java"
        type_name = "C"

    c_file = open(file_path, 'r+')

    is_found = False

    my_mark_down = MyMarkDown()

    c_log_content = ""
    for data in c_file.readlines():
        data = data.decode("utf-8").strip()

        if not is_found:
            if data.startswith("public") and log_enum_pattern.match(data):
                is_found = True
                c_log_content += data + "<br>"
                my_mark_down.addLineByString(data)
        else:
            # print data
            if data.startswith("private"):
                #end
                break
            c_log_content += data  + "<br>"
            my_mark_down.addLineByString(data)

    c_file.close()

    return render_template("log.html", type=type_name, content=my_mark_down.getAll())


@app.route('/')
def root():
    return index()

@app.route('/index')
def index():
    return "please visit /b or /c"

@app.route('/b')
def b():
    return getB()

@app.route('/c')
def c():
    return getC()

if __name__ == '__main__':
    app.debug = True
    #监听 所有ip
    app.run(host='192.168.2.100', port=8083)