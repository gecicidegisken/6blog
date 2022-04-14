from flask import (Flask, render_template, request,redirect, url_for, session)
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

entrys ={
    '1':{'title':'I.R.S', 'content':'selam naber'},
    '2':{'title':'Catcher In The Rye', 'content':'iyidir senden naber'}
}
users = {
    'user1':{'username':'yazar','password':'123'},
    'user2':{'username':'okuyucu','password':'123'}
}

class entry(Resource):
    def get(self, entry_id):
        return {'title':entrys[entry_id]['title'],'content':entrys[entry_id]['content']}
    #    update
    def put(self,entry_id):
        
        entrys[entry_id]['title']=request.form['e_title']
        entrys[entry_id]['content']=request.form['e_content']
        return {"title": entrys[entry_id]['title'],"content":entrys[entry_id]['content']}

class EntryList(Resource):
    def get(self):
        return entrys
    def post(self):
        entrys['entry3']['title']=request.form['e_title']
        entrys['entry3']['content']=request.form['e_content']

class Users(Resource):
    def get(self):
        return users
    def post(self):
        """ create new user """
        username= request.form['u_username']
        password= request.form['u_password']
        user_id = int(max(users.keys()).lstrip('user'))+1
        user_id = 'user%i'%user_id
        users[user_id] ={'username':username,'password':password}


api.add_resource(EntryList,'/', '/<string:entry_id>')     
api.add_resource(entry,
                    '/<string:entry_id>')

api.add_resource(Users,'/users')

if __name__ == "__main__": 
    app.run(debug=True)


#sudo systemctl start mongod
# pipenv run python3 app.py