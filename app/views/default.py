from flask import Flask, Blueprint, render_template, Response, jsonify
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
from database import mongo

bp = Blueprint('test', __name__, url_prefix='/')



@bp.route('/hwcapacity', methods=["GET"])
@cross_origin()
def getHwCapacity():
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


@bp.route('/set-capacity/<id>', methods=["PATCH"])
def set_capacity(id):
    print(set_capacity)
    try:
        dbResponse = mongo.db.HardwareSets.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"Capacity":request.form["Capacity"]}}
        )
        for attr in dir(dbResponse):
            print(f"{attr}")
        return Response(
            response = jsonify({
                "message":"capacity updated"
            }),
            status = 200,
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = jsonify({
                "message":"unable to update capacity"
            }),
            status = 500,
        )

@bp.route('/set-available/<id>', methods=["PATCH"])
def set_available(id):
    print(set_available)
    try:
        dbResponse = mongo.db.HardwareSets.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"Available":request.form["Available"]}}
        )
        for attr in dir(dbResponse):
            print(f"{attr}")
        return Response(
            response = jsonify({
                "message":"availability updated"
            }),
            status = 200,
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = jsonify({
                "message":"unable to update availability"
            }),
            status = 500,
        )

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


"""

react client calls <flask server>/datasetList
flask server gives list of datasets with info including names, urls, etc...
react client makes fancy list from that
user clicks button
react client calls <flask server>/datasets/<selected file>
<flask server> gives response, and response is downloaded to client computer

http://192.168.18.245:8080/datasets/abdominal-and-direct-fetal-ecg-database-1.0.0.zip


"""
