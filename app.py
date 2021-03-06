import time
import json
from instance.config import Connection, JWTKey
from datetime import timedelta
from flask_cors import *
from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource, reqparse, inputs
from mongoengine import *
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
    current_user,
    get_jwt,
)


app = Flask(__name__, instance_relative_config=True)
CORS(
    app,
    origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080/",
        "http://localhost:3000",
    ],
)


app.config.from_object("config")
app.config.from_pyfile("config.py")
app.config["JWT_SECRET_KEY"] = JWTKey.JWT_KEY

JWT_TTL = timedelta(minutes=1)

api = Api(app)
db = connect(host=Connection.DB_URI)
parser = reqparse.RequestParser()
jwt = JWTManager(app)
swagger = Swagger(app)


# region database schemas
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    usertype = BooleanField(required=True)  # 1 = writer , 0 = reader


class Entry(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = FloatField()


class Vote(Document):
    upordown = BooleanField()  # 1 = up, 0 = down
    voting_user = ReferenceField(User, reverse_delete_rule=CASCADE)
    entry = ReferenceField(Entry, reverse_delete_rule=CASCADE)


class TokenBlockList(Document):
    jti = StringField(required=True)


# Vote.objects.delete()
# Entry.objects.delete()
# TokenBlockList.objects.delete()
# endregion

# region helper functions
def get_user_by_id(userid):
    try:
        user = User.objects(id=userid).limit(1).first()
    except:
        return
    if user != None:
        return user
    return


def get_user_by_username(username):
    try:
        user = User.objects(username=username).limit(1).first()
    except:
        return
    if user != None:
        return user
    return


def get_entry_by_id(entryid):
    try:
        entry = Entry.objects(id=entryid).limit(1).first()
    except:
        return
    if entry != None:
        return entry
    return


def get_entries_orderby_date():
    try:
        entries = Entry.objects().order_by("-date")
    except:
        return
    return entries


def check_user_password(user, password):
    password_check = check_password_hash(user.password, password)
    return password_check


# endregion

# region JWT callbacks
# JWT olu??tururken identity=user yazd??????m??zda bu user objectinin id de??erini do??ru formatta getiren
# callback fonksiyonu
@jwt.user_identity_loader
def get_id_by_user(user):
    return str(user.id)


# current_user da buradan geliyor
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.objects(id=identity).limit(1).first()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlockList.objects(jti=jti).limit(1).first()
    return token != None


# endregion


# entry: get & vote actions
class SingleEntry(Resource):
    def get(self, entry_id):
        """Get an entry by entry_id
        ---
        parameters:
            - in: path
              name: entry_id
              required: true
              description: the ID of the entry from db
              type: string
        responses:
            200:
                description: the entry data {title,content,author,data,upvotes,downvotes}
            404:
                description: entry not found
        """
        entry = get_entry_by_id(entry_id)
        votes = Vote.objects(entry=entry)
        upvotes = votes.filter(upordown=True).count()
        downvotes = votes.filter(upordown=False).count()
        if entry != None:
            return {
                "title": entry.title,
                "content": entry.content,
                "author": json.loads(entry.author.to_json()),
                "date": entry.date,
                "upvotes": upvotes,
                "downvotes": downvotes,
            }

        return {"err": "not found"}, 404

    @jwt_required()
    def post(self, entry_id):
        """Vote an entry by entry_id
        ---
        parameters:
            - in: path
              name: entry_id
              required: true
              description: the ID of the entry from db
              type: string
            - in: body
              name: votetype
              required: true
              description: vote (0 = downvote , 1 = upvote)
              type: boolean
        responses:
            200:
                description: Successfully voted
            210:
                description: Vote successfully changed
            401:
                description: User must be logged in to vote
            403:
                description: Current user already voted this content

        """

        if current_user:
            parser.add_argument(
                "votetype", location="args", help="argda hata", type=inputs.boolean
            )
            print("burda")
            args = parser.parse_args()
            votetype = args["votetype"]
            entry = get_entry_by_id(entry_id)
            vote = Vote(upordown=votetype, voting_user=current_user, entry=entry)
            existingVote = (
                Vote.objects(voting_user=vote.voting_user, entry=vote.entry)
                .limit(1)
                .first()
            )
            if existingVote == None:
                vote.save()
                return {"msg": "entry voted"}, 200
            elif existingVote.upordown == votetype:
                # user is trying to vote the same votetype
                return {"err": "user already voted this content"}, 403
            elif existingVote.upordown != votetype:
                # user already voted but changed their mind
                existingVote.delete()
                vote.save()
                return {"msg": "new vote posted"}, 210

        else:
            return {"err": "login to vote"}, 401


# entry: get the page with new entry form
class NewEntry(Resource):
    @jwt_required()
    def get(self):
        """Get the page to post a new entry

        ---
        responses:
            200:
                description: user is authanticated to write
            401:
                description: user is not logged in
            403:
                description: user's usertype is not allowed to write

        """
        if current_user:
            usertype = get_user_by_id(current_user.id).usertype

            if usertype:
                return 200
            else:
                return {"err": "user is not allowed to write"}, 403
        else:
            return {"err": "you must login to write"}, 401


# entry: list all, post new and delete actions
class EntryList(Resource):
    def get(self):
        """Get all entries ordered by date
        ---

        responses:
            200:
                description: all entries ordered by date in json format
        """

        entries = get_entries_orderby_date()

        return json.loads(entries.to_json())

    @jwt_required()
    def post(self):
        """Add new entry
        ---
        parameters:
            - in: body
              name: title
              required: true
              description: the title of the new entry
              type: string

            - in: body
              name: content
              required: true
              description: the content of the new entry
              type: string
        responses:
            200:
                description: info of the new entry
            401:
                description: login to post a new entry
            403:
                description: current user's usertype is not allowed to write

        """

        parser.add_argument("title")
        parser.add_argument("content")
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]

        if current_user:
            author = get_user_by_id(current_user.id)
            if author.usertype == 0:
                return {"err": "user must be a writer to write"}, 403

            else:
                newEntry = Entry(
                    title=title, content=content, author=author, date=time.time()
                ).save()
            return {"msg": "successfully posted"}
        else:
            return {"err": "login to post a new entry"}, 401

    def delete(self, entry_id):
        """Delete an entry by entry_id
        ---
        parameters:
            - in: path
              name: entry_id
              required: true
              description: the id of the entry to be deleted
              type: string
        responses:
            200:
                description: entry deleted
            400:
                description: entry not found

        """
        entry = get_entry_by_id(entry_id)
        if entry != None:
            entry.delete()
            return {"msg": "entry deleted"}
        else:
            return {"err": "entry does not exist"}, 400


# user: register, delete and get actions
class UserList(Resource):
    def get(self, user_id):
        """Get user info by user_id
        ---
        parameters:
            - in : path
              name: user_id
              required: true
              description: the id of the user
              type: string

        responses:
            200:
                description: user info
            404:
                description: user not found
        """
        user = get_user_by_id(user_id)
        if user != None:
            return {
                "username": user.username,
                "usertype": user.usertype,
            }
        else:
            return {"err": "user not found"}, 404

    def post(self):
        """Register a new user
        ---
        parameters:
            - in: body
              name: username
              description: username of the user
              required: true
              type: string
            - in: body
              name: password
              description: password of the user
              required: true
              type: string
            - in: body
              name: usertype
              description: user type ( writer or reader )
              required: true
              type: boolean
        responses:
            200:
                description: new user's info
            400:
                description: username is used
            405:
                description: info cannot be blank
        """
        parser.add_argument("username")
        parser.add_argument("password")
        parser.add_argument("usertype", type=inputs.boolean)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        usertype = args["usertype"]
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )
        user = get_user_by_username(username)

        if username == None or password == None or usertype == None:
            return {"err": "user info cannot be blank"}, 405
        else:
            if user != None:
                return {"err": "username is used"}, 400

            newUser = User(
                username=username, password=hashed_password, usertype=usertype
            ).save()
            return {
                "msg": "successfully registered",
                "username": newUser.username,
            }, 200

    def delete(self, user_id):
        """Delete a user by user_id

        ---
        parameters:
            - in: path
              name: user_id
              description: id of the user to be deleted
              type: string
              required: true

        responses:
            200:
                description: user deleted
            404:
                description: user does not exist
        """
        user = get_user_by_id(user_id)

        if user != None:
            user.delete()
            return {"msg": "user deleted"}
        return {"err": "user does not exist"}, 404


# user: login and logout actions
class SingleUser(Resource):
    def get(self):
        """
        Get the page with login form

        ---
        responses:
            200:
                description: page with the login form
        """
        return

    def post(self):
        """
        Credental check for user login
        ---
        parameters:
            - in: body
              name: username
              description: username of the user
              required: true
              type: string
            - in: body
              name: password
              description: password of the user
              required: true
              type: string
        responses:
            200:
                description: Returns access token and 'false' if usertype is reader &
                'true' if usertype is writer
            400:
                description: Login failed
        """

        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        user = get_user_by_username(username)

        if user != None:
            password_check = check_user_password(user, password)
            if password_check:
                access_token = create_access_token(identity=user)
                return {
                    "access_token": access_token,
                }
        else:
            return {"err": "Username/password incorrect"}, 400

    @jwt_required(optional=True)
    def delete(self):
        """Logout
        responses:
            200:
                description: logout success
            400:
                description: already logged out
            401:
                description: token expired before logging out
        """
        if current_user != None:
            jti = get_jwt()["jti"]
            blockedToken = TokenBlockList(jti=jti)
            blockedToken.save()
            return {"msg": "logout success"}
        else:
            return {"err": "already logged out"}, 400


api.add_resource(EntryList, "/entries")
api.add_resource(SingleEntry, "/entries/<string:entry_id>")
api.add_resource(UserList, "/users/<string:user_id>", "/register", "/users")
api.add_resource(SingleUser, "/login")
api.add_resource(NewEntry, "/newentry")

if __name__ == "__main__":
    app.run(debug=True)
