from flask import Flask,g,render_template,session,url_for,redirect,request
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
    if 'username' in session:
        return render_template("homepage.html", username=session['username'])
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
    sql = "SELECT e.ability_name, e.ability_function, agents.agent_name, e.max_charges, e.cost, e.recharge_time, e.image_filename FROM signature_ability_e e JOIN agents ON e.agent_number = agents.agent_number"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template("signatures.html", results=results)

@app.route("/basic")
def basic():
    cursor = get_db().cursor()
    sql = "SELECT c.ability_name, c.ability_function, agents.agent_name, c.max_charges, c.cost FROM basic_ability_c c JOIN agents ON c.agent_number = agents.agent_number"
    cursor.execute(sql)
    results_c = cursor.fetchall()
    sql = "SELECT q.ability_name, q.ability_function, agents.agent_name, q.max_charges, q.cost, agents.agent_name FROM basic_ability_q q JOIN agents ON q.agent_number = agents.agent_number"
    cursor.execute(sql)
    results_q = cursor.fetchall()
    return render_template("basic.html", results_c=results_c, results_q=results_q)

@app.route("/ultimate")
def ultimate():
    cursor = get_db().cursor()
    sql = "SELECT x.ability_name, x.ability_function, agents.agent_name, x.ult_points FROM ultimate_ability_x x JOIN agents ON x.agent_number = agents.agent_number"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("ultimates.html", results=results,)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)