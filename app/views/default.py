from flask import Blueprint, render_template

bp = Blueprint('test', __name__, url_prefix='/')


@bp.route("/")
def get_site():
    return render_template("site.html")