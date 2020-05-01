from flask import Flask, render_template, request, session
import pyrebase
import json

app = Flask(__name__)

app.config['SECRET_KEY'] ='b1gk3y'

#configure initial firebase settings
config = {
  "apiKey": "",
  "authDomain": "mathtutorapp-f3ddc.firebaseapp.com",
  "databaseURL": "https://mathtutorapp-f3ddc.firebaseio.com",
  "storageBucket": "mathtutorapp-f3ddc.appspot.com"
}

#use pYrebase package to use firebase through python and flask
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()

#signin function using pyrebase
def signIn(email,password):
	user = auth.sign_in_with_email_and_password(email,password)
	return user

#signup function using pyrebase
def signUp(email,password):
    auth.create_user_with_email_and_password(email,password)

#class used to store lessons
class lessons:
    def __init__(self, topic, video, quiz, quizno):
        self.topic = topic
        self.video = video
        self.quiz = quiz
        self.quizno = quizno

#landing page for login/signup
@app.route("/", methods = ['POST','GET'])
def index():
    return render_template('index.html')

#signup page
@app.route("/new_user", methods = ['POST'])
def signup():
    email = request.form.get("email_up")
    password = request.form.get("password_up")
    signUp(email,password)
    return render_template('signup.html')

#home page after login
@app.route("/home", methods = ['POST','GET'])
def signin():
	if request.method == "POST":
		email = request.form.get("email_in")
		password = request.form.get("password_in")
		user = signIn(email,password)
		session['user'] = user
		username = email.split('@')[0]
		session['username'] = username
		return render_template('home.html', username=username)
	else:
		usr = session.get('username')
		return render_template('home.html', username=usr)

#lesson creator page
@app.route("/lessoncreator", methods = ['POST'])
def test():
    return render_template('lessoncreator.html')

#quiz creator page
@app.route('/quizcreator', methods = ['POST'])
def quizcreator():
    lesson = request.form.get("lesson")
    video = request.form.get("video")
    noquestions = int(request.form.get("noquestions"))
    session['lesson'] = lesson
    session['video'] = video
    session['noquestions'] = noquestions
    return render_template('quizcreator.html', noquestions = noquestions)

#quiz complete page
@app.route("/complete", methods = ['POST'])
def complete():
    lesson = session.get('lesson')
    video = session.get('video')
    noquestions = session.get('noquestions')
    user = session.get('user')
    username = session.get('username')
    qDict = {}

    for i in range(noquestions):
        question = request.form.get("q{}".format(i+1))
        answer = request.form.get("a{}".format(i+1))
        qDict[question] = answer
    
    #make lesson class
    l1 = lessons(lesson,video,qDict,noquestions)
    y = json.dumps(l1.__dict__)

    #add lesson to database under user
    db.child("users").child(username).child(lesson).set(y, user['idToken'])
    return render_template('complete.html')

#lesson collection page
@app.route("/collection", methods = ['POST'])
def collection():
    username = session.get('username')
    lessonset = db.child("users").child(username).get()
    lessonCollection = []
    for lesson in lessonset.each():
        lessonCollection.append(lesson.key())
    return render_template('collection.html',username = username, lessonCollection = lessonCollection)

#view lesson page
@app.route("/lesson", methods = ['POST'])
def lessoner():
    username = session.get('username')
    select = request.form.get("selector")
    print(username)
    print(select)
    x = db.child("users").child(username).child(select).get().val()
    print(x)
    display = json.loads(x)
    final = lessons(display["topic"], display["video"], display["quiz"], display["quizno"])
    return render_template('lesson.html', lessonplan1 = final)

if __name__ == '__main__':
    app.run(debug=True)
