from flask import Flask, url_for, render_template, redirect, request, session
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def categories():
    sql = "SELECT * FROM categories ORDER BY category_name ASC"
    cursor.execute(sql)
    cats = cursor.fetchall()
    return cats
app.jinja_env.globals.update(categories=categories)


@app.route('/')
def home():
    sql = "SELECT * FROM posts " \
          "INNER JOIN users ON users.user_id = posts.post_user_id " \
          "INNER JOIN categories ON categories.category_id = posts.post_category_id " \
          "ORDER BY post_id DESC"
    cursor.execute(sql)
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/category/<url>')
def category(url):
    cursor.execute("SELECT * FROM categories WHERE category_url = %s", (url,))
    cat = cursor.fetchone()

    if cat:
        sql = "SELECT * FROM posts " \
              "INNER JOIN users ON users.user_id = posts.post_user_id " \
              "INNER JOIN categories ON categories.category_id = posts.post_category_id " \
              "WHERE post_category_id = %s " \
              "ORDER BY post_id DESC"
        cursor.execute(sql, (cat['category_id'],))
        posts = cursor.fetchall()
        return render_template('category.html', category=cat, posts=posts)
    else:
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    error = ''
    if request.method == 'POST':
        if request.form['email'] == '':
            error = 'E-posta adresinizi belirtin.'
        elif request.form['password'] == '':
            error = 'Şifrenizi belirtin.'
        else:
            sql = "SELECT * FROM users WHERE user_email = %s && user_password = %s"
            cursor.execute(sql, (request.form['email'], (request.form['password']),))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user['user_id']
                return redirect(url_for('home'))
            else:
                error = 'Girdiğiniz bilgilere ait kullanıcı bulunamadı.'

    return render_template('login.html', error=error)

    
@app.route('/register')
def register():
        return render_template('register.html')
    
@app.route('/post/<url>')
def post(url):
    sql = "SELECT * FROM posts " \
          "INNER JOIN users ON users.user_id = posts.post_user_id " \
          "INNER JOIN categories ON categories.category_id = posts.post_category_id " \
          "WHERE post_url = %s"
    cursor.execute(sql, (url,))
    post = cursor.fetchone()
    if post:
        return render_template('post.html', post=post)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
