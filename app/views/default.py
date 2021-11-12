from flask import Blueprint, render_template, Response, jsonify, request, flash, url_for, redirect, session, send_from_directory
from flask_cors import cross_origin
from bson.objectid import ObjectId
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from pymongo import MongoClient
import ssl
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
    session.pop("user", None)
    session.pop("projects", None)
    return jsonify({'success': 'false'})

@bp.route('/get-hardware', methods=["GET"])
def get_hardware():
    output = []
    for sets in mongo.db.HardwareSets.find():
        output.append({'Name': sets['Name'], 'Capacity': sets['Capacity'], 'Available': sets['Available']})
    return jsonify({'result' : output})

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
                projects.append({'Name': sets['Name'], 'HardwareSet1': sets['HardwareSet1'], 'HardwareSet2': sets['HardwareSet2'], 'Users' : sets['Users']})
        return jsonify({'success': 'true', 'user' : user, 'hardware': hardware, 'projects' : projects})
    else:
        return jsonify([{'success': 'false'}])

@bp.route('/get-user', methods=["GET"])
def get_user():
    if "user" in session:
        user = session["user"]
        projects = session["projects"]
        return jsonify({'success': 'true', 'user' : user, 'projects': projects})
    else:
        return jsonify([{'success': 'false'}])

        


@bp.route("/")
def get_site():
    return render_template("site.html")


@bp.route("/datasets")
def get_datasets():
    """ Get the valid datasets stored on this server.
    :return: A json file containing info for all valid datasets stored on this server.
    """
    # TODO
    return "{}"


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
    try:
        message = ''
        if request.method == 'POST':
            username = request.form['username']  # access the data inside 
            password = request.form['password']

            col = mongo.db.Users
            login_user = col.find_one({'username': username})
            print(login_user)

            if login_user:
                message = "here"
                hashpass = login_user['passhash']
                print(request.referrer)
                if password == hashpass:  # if this is the correct password
                    session["user"] = username
                    session["projects"] = login_user['Projects']
                    return redirect(request.referrer)
            else:
                message = "Wrong username or password"
        return message

    except Exception as e:
        print("Invalid credentials, try again.")
        return redirect(request.referrer)


@bp.route("/signup/", methods=["GET", "POST"])
def register_page():
    try:

        if request.method == "POST":
            username = request.form.get("newuser")
            password = request.form.get("newpass")
            # password = sha256_crypt.encrypt((str(form.password.data)))

            # if int(x) > 0:
            #     flash("That username is already taken, please choose another")
            #     return render_template('register.html', form=form)

            # else:
            #     c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
            #               (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

            #     conn.commit()
            #     flash("Thanks for registering!")
            #     c.close()
            #     conn.close()
            #     gc.collect()

            #     session['logged_in'] = True
            #     session['username'] = username

            # return redirect(url_for('dashboard'))

        # return a template for the login form if we receive a GET request
        # return render_template("register.html", form=form)
        # flash("Thanks for registering!")
        return redirect(url_for('test'))

    except Exception as e:
        return (str(e))


"""

react client calls <flask server>/datasetList
flask server gives list of datasets with info including names, urls, etc...
react client makes fancy list from that
user clicks button
react client calls <flask server>/datasets/<selected file>
<flask server> gives response, and response is downloaded to client computer

http://192.168.18.245:8080/datasets/abdominal-and-direct-fetal-ecg-database-1.0.0.zip


"""
