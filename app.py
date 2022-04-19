from xmlrpc.client import Boolean, boolean
from flask import Flask, request, session, jsonify
from mongoengine import *
from flask_restful import Api, Resource, reqparse

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")
api = Api(app)
db = connect("6blogdb")
parser = reqparse.RequestParser()


# database schemas

# db.drop_database('6blogdb')


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # bunun tipi değişebilir
    usertype = BooleanField(required=True)  # 1 = writer , 0 = reader


class Entry(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(
        User, reverse_delete_rule=CASCADE
    )  # delete all of their entries if a user is deleted
    date = DateTimeField()


class Vote(Document):
    upordown = BooleanField()  # 1=up, 0=down
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
def get_user_by_id(userid):
    user = User.objects(id=userid).limit(1).first()
    if user != None:
        return user
    return


def get_user_by_username(username):
    user = User.objects(username=username).limit(1).first()
    if user != None:
        return user
    return


def get_entry_by_id(entryid):
    entry = Entry.objects(id=entryid).limit(1).first()
    if entry != None:
        return entry
    return


def get_entries_orderby_date():
    entries = Entry.objects().order_by("date")
    return entries


# entry: get, vote actions
class SingleEntry(Resource):
    def get(self, entry_id):
        # get an entry
        entry = get_entry_by_id(entry_id)
        if entry != None:
            return {"title": entry.title, "content": entry.content}
        else:
            return {"err": "not found"}, 404

    # voting system needs updating
    def put(self, entry_id):
        # vote an entry
        if "username" in session:
            parser.add_argument("votetype", type=Boolean, required=True)
            args = parser.parse_args()
            votetype = args["votetype"]
            current_user = get_user_by_username(session["username"])
            entry = get_entry_by_id(entry_id)
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
        # get all entries
        entries = get_entries_orderby_date()
        return entries.to_json()

    def post(self):
        # new entry
        print(request.content_type)

        parser.add_argument("title", required=True)
        parser.add_argument("content", required=True)
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]

        if "username" in session:
            author = get_user_by_username(session["username"])
            newEntry = Entry(
                title=title,
                content=content,
                author=author,
            ).save()
            return {"title": newEntry.title, "author": newEntry.author.username}
        else:
            return {"err": "login to post a new entry"}, 401

    def delete(self, entry_id):
        # delete entry by id
        entry = get_entry_by_id(entry_id)
        if entry != None:
            entry.delete()
            return {"msg": "entry deleted"}
        else:
            return {"err": "entry does not exist"}, 400


# user: register, delete and get actions
class UserList(Resource):
    def get(self, user_id):
        # get a user's information
        user = get_user_by_id(user_id)
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
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("usertype", type=Boolean, required=True)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        usertype = args["usertype"]
        user = get_user_by_username(username)

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
        user = get_user_by_id(user_id)

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
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        user = get_user_by_username(username)

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


api.add_resource(EntryList, "/", "/entries")
api.add_resource(SingleEntry, "/entries/<string:entry_id>")
api.add_resource(UserList, "/users/<string:user_id>", "/users/register", "/users")
api.add_resource(SingleUser, "/login")

if __name__ == "__main__":
    app.run(debug=True)


# sudo systemctl start mongod
# pipenv run python3 app.py
