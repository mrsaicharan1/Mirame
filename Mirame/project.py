from flask import Flask,request,render_template,redirect,url_for,session,flash
from flask_bootstrap import Bootstrap
import _sqlite3

app = Flask(__name__)
bootstrap = Bootstrap(app)

con=_sqlite3.connect('database.db')
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS LIST(email TEXT NOT NULL ,password TEXT NOT NULL )')
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/success')
def success():
    return 'SIGNUP was a success! :D'

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        con = _sqlite3.connect('database.db')
        cur = con.cursor()
        users = cur.execute('SELECT * FROM LIST')
        for user  in users :
            if request.form['email']==user[0]:
                con.commit()
                con.close()
                flash('Email already exists')
            if request.form['password']!=request.form['confirm-password']:
                flash('passwords mismatch')
                return render_template('psmc.html')  
        con.execute('INSERT INTO LIST(email,password) VALUES(?,?)',(request.form['email'], request.form['password']))
        con.commit()
        con.close()
        return render_template('success.html')

@app.route('/login',methods=['post','get'])
def login():    
    session.clear()
    if request.method=='GET':
        return render_template('login.html')
    con = _sqlite3.connect('database.db')
    cur = con.cursor()
    error=False
    email = request.form['email']
    password = request.form['password']
    user_data = cur.execute('SELECT * FROM LIST WHERE email=(?)',(email,))
    if password == user_data.fetchone()[1]:
        con.commit()
        con.close() 
        session['email']=email
        session['logged_in']=True
        return render_template('index.html',message='You have successfully logged in!')
    else:
        error=True
        con.commit()
        return render_template('index.html',message='Incorrect password or user does not exist')

if __name__ == '__main__':
      app.secret_key='chala secret'  
      app.run(debug=True)
    

