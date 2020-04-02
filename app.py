from flask import Flask, render_template, url_for
import requests
import student as s

app = Flask(__name__)

def signin():
    return 1

@app.route('/')
def index():
    user = signin()
    if (user == 1):
        stu = s.student()
        resp = stu.chatbot()
    else:
        print("ERROR")
    return resp

if __name__ == "__main__":
    app.run(debug=True)
