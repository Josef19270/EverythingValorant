from flask import Flask,g,render_template
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'husaiflh'
DATABASE = 'everythingvalorant.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/agents")
def agents():
    cursor = get_db().cursor()
    sql = "SELECT * FROM agents"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("agents.html", results=results,)

if __name__ == "__main__":
    app.run(debug=True)