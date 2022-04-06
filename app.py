
from cmath import log
import re
from flask import (Flask, render_template, request,redirect, url_for, session)
app = Flask(__name__)
app.secret_key = 'gizli_metin' #bunu buraya yazmak mantıklı mı?


@app.route('/' ,methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
         #üyeyi veritabanına kaydetme işlemleri
        username = request.form['username']
        password = request.form['password']
        usertype= request.form['usertype']
        
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