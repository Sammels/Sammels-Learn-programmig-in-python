"""
Перенесено из webapp2 __init__.py
"""
from flask import Blueprint, render_template
from webapp2.user.decorators import admin_required

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@admin_required
def admin_index():
    title = "Админы на месте"
    return render_template('admin/index.html', title=title)
