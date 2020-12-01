import os
from flask import Flask, render_template, request, url_for,redirect
from enum import Enum
from flaskXMLRPC import XMLRPCHandler
from Video_DB import *

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')

@app.route("/API/")
def index():
    return render_template('videoList.html')

@app.route("/API/videoList/", methods=['POST'])
def createNewVideo():
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409
    
@app.route("/API/videoList/", methods=['GET'])
def returnsVideosJSON():
    return {"videos": listVideosDICT()}

@app.route("/API/<int:id>/", methods=['GET'])
def goToVideoPage(id):
    video = getVideoDICT(id)
    title = video["description"]
    src = video["url"]
    return render_template('videoPage.html', title= title, videoID = id, src = src)

@app.route("/API/<int:id>/Questions", methods=['GET'])
def getVideoQuestions(id):
    Q = getQuestionsfromVideoDICT(id)
    return {"questions": Q}

@app.route("/API/<int:id>/Questions/", methods=['POST'])
def createNewQuestion(id):
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        ret = newQuestion(j["time"], j['description'],id)
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)