from flask import Flask,url_for,request,render_template,redirect 
from markupsafe import escape

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return 'post edildi'
    else:
        return render_template('index.html')
    
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
