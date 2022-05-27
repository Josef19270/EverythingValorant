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

@app.route("/signatures")
def signatures():
    cursor = get_db().cursor()
    sql = "SELECT e.ability_name, e.ability_function, agents.agent_name, e.max_charges, e.cost, e.recharge_time FROM signature_ability_e e JOIN agents ON e.agent_number = agents.agent_number"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("signatures.html", results=results,)

@app.route("/basic")
def basic():
    cursor = get_db().cursor()
    sql = "SELECT * FROM basic_ability_c"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("basic.html", results=results)

@app.route("/ultimate")
def ultimate():
    cursor = get_db().cursor()
    sql = "SELECT x.ability_name, x.ability_function, agents.agent_name, x.ult_points FROM ultimate_ability_x x JOIN agents ON x.agent_number = agents.agent_number"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("ultimates.html", results=results,)

if __name__ == "__main__":
    app.run(debug=True)