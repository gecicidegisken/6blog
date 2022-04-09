from enum import unique
from flask import (Flask, render_template, request,redirect, url_for, session)
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)
app.secret_key = 'kRzGGFpnat' #bunu buraya yazmanın mantığını anlamadım
client = MongoClient('localhost',27017)

db=client.blog_db

db.users.create_index("username",unique=True)
db.users.create_index("email",unique=True)

@app.route('/' ,methods=['GET', 'POST'])
def index():
    # db.posts.delete_many({})
   
    allPosts= db.posts.find()
    return render_template('index.html',posts=allPosts)

@app.route('/<postid>/vote/<votetype>')
def vote(postid,votetype):
    post= db.posts.find_one({"_id": ObjectId(postid)})
    dislikes = post['dislikes']
    likes = post['likes']
    where={"_id":ObjectId(postid)}
    if votetype == '0':
        newValue={"$set":{"dislikes":dislikes+1}}
        db.posts.update_one(where,newValue)
        print(db.posts.find_one({"_id":ObjectId(postid)},{"_id":1,"dislikes":1}))
    elif votetype =='1':
        newValue={"$set":{"likes":likes+1}}
        db.posts.update_one(where,newValue)
        print(db.posts.find_one({"_id":ObjectId(postid)},{"_id":1,"likes":1}))
        
    return redirect(url_for('index'))
    

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
         #add user to users collection in database
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        usertype= request.form['usertype']

        if not db.users.find_one({"username":username}) and not db.users.find_one({"email":email}):
         db.users.insert_one({'username':username,'email':email,'password':password,'usertype':usertype})
         print("signup success")
         return redirect(url_for('login'))
    print("signup fail")  
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST']) #buradaki formun login actionu
def login():
    if 'username' in session:
        return redirect(url_for('index')) #kullanıcı giris yapmışsa indexe yönlendir
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({"username":username,"password":password})
        if user:
            print("login succes")
            session['username']=username
            session['usertype']=user['usertype']
            return redirect(url_for('index')) 
        else:
            print("login failed")
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
        db.posts.insert_one({"title":title,"content":content,"author":session["username"], "likes":0, "dislikes":0})
        return redirect(url_for('index'))

    return render_template('newpost.html')




if __name__ == "__main__": 
    app.run(debug=True)


#sudo systemctl start mongod
# pipenv run python3 app.py