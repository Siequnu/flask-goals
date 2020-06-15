from flask import render_template, flash, redirect, url_for, request, abort, current_app, session, Response
from flask_login import current_user, login_required

from . import bp, models
from .models import StudentGoal
from .forms import StudentGoalForm

import app.models
from app.models import User


# Main overview of student goals
@bp.route("/view")
@login_required
def view_goals():
	if app.models.is_admin(current_user.username):
		goals = StudentGoal.query.all()
		students = User.query.filter_by(is_admin = False).all()
		return render_template('view_goals.html', goals=goals, students = students)
	else:
		return redirect(url_for('goals.view_student_goals', student_id = current_user.id))


# Get an individual student's goals
@bp.route("/view/<int:student_id>")
@login_required
def view_student_goals(student_id):
	goals = models.get_student_goals_from_user_id (student_id)
	if goals is None: abort (404)
	student = User.query.get(student_id)
	if student is None: abort (404)
	print (current_user.id)
	print (student_id)
	if app.models.is_admin(current_user.username) or current_user.id == student_id:
		return render_template('view_student_goals.html', goals = goals, student = student)
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
@bp.route("/add/<student_id>", methods = ['GET', 'POST'])
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
				goal = StudentGoal(
					title = form.title.data,
					description = form.description.data,
					student_id = student.id,
					date_due = form.datefield.data
				)
				goal.add()
				flash ('Goal saved', 'success')
				return redirect(url_for('goals.view_student_goals', student_id = student.id))
			return render_template('add_goal.html', form = form, title = 'Add student goal', student = student)
	else:
		abort (403)