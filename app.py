from instance.config import Connection, JWTKey
from datetime import date, timedelta
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
JWT_TTL = timedelta(hours=2)
app.config.from_object("config")
app.config.from_pyfile("config.py")
app.config["JWT_SECRET_KEY"] = JWTKey.JWT_KEY
api = Api(app)
db = connect(host=Connection.DB_URI)
parser = reqparse.RequestParser()
jwt = JWTManager(app)
swagger = Swagger(app)
# database schemas
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    usertype = BooleanField(required=True)  # 1 = writer , 0 = reader


class Entry(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = DateTimeField(required=True)


class Vote(Document):
    upordown = BooleanField()  # 1 = up, 0 = down
    voting_user = ReferenceField(User, reverse_delete_rule=CASCADE)
    entry = ReferenceField(Entry, reverse_delete_rule=CASCADE)


class TokenBlockList(Document):
    jti = StringField(required=True)


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


def check_user_password():
    """"""


# JWT oluştururken identity=user yazdığımızda bu user objectinin id değerini doğru formatta getiren
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


# entry: get, vote actions
class SingleEntry(Resource):
    def get(self, entry_id):
        """Get an entry by entry_id

        Return entry information (title,content,author username,date) based on ID,
        Return 404 not found if entry does not exist
        ---
        parameters:
            - in: path
              name: entry_id
              required: true
              description: the ID of the entry from db
              type: string
        responses:
            200:
                description: the entry data
            404:
                description: entry not found
        """
        entry = get_entry_by_id(entry_id)
        if entry != None:
            return {
                "title": entry.title,
                "content": entry.content,
                "author": entry.author.username,
                "date": entry.date,
            }
        else:
            return {"err": "not found"}, 404

    def put(self, entry_id):
        """Vote an entry by entry_id
        ---
        parameters:
            - in: path
              name: entry_id
              required: true
              description: the ID of the entry from db
              type: string
        responses:
            200:
                description: Vote info
            401:
                description: Login to vote
            403:
                description: Current user already voted this content

        """
        current_user = get_user_by_username(session["username"])
        if current_user != None:
            parser.add_argument("votetype", type=inputs.boolean, required=True)
            args = parser.parse_args()
            votetype = args["votetype"]
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
        """Get all entries ordered by date
        ---
        responses:
            200:
                description: all entries ordered by date in json format
        """
        entries = get_entries_orderby_date()
        return entries.to_json()

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

        """
        # print(current_user.username)
        parser.add_argument("title", required=True)
        parser.add_argument("content", required=True)
        args = parser.parse_args()
        title = args["title"]
        content = args["content"]

        if current_user != None:
            author = get_user_by_id(current_user.id)
            newEntry = Entry(
                title=title, content=content, author=author, date=date.today()
            ).save()
            return {
                "title": newEntry.title,
                "content": newEntry.content,
                "author": newEntry.author.username,
                "date": newEntry.date,
            }
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
                "password": user.password,
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
        """
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("usertype", type=inputs.boolean, required=True)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        usertype = args["usertype"]
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )
        user = get_user_by_username(username)

        if user != None:
            return {"err": "username is used"}, 400
        newUser = User(
            username=username, password=hashed_password, usertype=usertype
        ).save()

        return {
            "username": newUser.username,
            "password": newUser.password,
            "usertype": newUser.usertype,
        }

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
                description: Returns access token
            400:
                description: Login failed
        """
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        user = get_user_by_username(username)
        password_check = check_password_hash(user.password, password)
        print(password_check)

        if user != None and password_check:
            access_token = create_access_token(identity=user)
            print(get_id_by_user(user))
            print(user.id)
            return jsonify(access_token=access_token)

        return {"err": "login fail"}, 400

    @jwt_required()
    def delete(self):
        """Logout
        responses:
            200:
                description: logout success
        """

        jti = get_jwt()["jti"]
        blockedToken = TokenBlockList(jti=jti)
        blockedToken.save()
        return {"msg": "logout success"}


api.add_resource(EntryList, "/", "/entries")
api.add_resource(SingleEntry, "/entries/<string:entry_id>")
api.add_resource(UserList, "/users/<string:user_id>", "/users/register", "/users")
api.add_resource(SingleUser, "/login")

if __name__ == "__main__":
    app.run(debug=True)


# sudo systemctl start mongod
# pipenv run python3 app.py
