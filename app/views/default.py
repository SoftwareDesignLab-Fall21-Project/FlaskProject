from flask import Blueprint, render_template

bp = Blueprint('test', __name__, url_prefix='/')


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
