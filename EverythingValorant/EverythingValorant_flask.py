from asyncio.windows_events import NULL
from flask import Flask,g,render_template,session,url_for,redirect,request
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b"husaiflh"
DATABASE = "everythingvalorant.db"


def get_db():#Connect to the database
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext#Closing the connection to database in order to not lock it
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")#Homepage that will show splash art for Valorant game.
def home():
    session["admin"] = NULL
    return render_template("homepage.html")

@app.route("/agents")#Route that will display all the data from the agents table
def agents():
    cursor = get_db().cursor()
    sql = "SELECT * FROM agents" #Selecting all data from the agents table
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("agents.html", results=results,)#Collected data is passed as a variable to the agents html template

@app.route("/signatures")#Route that will display all the data from the signature_ability_e table
def signatures(): 
    cursor = get_db().cursor()
    sql = """SELECT e.ability_name, e.ability_function, agents.agent_name, e.max_charges, e.cost, e.recharge_time, e.image_filename
        FROM signature_ability_e e JOIN agents ON e.agent_number = agents.agent_number"""
    #SQL statement that selects all data from signature_ability_e table with a join statement that replaces the agent number with the agent name.
    cursor.execute(sql)
    results = cursor.fetchall()#Collected data is converted to a variable
    return render_template("signatures.html", results=results)#Data is returned as a variable to the signatures.html template

@app.route("/basic")#Route that will display all the data from the basic_ability_c and basic_ability_q table in 2 tables
def basic():
    cursor = get_db().cursor()
    sql = """SELECT c.ability_name, c.ability_function, agents.agent_name, c.max_charges, c.cost, c.image_filename
        FROM basic_ability_c c JOIN agents ON c.agent_number = agents.agent_number"""
    #SQL statement that selects all data from basic_ability_c table with a join statement that replaces the agent number with the agent name.
    cursor.execute(sql)
    results_c = cursor.fetchall()#Collected data is converted to a variable
    sql = """SELECT q.ability_name, q.ability_function, agents.agent_name, q.max_charges, q.cost, q.image_filename
        FROM basic_ability_q q JOIN agents ON q.agent_number = agents.agent_number"""
    #SQL statement that selects all data from basic_ability_q table with a join statement that replaces the agent number with the agent name.
    cursor.execute(sql)
    results_q = cursor.fetchall()#Collected data is converted to a variable
    return render_template("basic.html", results_c=results_c, results_q=results_q)#Collected data are returned as variables to the basic.html template

@app.route("/ultimate")#Route that will display all the data from the ultimate_ability_x table
def ultimate():
    cursor = get_db().cursor()
    sql = """SELECT x.ability_name, x.ability_function, agents.agent_name, x.ult_points, x.image_filename
        FROM ultimate_ability_x x
        JOIN agents ON x.agent_number = agents.agent_number"""
    #SQL statement that selects all data from ultimate_ability_x table with a join statement that replaces the agent number with the agent name.
    cursor.execute(sql)
    results = cursor.fetchall()#Collected data is converted to a variable
    print(results)
    return render_template("ultimates.html", results=results,)#Data is returned as a variable to the ultimates.html template

@app.route("/create", methods=["GET", "POST"])#Posting page to create a new post
def create():
    cursor = get_db().cursor()
    sql = "SELECT agents.image_filename, agents.agent_name FROM agents"
    #Selecting all agent images to be used for profile picture values, agent names to be used for profile picture options
    cursor.execute(sql)
    pictures = cursor.fetchall()#Collected data is returned to a variable
    print(pictures)
    if request.method == "POST":
        cursor = get_db().cursor()
        username = request.form["user_name"] #Get results of various forms in create page
        profile_picture = request.form["user_picture"]
        agent_number = request.form["agent_number"]
        rank_picture = request.form["user_rank"]
        sql = "INSERT INTO posts(username, profile_picture, agent_number, rank_picture) VALUES(?,?,?,?)"#Insert data into database
        cursor.execute(sql,(username, profile_picture, agent_number, rank_picture))
        get_db().commit()
        return redirect("/posts")#Redirect to page with all posts
    return render_template("create.html", pictures=pictures)#Returns the create template with the collected data

@app.route("/posts")
def posts():
    cursor = get_db().cursor()
    sql = "SELECT * FROM posts"#Sql statement that selects all data from posts
    cursor.execute(sql)
    results = cursor.fetchall()
    if session["admin"] == "V4lorant": #If user inputted the right password
        authorised = True #The authorised variable is set to true in order to give the user access to admin tools
        return render_template("posts.html", results=results, authorised=authorised)
    else:
        return render_template("posts.html", results=results)


@app.route("/admin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["admin"] = request.form["password"]#The admin is given to the 
        if session["admin"] != "V4lorant":#If the password is incorrect
            authorised = False#User is not given access to admin tools and has to try again
            return render_template("admin.html", authorised=authorised)
        else:#If password is correct
            return redirect(url_for("posts"))#User is redirected to posts page where they can delete posts.
    return render_template("admin.html")

@app.route("/delete", methods=["GET", "POST"])#Route that will delete a post from the database
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        post_number = int(request.form["post_number"])#The primary key of the post is returned
        sql = ("DELETE FROM posts WHERE post_id=?")#Sql statement that will delete the post according to the id returned
        cursor.execute(sql,(post_number,))
        get_db().commit()
    return redirect("/posts")#User stays on the post page as there is no need to render other templates.

@app.route("/logout")
def logout():
    # remove the admin from the session if it's there
    session.pop("admin", None)
    return redirect(url_for("home"))

@app.route("/info/<string:agent_name>")#Dynamic routing that will show all info related to a signle agent
def info(agent_name):
    cursor = get_db().cursor()
    sql = """SELECT agents.*, basic_ability_c.ability_name, basic_ability_q.ability_name, signature_ability_e.ability_name, ultimate_ability_x.ability_name FROM agents
        JOIN basic_ability_c ON basic_ability_c.agent_number = agents.agent_number
        JOIN basic_ability_q ON basic_ability_q.agent_number = agents.agent_number
        JOIN signature_ability_e ON signature_ability_e.agent_number = agents.agent_number
        JOIN ultimate_ability_x ON ultimate_ability_x.agent_number = agents.agent_number
        WHERE agent_name = ? 
    """
    #Selects relevant data from agents table where the agent name matches that in the url
    cursor.execute(sql,(agent_name,))
    agent = cursor.fetchall()#Collected data is stored in a variable
    return render_template("info.html", results=agent,)#Variable is returned to the info.html template

if __name__ == "__main__":
    app.run(debug=True)