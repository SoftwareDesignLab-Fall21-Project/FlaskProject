from flask import Blueprint, render_template, Response, jsonify, request, flash, url_for, redirect, session, send_from_directory
from flask_cors import cross_origin
from bson.objectid import ObjectId
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from pymongo import MongoClient
import ssl
from app.scripts import mongo

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


@bp.route('/get-hardware', methods=["GET"])
def get_hardware():
    output = []
    for sets in mongo.db.HardwareSets.find():
        output.append({'Name': sets['Name'], 'Capacity': sets['Capacity'], 'Available': sets['Available']})
    return jsonify({'result' : output})


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
            username = request.form.get('username')  # access the data inside 
            print(username)
            password = request.form.get('password')
            print(password)

            # client = MongoClient(
            #     "mongodb+srv://tbertolino:softwarelabfall2021@cluster0.mphmj.mongodb.net/SoftwareDesignLab-Fall21-Project?retryWrites=true&w=majority",
            #     ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
            currentDB = mongo.db['SoftwareDesignLab-Fall21-Project']
            col = currentDB['Users']
            # col = mongo.db.Users # our collection of user information
            login_user = col.find_one({'username': username})
            message = login_user['username']
            if login_user:
                hashpass = login_user['passhash']
                if hashpass == password:
                    if sha256_crypt.verify(password, hashpass):
                        session['logged_in'] = True
                        session['username'] = request.form['username']
                        print("session success")
                        return "Nice"
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
