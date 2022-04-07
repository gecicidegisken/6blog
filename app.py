import email
from http import client
from importlib.metadata import requires
from flask import (Flask, render_template, request,redirect, url_for, session)
from pymongo import MongoClient
app = Flask(__name__)
app.secret_key = 'kRzGGFpnat' #bunu buraya yazmanın mantığını anlamadım
client = MongoClient('localhost',27017)

db=client.blog_db

class User():
    username =""
    password =""
    usertype =""
    email =""
    def __init__(self,username):
        self.username=username
    def createUser(self,username,email,password,usertype):
        username=username
        email =email
        password=password
        usertype=usertype

@app.route('/' ,methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
         #üyeyi veritabanına kaydetme işlemleri
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        usertype= request.form['usertype']
        user = User(username)
        user.createUser(username,email,password,usertype)
        db.users.insert_one({'username':username,'email':email,'password':password,'usertype':usertype})

       
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST']) #buradaki formun login actionu
def login():
    if 'username' in session:
        return redirect(url_for('index')) #kullanıcı giris yapmışsa indexe yönlendir
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usertype= "writer" #geçici
        #burada veritabanındaki kayıtlarla kontrol edeceğiz
        if username=='hilal' and password =='123':
          session['username']=username
          session['usertype']=usertype
          return redirect(url_for('index'))
        else:
          render_template('login.html')
    return render_template('login.html')
    

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/newpost', methods=['GET','POST']) 
def newpost():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title= request.form['post-title']
        content = request.form['post-content']
        return redirect(url_for('index'))
    return render_template('newpost.html')




if __name__ == "__main__": 
    app.run(debug=True)


# pipenv run python3 app.py