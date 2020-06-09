from flask import render_template, flash, redirect, url_for, request, abort, current_app, session, Response
from flask_login import current_user, login_required

from . import bp
from .models import StudentGoal
import app.models

# Check grammar
@bp.route("/view/")
@login_required
def view_goals():
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		goals = StudentGoal.query.all()
		return render_template('view_goals.html', goals = goals)
	abort (403)