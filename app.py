from flask import (Flask, request, session, url_for,redirect)
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
app.secret_key = 'kRzGGFpnat' #bunu buraya yazmanın mantığını anlamadım

entrys ={
    'entry1':{'title':'I.R.S', 'content':'selam naber'},
    'entry2':{'title':'Catcher In The Rye', 'content':'iyidir senden naber'}
}
users = {
    'user1':{'username':'yazar','password':'123'},
    'user2':{'username':'okuyucu','password':'123'}
}

class Entry(Resource):
    def get(self, entry_id):
        #get an entry
        return {'title':entrys[entry_id]['title'],'content':entrys[entry_id]['content']}
    def put(self,entry_id):    
        # update an entry
        entrys[entry_id]['title']=request.form['title']
        entrys[entry_id]['content']=request.form['content']
        return {"title": entrys[entry_id]['title'],"content":entrys[entry_id]['content']}

class EntryList(Resource):
    def get(self):
        #get all entries
        return entrys
    def post(self):
        #new entry
        title=request.form['title']
        content=request.form['content']
        entry_id = int(max(entrys.keys()).lstrip('entry'))+1
        entry_id = 'entry%i'%entry_id
        entrys[entry_id]={'title':title,'content':content}

class UserList(Resource):
    def get(self,user_id):
        #get a user
        return users[user_id]

    def post(self):
        #create new user
        username= request.form['u_username']
        password= request.form['u_password']
        user_id = int(max(users.keys()).lstrip('user'))+1
        user_id = 'user%i'%user_id
        users[user_id] ={'username':username,'password':password}
    def delete(self):
        """delete user"""

#user login logout actions
class User(Resource):
    def get(self):
        #get the page with login form
        return()
    def post(self):
        #user login --credental check
        username = request.form['username']
        session['username']=username  
        print(session)
        return("giris:basarili")
    def delete(self):
        #user logout
        print(session)
        session.pop('username',None)
        return("cikis:basarili")


         
api.add_resource(EntryList,'/', '/entries', '/entries/new')     
api.add_resource(Entry,'/entries/<string:entry_id>')
api.add_resource(UserList,'/users/<string:user_id>')
api.add_resource(User,'/login')
# api.add_resource(UserLogout,'/logout')

if __name__ == "__main__": 
    app.run(debug=True)


#sudo systemctl start mongod
# pipenv run python3 app.py