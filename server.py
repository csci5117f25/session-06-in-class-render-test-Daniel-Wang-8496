from flask import Flask, redirect, request, render_template, session, url_for
import os
import psycopg2

import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

#auth things

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("hello"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/guestlist', methods=['POST'])
def gfg():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE guest_list (Name varchar(255), Message varchar(255))")
            cur.execute("INSERT INTO guest_list (Name, Message) VALUES (%s, %s)", (name, message))
    conn.close()
    return render_template('index.html', name=name, message=message)
    
