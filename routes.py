from flask import render_template, flash, redirect, url_for, request, abort, current_app, session, Response
from flask_login import current_user, login_required

from . import bp
from .models import StudentGoal
from .forms import StudentGoalForm

import app.models
from app.models import User


# Main overview of student goals
@bp.route("/view/")
@login_required
def view_goals():
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		goals = StudentGoal.query.all()
		return render_template('view_goals.html', goals=goals)
	abort(403)


# Search for a student
@bp.route("/add/search")
@login_required
def add_goal_find_student():
	# View a list of consultations
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		students = User.query.filter_by(is_admin=False).all()
		return render_template('goals_search_student.html', students=students)


# Create a new goal
@bp.route("/add/<student_id>")
@login_required
def add_goal(student_id):
	# View a list of consultations
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		form = StudentGoalForm()
		student = User.query.filter_by(id=student_id).first()
		if student is None:
			flash('Could not locate this student.', 'error')
			return redirect(url_for('goals.view_goals'))
		else:
			if form.validate_on_submit():
				goal = StudentGoal()
				goal.save()
				flash ('Goal saved', 'success')
				return redirect(url_for('goals.view_goals'))
			return render_template('add_goal.html', form = form, title = 'Add student goal', student = student)
	else:
		abort (403)