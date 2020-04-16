from flask import Flask, redirect, render_template, url_for, request
import student as s
import functions as f

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        #verify login credentials
        return redirect(url_for("student"))
    else:
        return render_template('sign-in.html')

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
        return render_template('new-user.html')

@app.route('/student', methods=["POST", "GET"])
def student():
    if request.method == "POST":
        #launch chatbot
    else:
        return render_template('student.html')

if __name__ == "__main__":
    app.run(debug=True)
