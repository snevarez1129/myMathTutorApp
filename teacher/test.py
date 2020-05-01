from flask import Flask, render_template, request, session
import pyrebase
import json
app = Flask(__name__)

app.config['SECRET_KEY'] ='b1gk3y'

config = {
  "apiKey": "AIzaSyDSdsT2h6wAlkQI3rj7sAbPD2a0hFJVIIA",
  "authDomain": "mathtutorapp-f3ddc.firebaseapp.com",
  "databaseURL": "https://mathtutorapp-f3ddc.firebaseio.com",
  "storageBucket": "mathtutorapp-f3ddc.appspot.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()

def signIn(email,password):
    user = auth.sign_in_with_email_and_password(email,password)
    return user

def signUp(email,password):
    auth.create_user_with_email_and_password(email,password)

class lessons:
    def __init__(self, topic, video, quiz, quizno):
        self.topic = topic
        self.video = video
        self.quiz = quiz
        self.quizno = quizno

@app.route("/", methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route("/signin", methods = ['POST'])
def signin():
    email = request.form.get("email_in")
    password = request.form.get("password_in")
    user = signIn(email,password)
    session['user'] = user
    username = email.split('@')[0]
    session['username'] = username
    return render_template('home.html', email = email)

@app.route("/signup", methods = ['POST'])
def signup():
    email = request.form.get("email_up")
    password = request.form.get("password_up")
    signUp(email,password)
    return render_template('signup.html')

@app.route("/lessoncreator", methods = ['POST'])
def test():
    return render_template('test.html')


@app.route('/quizcreator', methods = ['POST'])
def quizcreator():
    lesson = request.form.get("lesson")
    video = request.form.get("video")
    noquestions = int(request.form.get("noquestions"))
    session['lesson'] = lesson
    session['video'] = video
    session['noquestions'] = noquestions
    return render_template('test2.html', noquestions = noquestions)

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
    l1 = lessons(lesson,video,qDict,noquestions)
    y = json.dumps(l1.__dict__)
    db.child("users").child(username).child(lesson).set(y, user['idToken'])
    return render_template('complete.html')

@app.route("/collection", methods = ['POST'])
def collection():
    username = session.get('username')
    lessonset = db.child("users").child(username).get()
    lessonCollection = []
    for lesson in lessonset.each():
        lessonCollection.append(lesson.key())
    return render_template('collection.html',username = username, lessonCollection = lessonCollection)

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
    return render_template('test3.html', lessonplan1 = final)

if __name__ == '__main__':
    app.run(debug=True)