import os
from flask import Flask, render_template, request, url_for,redirect
from flask_dance.consumer import OAuth2ConsumerBlueprint
from enum import Enum
from flaskXMLRPC import XMLRPCHandler
from Video_DB import *
from QA_DB import *
from User_DB import *
from flask import session

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')

#necessary so that our server does not need https
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


#Go to FENIX -> Pessoal ->  Aplicações Externas   -> Gerir Aplicações
#Go to FENIX -> Personal -> External Applications -> Manage Applications
#Click Criar / Create
#Fill the form with the following inforamrion:
#      Namè - name of your Application
#      Description - description of your Application
#      Site - http://127.0.0.1:5000/    !!!!!!!! copy from the conselo when running the application
#      Redirect URL - http://127.0.0.1:5000/fenix-example/authorized   !!!!!!! the endpoint should be exactly this one
#      Scopes - Information
# Create the new application recold
# Click details do get the Client Id and Client Secret and fille the next constructor
app = Flask(__name__)
app.secret_key = "supersekrit123"  # Replace this with your own secret!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
fenix_blueprint = OAuth2ConsumerBlueprint(
    "fenix-example", __name__,
    # this value should be retrived from the FENIX OAuth page
    client_id="1132965128044812",
    # this value should be retrived from the FENIX OAuth page
    client_secret="Zg7fvVe2t71y0FvZ5fjGnS7/R1zJ/wsQ7ghZqbSe/ttIV432CCMk8/DkRg3tV9ab5zd+/Ebcpp62G+UYqgT+NA==",
    # do not change next lines
    base_url="https://fenix.tecnico.ulisboa.pt/",
    token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
    authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
)

app.register_blueprint(fenix_blueprint)


@app.route('/')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    print(fenix_blueprint.session.authorized)
    print("Access token: "+ str(fenix_blueprint.session.access_token))
    if fenix_blueprint.session.authorized == True:
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        data = resp.json() 
        print(resp.json())
        newUser(data['name'],data['username'])
    return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)



@app.route('/logout')
def logout():
    # this clears all server information about the access token of this connection
    res = str(session.items())
    print(res)
    session.clear()
    res = str(session.items())
    print(res)
    # when the browser is redirected to home page it is not logged in anymore
    return redirect(url_for("home_page"))

    

@app.route('/private')
def private_page():
    #this page can only be accessed by a authenticated user
    # verification of the user is  logged in
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for("fenix-example.login"))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json() 
        print(resp.json())
        return render_template("privPage.html", username=data['username'], name=data['name'])



@app.route("/API/")
def index():
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for("fenix-example.login"))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json() 
        print(resp.json())
        return render_template('videoList.html')

@app.route("/API/videoList/", methods=['POST'])
def createNewVideo():
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #res contains the responde made to /api/fenix/vi/person (information about current user)
        data = resp.json() 
        print(resp.json())
        ret = newVideo(j["description"], j['url'],data['username'])
        video_inc(data['username'])  #incremets the number of videos by this user
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
    videos = listVideosDICT()
    for v in videos:
        v['QA'] = getNumberOfQuestionsByVideo(v['video_id'])
    return {"videos": videos}

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
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        data = resp.json() 
        print(resp.json())
        ret = newQuestion(j["time"], j['description'],id,data['username'])
        question_inc(data['username']) #incremets the number of questions by this user
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/<int:Vid>/Questions/<int:Qid>/", methods=['GET'])
def getQuestion(Vid,Qid):
    Q = getQuestionDICT(Qid)
    U = getUserDICT(Q["user"])
    Q["user"] = U["user_id"]+' '+U["name"]
    return {"question": Q}
    
@app.route("/API/<int:Vid>/Questions/<int:Qid>/Answers/", methods=['GET'])
def getQuestionAnswers(Vid,Qid):
    A = getAnswersfromQuestionDICT(Qid)
    return {"answers": A}

@app.route("/API/users/userID", methods=['GET'])
def getUserFromID(userID):
    U = getUserFromIDDICT(userID)
    return {"user": U}

@app.route("/API/<int:Vid>/Questions/<int:Qid>/Answers/", methods=['POST'])
def createNewAnswer(Vid,Qid):
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        data = resp.json() 
        print(resp.json())
        ret = newAnswer(j["description"], Qid,data['username'])
        answers_inc(data['username'])   #incremets the number of questions by this user
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)