import numbers
import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/addResturants", methods =["GET","POST"])
@login_required
def addResturants():
    #Egyptian Cuisines
    cuisines= ["Koshary","Kabab","Sandwiches","Crepe",
    "Pasta","Foul","Falafel","Kebda","Burger",
    "Fried Chicken","Pizza","Hawawshi","Desserts","Sea Food"
    ]

    if request.method == "POST":
        #Information needed to add a resturant
        resturant = request.form.get("resturant")
        number = request.form.get("number")
        dine_in = request.form.get("dine_in")
        delivery = request.form.get("take_away")
        location = request.form.get("location")
        cuisines = request.form.getlist("cuisine")

        #Making sure that everything isn't null
        if not resturant or not number or dine_in == "None" or delivery == "None" or not location or len(cuisines) == 0:
            return apology("Please, fill all the details!",400)
        
        print(resturant,number,"dinein:",dine_in,"test","takwaay:",delivery,location,cuisines)
        #Add to the SQLite Resturant Table
        db.execute("INSERT INTO resturants (resturant_name,resturant_number,dine_in,delivery,location) VALUES (?,?,?,?,?)",resturant,number,dine_in,delivery,location)
        #Select the resturant ID and insert all cuisines in the cuisines foreign table
        resturant_id = db.execute("SELECT id FROM resturants WHERE resturant_name = ?", resturant)[0]["id"]
        for cuisine in cuisines:
            db.execute("INSERT INTO cuisines (rest_id, cuisine) VALUES(?,?)",resturant_id,cuisine)
        return redirect("/")
    return render_template("add_resturants.html",cuisines=cuisines)

@app.route("/add_post", methods=["GET","POST"])
@login_required
def add_post():
    #Resturants list
    resturants = db.execute("SELECT * FROM resturants")
    if request.method == "POST":
        resturant = request.form.get("resturant")
        time_from = request.form.get("from")
        time_to = request.form.get("to")
        order_type = request.form.get("order_type")
        number_of_people = request.form.get("number_of_people")
        comments = request.form.get("comments")
        if not resturant or not time_from or not time_to or not number_of_people:
                return apology("Please, fill all the details!",400)
        #Posts insertion
        db.execute("INSERT INTO posts (user_id,rest_id,time_from,time_to,order_type,number_of_people,comments) VALUES(?,?,?,?,?,?,?)", session["user_id"],resturant,time_from,time_to,order_type,number_of_people,comments)
        post_id = db.execute("SELECT id FROM posts WHERE user_id = ? AND rest_id = ? AND order_type = ? AND time_from = ? AND time_to = ? AND comments = ?", session['user_id'],resturant,order_type,time_from,time_to,comments)[0]['id']
        db.execute("INSERT INTO dashboard (id_post,user_id) VALUES(?,?)",post_id,session["user_id"])
        
        return redirect(url_for('dashboard',post_id = post_id))
    return render_template("add_post.html",resturants=resturants)

@app.route("/delivery", methods=["GET","POST"])
@login_required
def delivery():
    posts = db.execute("SELECT * FROM posts WHERE order_type = ?","order")
    if request.method == "POST":
        post_id = request.form.get("id")
        joiners = db.execute("SELECT user_id FROM dashboard WHERE id_post = ?", post_id)
        for joiner in joiners:
            if joiner["user_id"] == session["user_id"]:
                return apology("Already Joined",400)
        current_number = db.execute("SELECT current_people FROM posts WHERE id = ?", post_id)[0]["current_people"]
        max_number = db.execute("SELECT number_of_people FROM posts WHERE id = ?", post_id)[0]["number_of_people"]
        if current_number >= max_number:
            return apology("Already Full! Try Another Post.",400)
        db.execute("UPDATE posts SET current_people = ? WHERE id = ?",current_number+1,post_id) 
        db.execute("INSERT INTO dashboard (id_post,user_id) VALUES (?,?)", post_id,session["user_id"])
        return redirect(url_for('dashboard',post_id = post_id))
    return render_template("delivery.html",posts=posts,db=db,len=len)

@app.route("/in_resturant", methods=["GET","POST"])
@login_required
def in_resturant():
    posts = db.execute("SELECT * FROM posts WHERE order_type = ?","in_resturant")
    if request.method == "POST":
        post_id = request.form.get("id")
        joiners = db.execute("SELECT user_id FROM dashboard WHERE id_post = ?", post_id)
        print(joiners)
        for joiner in joiners:
            if joiner["user_id"] == session["user_id"]:
                return apology("Already Joined! Try Another Post.",400)
        current_number = db.execute("SELECT current_people FROM posts WHERE id = ?", post_id)[0]["current_people"]
        max_number = db.execute("SELECT number_of_people FROM posts WHERE id = ?", post_id)[0]["number_of_people"]
        if current_number >= max_number:
            return apology("Already Full! Try Another Post.",400)
        db.execute("UPDATE posts SET current_people = ? WHERE id = ?",current_number+1,post_id) 
        db.execute("INSERT INTO dashboard (id_post,user_id) VALUES (?,?)", post_id,session["user_id"])
        return redirect(url_for('dashboard',post_id = post_id))
    return render_template("in_resturant.html",posts=posts,db=db)

@app.route("/dashboard/<post_id>", methods=["POST","GET"])
@login_required
def dashboard(post_id):
    joiners = db.execute("SELECT user_id FROM dashboard WHERE id_post = ?",post_id)
    admin = joiners[0]["user_id"]
    print(type(admin), "and")
    if request.method == "POST":
        remove_user = request.form.get("id")
        if admin == int(remove_user):
            return apology("You can't delete the Admin!.",400)
        else:
            print("a7ten")
            db.execute("DELETE FROM dashboard WHERE user_id = ? AND id_post = ?", remove_user,post_id)
            current_number = db.execute("SELECT current_people FROM posts WHERE id = ?", post_id)[0]["current_people"]
            db.execute("UPDATE posts SET current_people = ? WHERE id = ?",current_number-1,post_id) 
            return redirect(url_for('dashboard',post_id = post_id))
    return render_template("dashboard.html",admin = admin,post_id=post_id,joiners=joiners,db=db,current_user = int(session["user_id"]))


@app.route("/profile", methods=["GET","POST"])
@login_required
def update_profile():
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    profile = db.execute("SELECT * FROM profile WHERE user_id = ?", session["user_id"])[0]
    if request.method == "POST":
        #Inputs
        number = request.form.get("number")
        name = request.form.get("name")
        building = request.form.get("building")
        room = request.form.get("room")

        #update profile table
        db.execute("UPDATE profile SET name = ?, number = ?, building = ?, room = ?  WHERE user_id = ?",name,number,building,room, session["user_id"])
        profile = db.execute("SELECT * FROM profile WHERE user_id = ?", session["user_id"])[0]
        return render_template("profile.html",profile=profile,user=user)
    return render_template("profile.html",profile=profile,user=user)

@app.route("/")
@login_required
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/my_posts",methods = ["GET","POST"])
def my_posts():
    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        post_id = request.form.get("id_post")
        db.execute("DELETE FROM dashboard WHERE id_post = ?",post_id)
        db.execute("DELETE FROM posts WHERE id = ?",post_id)
        posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])
    return render_template("my_posts.html",posts=posts,db=db,len=len)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usernames = db.execute("SELECT username FROM users")
        for counter in usernames:
            if username == counter["username"]:
                return apology("This username is already taken. Try another.",400)
        if not username or not password or not confirmation:
            return apology("All fields are required!",400)
        elif password != confirmation:
            return apology("Confirmation Password doesn't match the Password!")
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username,generate_password_hash(password))
        user_id = db.execute("SELECT id FROM users WHERE username = ?",username)[0]["id"]
        number = request.form.get("number")
        email = request.form.get("email")
        name = request.form.get("name")
        building = request.form.get("building")
        room = request.form.get("room")
        if not number or not email or not building or not room or not name:
            db.execute("DELETE FROM users WHERE id = ?",user_id)
            return apology("All fields are required!",400)
            
        db.execute("INSERT INTO profile (user_id,number,email,building,room,name) VALUES(?,?,?,?,?,?)", user_id,number,email,building,room,name)
        return redirect("/login")

    return render_template("register.html")
