from flask import Blueprint, render_template, Response, jsonify, request, flash, url_for, redirect, session, \
    send_from_directory
from flask_cors import cross_origin
from bson.objectid import ObjectId
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from app.scripts import mongo, check_hash

bp = Blueprint('test', __name__, url_prefix='/')


@bp.route('/hwcapacity', methods=["GET"])
@cross_origin()
def get_hw_capacity():
    """
    using placeholder until DB is setup
    :return: the capacity of the hardware sets
    """
    col = mongo.db.HardwareSets
    col.insert_one({
        "HardwareSet": "3",
        "Capacity": "2",
        "Availability": "3"
    })
    print(col.find_one())
    return {
        "Set 1": "5",
    }


# @bp.route('/get-hardware', methods=["GET"])
# def get_hardware():
#     col = mongo.db.HardwareSets
#     documents = list(col.find())
#     return jsonify(documents)


@bp.route('/set-capacity/<id>', methods=["PATCH"])
def set_capacity(id):
    print(set_capacity)
    try:
        db_response = mongo.db.HardwareSets.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"Capacity": request.form["Capacity"]}}
        )
        for attr in dir(db_response):
            print(f"{attr}")
        return Response(
            response=jsonify({
                "message": "capacity updated"
            }),
            status=200,
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=jsonify({
                "message": "unable to update capacity"
            }),
            status=500,
        )


@bp.route('/set-available/<id>', methods=["PATCH"])
def set_available(id):
    print(set_available)
    try:
        db_response = mongo.db.HardwareSets.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"Available": request.form["Available"]}}
        )
        for attr in dir(db_response):
            print(f"{attr}")
        return Response(
            response=jsonify({
                "message": "availability updated"
            }),
            status=200,
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=jsonify({
                "message": "unable to update availability"
            }),
            status=500,
        )


@bp.route('/logout', methods=["GET"])
def logout_user():
    session.clear()
    return jsonify({'success': 'true'})


@bp.route('/get-hardware', methods=["GET"])
def get_hardware():
    output = []
    for sets in mongo.db.HardwareSets.find():
        output.append({'Name': sets['Name'], 'Capacity': sets['Capacity'], 'Available': sets['Available']})
    return jsonify({'result': output})


@bp.route('/get-db', methods=["GET"])
def get_db():
    hardware = []
    projects = []
    if "user" in session:
        user = session["user"]
        for sets in mongo.db.HardwareSets.find():
            hardware.append({'Name': sets['Name'], 'Capacity': sets['Capacity'], 'Available': sets['Available']})
        for sets in mongo.db.Projects.find():
            if user in sets['Users']:
                projects.append(
                    {'Name': sets['Name'], 'HardwareSet1': sets['HardwareSet1'], 'HardwareSet2': sets['HardwareSet2'],
                     'Users': sets['Users']})
        return jsonify({'success': 'true', 'user': user, 'hardware': hardware, 'projects': projects})
    else:
        return jsonify([{'success': 'false'}])


@bp.route('/get-user', methods=["GET"])
def get_user():
    if "user" in session:
        user = session["user"]
        projects = session["Projects"]
        return jsonify({'success': 'true', 'user': user, 'Projects': projects})
    else:
        return jsonify([{'success': 'false'}])


@bp.route("/")
def get_site():
    return render_template("site.html")


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    # email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)',
                              [validators.InputRequired()])


@bp.route("/login", methods=['POST'])
def login_page():
    # if 'user' in session:
    #     return "Success"
    session.clear()
    try:
        message = ''
        username = request.form['username']  # access the data inside
        password = request.form['password']

        col = mongo.db.Users
        login_user = col.find_one({'username': username})
        print(login_user)

        if login_user:
            if sha256_crypt.verify(password, login_user['passhash']):
                session["user"] = username
                session["Projects"] = login_user['Projects']

                return "Success"
        else:
            return "Fail"

    except Exception as e:
        print(e)
        return "Fail"


@bp.route("/register", methods=["POST"])
def register_page():
    try:

        username = request.form['newuser']  # access the data inside
        password = request.form['newpass']

        # TODO: clean incoming data to prevent injection

        col = mongo.db.Users  # search to check if username exists already
        login_user = col.find_one({'username': username})

        if login_user:
            msg = "That username is already taken."
            return msg

        else:

            passhash = sha256_crypt.encrypt(str(password))
            user = {'username': username, 'passhash': passhash, 'Projects': [], 'numCollections': 0}
            session["user"] = username
            session["Projects"] = login_user['Projects']
            col.insert_one(user)  # add this new user to the db

            msg = "New user registered."
            return msg

    except Exception as e:
        return (str(e))
