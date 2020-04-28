from flask import Flask, render_template, request, session
import pyrebase
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b1gk3y'

config = {
  "apiKey": "AIzaSyDSdsT2h6wAlkQI3rj7sAbPD2a0hFJVIIA",
  "authDomain": "mathtutorapp-f3ddc.firebaseapp.com",
  "databaseURL": "https://mathtutorapp-f3ddc.firebaseio.com",
  "storageBucket": "mathtutorapp-f3ddc.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

teach = ''

class aLesson:
    def __init__(self, topic, video, quiz, quizno):
        self.topic = topic
        self.video = video
        self.quiz = quiz
        self.quizno = quizno

def signIn(email, password):
	user = auth.sign_in_with_email_and_password(email, password)
	return user

def signUp(email, password):
    auth.create_user_with_email_and_password(email, password)

@app.route("/", methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route("/new_user", methods = ['POST'])
def signup():
    email = request.form.get("email_up")
    password = request.form.get("password_up")
    signUp(email,password)
    return render_template('new_user.html')

@app.route("/student", methods = ['POST','GET'])
def signin():
	if request.method == "POST":
		email = request.form.get("email_in")
		password = request.form.get("password_in")
		user = signIn(email,password)
		session['user'] = user
		username = email.split('@')[0]
		session['username'] = username
		teachers = db.child("users").get()
		allTeachers = []
		for teacher in teachers.each():
			allTeachers.append(teacher.key())
		return render_template('student.html', username=username, allTeachers=allTeachers)
	else:
		usr = session.get('username')
		teachers = db.child("users").get()
		allTeachers = []
		for teacher in teachers.each():
			allTeachers.append(teacher.key())
		return render_template('student.html', username=usr, allTeachers=allTeachers)

@app.route("/lessons", methods = ['POST','GET'])
def showLessons():
	if request.method == "POST":
		select = request.form.get('selector')
		global teach
		teach = select
		lessonSet = db.child("users").child(select).get()
		lessonCollection = []
		for lesson in lessonSet.each():
			lessonCollection.append(lesson.key())
		return render_template('lessons.html', username=select, lessonCollection=lessonCollection)
	else:
		username = teach
		lessonSet = db.child("users").child(username).get()
		lessonCollection = []
		for lesson in lessonSet.each():
			lessonCollection.append(lesson.key())
		return render_template('lessons.html', username=username, lessonCollection=lessonCollection)

@app.route("/learn", methods = ['POST'])
def learn():
    username = teach
    select = request.form.get('selector')
    x = db.child("users").child(username).child(select).get().val()
    display = json.loads(x)
    final = aLesson(display["topic"], display["video"], display["quiz"], display["quizno"])
    return render_template('learn.html', lessonplan1 = final)

if __name__ == '__main__':
    app.run(debug=True)
