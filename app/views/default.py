from flask import Blueprint, render_template, Response, jsonify, request
from flask_cors import cross_origin
from bson.objectid import ObjectId
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


@bp.route('/get-hardware', methods=["GET"])
def get_hardware():
    col = mongo.db.HardwareSets
    documents = list(col.find())
    return jsonify(documents)


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


@bp.route("/")
def get_site():
    return render_template("site.html")

