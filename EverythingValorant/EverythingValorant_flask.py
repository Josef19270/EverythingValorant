from flask import Flask,g,render_template
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
def index():
    cursor = get_db().cursor()
    sql = "SELECT * FROM b"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("agents.html", results=results,)

if __name__ == "__main__":
    app.run(debug=True)