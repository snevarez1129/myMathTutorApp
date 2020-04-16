from flask import Flask, render_template, request, session
import json
app = Flask(__name__)

app.config['SECRET_KEY'] ='b1gk3y'

class lessons:
    def __init__(self, topic, video, quiz):
        self.topic = topic
        self.video = video
        self.quiz = quiz

@app.route("/")
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
    qDict = {}
    for i in range(noquestions):
        question = request.form.get("q{}".format(i+1))
        print(question)
        answer = request.form.get("a{}".format(i+1))
        print(answer)
        qDict[question] = answer
    l1 = lessons(lesson,video,qDict)
    y = json.dumps(l1.__dict__)
    
    return render_template('test3.html', lessonplan = y, lessonplan1 = l1)

if __name__ == '__main__':
    app.run(debug=True)