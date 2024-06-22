from flask import Flask,url_for,request,render_template,redirect 
from markupsafe import escape
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="python"
)

cursor =db.cursor(dictionary=True)



app = Flask(__name__)

@app.route('/')
def home():
        sql="SELECT*FROM posts ORDER BY post_id DESC"
        cursor.execute(sql)
        posts=cursor.fetchall()
        return render_template('index.html', posts=posts)
    
@app.route('/user/<username>')
def user(username):
        return render_template('user.html',username=username)
    
@app.route('/login')
def login():
        return render_template('login.html')
    
@app.route('/register')
def register():
        return render_template('register.html')
    
@app.route('/post/<url>')
def post(url):
        return render_template('post.html',url=url)

if __name__ == '__main__':
    app.run(debug=True)
