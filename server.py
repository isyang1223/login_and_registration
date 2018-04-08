from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re 
import md5

app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'loginDB')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    
    return render_template("success.html")
    



@app.route('/login', methods=['POST'])
def log():
    query = "SELECT * FROM users WHERE users.email = :email AND users.password = :password"
    password = md5.new(request.form['password']).hexdigest()
    data = {
             'email': request.form['email'],
             'password': password
           }
    email = mysql.query_db(query, data)

    if len(email) > 0:   
        return redirect("/success")
    else:
        return redirect("/")

    return redirect('/')
    

@app.route('/registration', methods=['POST'])
def create():
    count = 0
    if len(request.form['email']) < 1:
        flash("Email cannot be empty!")
        
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email!")
        
    else:
        email = request.form['email']
        count+=1

    if len(request.form['first_name']) < 2 and len(request.form['last_name']) < 2 :
        flash("has to be greater than 2") 
    else:
        if not NAME_REGEX.match(request.form['first_name']) or not NAME_REGEX.match(request.form['last_name']):
            flash("Invalid name!")
        
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            count+=1
        
    if len(request.form['password']) < 1 or len(request.form['password']) < 8:
        flash("Password cannot be empty or needs to be at least 8 characters long!")
        
    else:
        if request.form['password'] != request.form['password2']:
            flash("Passwords need to match!")
            
        elif request.form['password'] == request.form['password2']:  
            count+=1
            password = request.form['password']
            password2 = request.form['password2']

    
    if count == 3:
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (:first_name, :last_name, :email, :password, NOW())"
        password = md5.new(request.form['password']).hexdigest()
        data = {
                'email': request.form['email'],
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'password': password
           }
        mysql.query_db(query, data)
        return redirect("/success")
    
    return redirect('/')



app.run(debug=True) # run our server