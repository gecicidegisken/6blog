from flask import Flask, request, session, jsonify
from mongoengine import *
from flask_restful import Api, Resource

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")
api = Api(app)
db = connect("6blogdb")

# database schemas

# db.drop_database('6blogdb')


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # bunun tipi değişebilir
    usertype = BooleanField(required=True)  # 1 = writer , 0 = reader


class Entry(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    # votes= ListField(ReferenceField(Vote))
    author = ReferenceField(
        User, reverse_delete_rule=CASCADE
    )  # delete all of their entries if a user is deleted
    date = DateTimeField()


class Vote(Document):
    upordown = BooleanField()  # 1=up, 0 =down
    voting_user = ReferenceField(
        User, reverse_delete_rule=CASCADE
    )  # delete all of their votes if a user is deleted
    entry = ReferenceField(Entry, reverse_delete_rule=CASCADE)


# dummyuser1=User(username='yazar', password='123',usertype=1).save()
# dummyuser2=User(username='hilal', password='123',usertype=1).save()
# dummyuser2=User(username='okur', password='123',usertype=0).save()
# dummyVote1=Vote(upordown=1,voting_user=dummyuser2).save()
# dummyVote2=Vote(upordown=0,voting_user=dummyuser2).save()
# dummyVote3=Vote(upordown=0,voting_user=dummyuser1).save()
# dummypost1=Entry(title='Chinese Democracy', content='AAAAA', author=dummyuser1 ).save()
# dummypost2=Entry(title='The Spaghetti Incident', content='BBBBB', author=dummyuser1).save()

# helper functions
def getUserbyId(userid):
    user = User.objects(id=userid).limit(1).first()
    if user != None:
        return user
    return


def getUserByUsername(username):
    user = User.objects(username=username).limit(1).first()
    if user != None:
        return user
    return


def getEntryById(entryid):
    entry = Entry.objects(id=entryid).limit(1).first()
    if entry != None:
        return entry
    return


def getEntriesByDate():
    entries = Entry.objects().order_by("date")
    return entries


# entry: get, vote actions
class SingleEntry(Resource):
    def get(self, entry_id):
        # get an entry
        entry = getEntryById(entry_id)
        if entry != None:
            return {"title": entry.title, "content": entry.content}
        else:
            return {"err": "not found"}, 404

    def put(self, entry_id):
        # vote an entry
        if "username" in session:
            votetype = int(request.form["vote"])
            current_user = getUserByUsername(session["username"])
            entry = getEntryById(entry_id)
            vote = Vote(upordown=votetype, voting_user=current_user, entry=entry)

            if not Vote.objects(voting_user=vote.voting_user, entry=vote.entry):
                print("oy kullanildi")
                vote.save()
                return vote.to_json()
            else:
                return {"err": "user already voted this content"}, 403

        else:
            return {"err": "login to vote"}, 401


# entry: list all, post new and delete actions
class EntryList(Resource):
    def get(self):
        # get all entries (return düzenlenecek)
        entries = getEntriesByDate()
        return entries.to_json()

    def post(self):
        # new entry
        title = request.form["title"]
        content = request.form["content"]

        if "username" in session:
            author = getUserByUsername(session["username"])
            newEntry = Entry(
                title=title, content=content, author=author, downvotes=0, upvotes=0
            ).save()
            return {"title": newEntry.title, "author": newEntry.author}
        else:
            return {"err": "login to post a new entry"}, 401

    def delete(self, entry_id):
        # delete entry by id
        entry = getEntryById(entry_id)
        if entry != None:
            entry.delete()
            return {"msg": "entry deleted"}
        else:
            return {"err": "entry does not exist"}, 400


# user: register, delete and get actions
class UserList(Resource):
    def get(self, user_id):
        # get a user's information
        user = getUserbyId(user_id)
        if user != None:
            return {
                "username": user.username,
                "password": user.password,
                "usertype": user.usertype,
            }
        else:
            return {"err": "user not found"}, 404

    def post(self):
        # register new user
        username = request.form["username"]
        password = request.form["password"]
        usertype = request.form["usertype"]
        user = getUserByUsername(username)

        if user != None:
            return {"err": "username is used"}, 400
        newUser = User(username=username, password=password, usertype=usertype).save()

        return {
            "username": newUser.username,
            "password": newUser.password,
            "usertype": newUser.usertype,
        }

    def delete(self, user_id):
        # delete user
        user = getUserbyId(user_id)

        if user != None:
            user.delete()
            return {"msg": "user deleted"}
        return {"err": "user does not exist"}


# user: login and logout actions
class SingleUser(Resource):
    def get(self):
        # get the page with login form
        return ()

    def post(self):
        # user login --credental check
        username = request.form["username"]
        password = request.form["password"]
        user = getUserByUsername(username)
        if user.password == password:
            session["username"] = username
            print(session)
            return {"msg": "login success"}
        return {"err": "login fail"}, 400

    def delete(self):
        # user logout
        session.pop("username", None)
        print(session)
        return {"msg": "logout success"}


api.add_resource(EntryList, "/", "/entries", "/entries/new")
api.add_resource(SingleEntry, "/entries/<string:entry_id>")
api.add_resource(UserList, "/users/<string:user_id>", "/users/register", "/users")
api.add_resource(SingleUser, "/login")

if __name__ == "__main__":
    app.run(debug=True)


# sudo systemctl start mongod
# pipenv run python3 app.py
