from flask import Flask, request, render_template
import os
import psycopg2

app = Flask(__name__)

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
