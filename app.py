from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, url_for
from flask import session

import requests


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
    client_id="1695915081466113",
    # this value should be retrived from the FENIX OAuth page
    client_secret="px416NQ88zaFOsfLIy5GaCP/GUDBNkMZ9JL3ckUhVYanLWicGzsfPRls8r9jCczMAGCTu6phzEOktBo2uzRHtQ==",
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



if __name__ == '__main__':
    app.run(debug=True)
 