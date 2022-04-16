from flask import (Flask, request, session, url_for,redirect)
from mongoengine import *
from flask_restful import Api, Resource

app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
api = Api(app)
connect('6blogdb')

#database schemas

class User(Document):
    username =StringField(required=True, unique=True)
    password = StringField(required = True) #bunun tipi değişebilir
    usertype = BooleanField(required =True) #1 = writer , 0 = reader

class Entry(Document):
    title=StringField(required=True)
    content=StringField(required=True)
    upvotes=IntField(required=True)
    downvotes=IntField(required=True)
    author = ReferenceField(User,reverse_delete_rule=CASCADE) #delete all of their entries if a user is deleted
    

# dummyuser1=User(username='yazar', password='123',usertype=1).save()
# dummyuser2=User(username='okur', password='123',usertype=0).save()

# dummypost1=Entry(title='Chinese Democracy', content='AAAAA', author=dummyuser1, downvotes=0, upvotes=0).save()
# dummypost2=Entry(title='The Spaghetti Incident', content='BBBBB', author=dummyuser1, downvotes=0, upvotes=0).save()
# dummypost3=Entry(title='The Spaghetti Incident', content='BBBBB', author=dummyuser1, downvotes=0, upvotes=0).save()

#entry: get, vote actions
class SingleEntry(Resource):
    def get(self, entry_id):
        #get an entry
        for e in Entry.objects(id=entry_id):
            return {'title':e.title,'content':e.content}
            
    def put(self,entry_id):    
        #vote an entry
        if 'username' in session:
            vote = int(request.form['vote'])
            for e in Entry.objects(id=entry_id):
                if vote==1:
                    e.upvotes =e.upvotes+1
                    e.save()
                elif vote==0:
                    e.downvotes =e.downvotes+1
                    e.save()
                return ({'downvotes':int(e.downvotes),'upvotes':int(e.upvotes)})
        else:
            return("hata:oy kullanmak icin giris yapmalisiniz")

#entry: list all, post new and delete actions
class EntryList(Resource):
    def get(self):
        #get all entries (return düzenlenecek)
        for e in Entry.objects:
            print(e.title)
        return ('No entry found')
    def post(self):
        #new entry  
        title=request.form['title']
        content=request.form['content']
        if 'username' in session:
            for u in User.objects(username=session['username']):
                author=u
            newEntry=Entry(title=title, content=content, author=author, downvotes=0, upvotes=0).save()
            return({"title":newEntry.title,"author":newEntry.author})
        else:
            return({'hata':'yazi yazmak icin giris yapmalisiniz'})
    def delete(self,entry_id):
        # delete entry by id
        for e in Entry.objects(id=entry_id):
            e.delete()
            return {"onay":"yazi silindi"}
        return({"hata":"yazi silinemedi"})

#user: register, delete and get actions
class UserList(Resource):
    def get(self,user_id):
        #get a user's informationee
        for u in User.objects(id=user_id):
            return {'username':u.username, 'password':u.password,'usertype':u.usertype}
        return({"hata":"kullanici bulunamadi"})

    def post(self):
        #register new user
        username= request.form['username']
        password= request.form['password']
        usertype= request.form['usertype']
        for u in User.objects(username=username):
            if u:
                return({"hata":"kullanici adi kullaniliyor"})
        newUser=User(username=username,password=password,usertype=usertype).save()
        return {'username':newUser.username, 'password':newUser.password,'usertype':newUser.usertype}
    def delete(self,user_id):
         #delete user
        for u in User.objects(id=user_id):
            u.delete()
            return {"onay":"kullanici silindi"}
        return({"hata":"kullanici silinemedi"})

#user: login and logout actions
class SingleUser(Resource):
    def get(self):
        #get the page with login form
        return()
    def post(self):
        #user login --credental check
        username = request.form['username']
        password = request.form['password']
        for u in User.objects:
            if u.username== username and u.password == password:
                session['username']=username  
                print(session)
                return({"onay":"giris basarili"})
        return ({"hata":"giris basarisiz"})
    def delete(self):
        #user logout
        session.pop('username',None)
        print(session)
        return({"onay":"cikis basarili"})


         
api.add_resource(EntryList,'/', '/entries', '/entries/new')     
api.add_resource(SingleEntry,'/entries/<string:entry_id>')

api.add_resource(UserList,'/users/<string:user_id>','/users/register','/users')
api.add_resource(SingleUser,'/login')

if __name__ == "__main__": 
    app.run(debug=True)


#sudo systemctl start mongod
# pipenv run python3 app.py