from flask import Flask, redirect, render_template, url_for, request
import student as s
import functions as f

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def sign_in():
    return render_template('signin.html')

@app.route('/new_user', methods=["POST", "GET"])
def new_user():
    if request.method == "POST":
        name = request.form["myName"]
        email = request.form["myEmail"]
        password = request.form["myPass"]
        school = request.form["mySchool"]
        user = request.form["userMode"]
        err = f.create_new_user(name, email, password, school, user)
        if (err != 1):
            return "ERROR: Could not create a new user"
        return redirect(url_for("student"))
    else:
        return render_template('new_user.html')

@app.route('/student')
def student():
    myStudent = s.student()
    resp = myStudent.chatbot()
    return resp

if __name__ == "__main__":
    app.run(debug=True)
