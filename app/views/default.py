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


@bp.route("/checkout-hw", methods=["POST"])
def checkout_hw():
    try:
        if "user" in session:
            project_name = request.form['project_name']
            hw_name = request.form['hw_name']
            number = int(request.form['number'])
            if number < 1:
                raise ValueError

            user = mongo.db.Users.find_one({'username': session["user"]})
            if user is None or project_name not in user["Projects"]:
                return jsonify([{'success': 'false', 'reason': "User authentication failed, reload the page."}])

            project = mongo.db.Projects.find_one({'Name': project_name})
            if project is None:
                return jsonify([{'success': 'false', 'reason': "Project doesn't exist."}])

            hw_set = mongo.db.HardwareSets.find_one({'Name': hw_name})
            if hw_set is None or int(hw_set['Available']) < number:
                return jsonify([{'success': 'false', 'reason': "Bad number of stuff."}])

            mongo.db.Projects.update_one(
                {"_id": project["_id"]},
                {"$set": {hw_name: (int(project[hw_name]) + number)}}
            )

            mongo.db.HardwareSets.update_one(
                {"_id": hw_set["_id"]},
                {"$set": {"Available": (int(hw_set["Available"]) - number)}}
            )

            return jsonify([{'success': 'true'}])
    except ValueError as e:
        print(e)
        return jsonify([{'success': 'false'}])

    return jsonify([{'success': 'false'}])


@bp.route("/return-hw", methods=["POST"])
def return_hw():
    try:
        if "user" in session:
            project_name = request.form['project_name']
            hw_name = request.form['hw_name']
            number = int(request.form['number'])
            if number < 1:
                raise ValueError

            user = mongo.db.Users.find_one({'username': session["user"]})
            if user is None or project_name not in user["Projects"]:
                return jsonify([{'success': 'false', 'reason': "User authentication failed, reload the page."}])

            project = mongo.db.Projects.find_one({'Name': project_name})
            if project is None or int(project[hw_name]) < number:
                return jsonify([{'success': 'false', 'reason': "Bad number of stuff."}])

            hw_set = mongo.db.HardwareSets.find_one({'Name': hw_name})
            if hw_set is None:
                return jsonify([{'success': 'false', 'reason': "Hardware set doesn't exist."}])

            mongo.db.Projects.update_one(
                {"_id": project["_id"]},
                {"$set": {hw_name: (int(project[hw_name]) - number)}}
            )

            mongo.db.HardwareSets.update_one(
                {"_id": hw_set["_id"]},
                {"$set": {"Available": (int(hw_set["Available"]) + number)}}
            )

            return jsonify([{'success': 'true'}])
    except ValueError as e:
        print(e)
        return jsonify([{'success': 'false'}])

    return jsonify([{'success': 'false'}])


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
        print(user)
        return jsonify({'success': 'true', 'user': user, 'Projects': projects})
    else:
        return jsonify([{'success': 'false'}])


# @bp.route('/create-project', methods=['POST'])
# def create_project():
#     if "user" in session:
#         project_name = request.form["project_name"]
#         project_description = request.form["project_description"]
#         project_id = request.form["project_id"]
#         user = mongo.db.Users.find_one({'username': session["user"]})
#
#         if user is None:
#             return jsonify([{'success': 'false', 'reason': 'Authentication error', 'error_no': 1}])
#
#         projects = user["Projects"]
#         if project_name in projects:
#             return jsonify([{'success': 'false', 'reason': 'Project exists', 'error_no': 2}])
#
#
#
#         return jsonify([{'success': 'true', 'reason': 'Project already exists', 'error_no': 0}])
#     else:
#         return jsonify([{'success': 'false', 'reason': 'Project already exists', 'error_no': -1}])

@bp.route("/create-project", methods=["POST"])
def create_project():
    if "user" not in session:
        return jsonify([{'success': 'false'}])

    try:
        project_name = request.form['project_name']  # access the data inside
        project_description = request.form['project_description']
        project_id = request.form['project_id']

        # TODO: clean incoming data to prevent injection

        col = mongo.db.Projects
        is_already_made = col.find_one({'Name': project_name})
        user = mongo.db.Users.find_one({'username': session["user"]})

        if user is None:
            return jsonify([{'success': 'false', 'reason': "User authentication failed, reload the page."}])

        if is_already_made:
            return jsonify([{'success': 'false', 'reason': "That project name is already taken."}])
        else:
            project = {'Name': project_name, 'HardwareSet1': "0", 'HardwareSet2': "0", 'Users': [session["user"]]}
            col.insert_one(project)  # add this new user to the db

            db_response = mongo.db.Users.update_one(
                {"_id": ObjectId(user["_id"])},
                {"$push": {"Projects": project_name}}
            )
            return jsonify([{'success': 'true'}])

    except Exception as e:
        print(e)
        return jsonify([{'success': 'false', 'reason': "Internal error."}])



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
            session["Projects"] = user['Projects']
            session["Projects"] = []
            col.insert_one(user)  # add this new user to the db

            msg = "New user registered."
            return msg

    except Exception as e:
        return (str(e))
