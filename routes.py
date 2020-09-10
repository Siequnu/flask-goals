from flask import render_template, flash, redirect, url_for, request, abort, current_app, session, Response
from flask_login import current_user, login_required

from . import bp, models
from .models import StudentGoal, StudentGoalTemplate
from .forms import StudentGoalForm

import app.models
from app.models import User

import json


# Main overview of student goals
@bp.route("/view")
@login_required
def view_goals():
	if app.models.is_admin(current_user.username):
		student_goals_info_array = models.get_all_goals_info ()
		goals = StudentGoal.query.all()
		students = User.query.filter_by(is_admin = False).all()
		return render_template('view_goals.html', student_goals_info_array = student_goals_info_array, goals=goals, students = students)
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
	goal_templates = StudentGoalTemplate.query.all ()
	if app.models.is_admin(current_user.username) or current_user.id == student_id:
		return render_template('view_student_goals.html', goals = goals, student = student, goal_templates = goal_templates)
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



# Remove goal
@bp.route("/remove/<int:goal_id>")
@login_required
def remove_goal(goal_id):
	if app.models.is_admin(current_user.username):
		goal = StudentGoal.query.get(goal_id)
		student = User.query.get (goal.student_id)
		if goal is None:
			flash ('Could not find this goal.', 'error')
		else:
			goal.delete ()
			flash ('Goal deleted successfully.', 'success')
		return redirect (url_for('goals.view_student_goals', student_id = student.id))
	else:
		abort (403)


# Admin redirect route to mark a goal as completed
@bp.route("/completed/<goal_id>")
@login_required
def toggle_goal_status(goal_id):
	# View a list of consultations
	if current_user.is_authenticated and app.models.is_admin(current_user.username):
		goal = StudentGoal.query.get(goal_id)
		if goal is None:
			flash('Could not locate this goal.', 'error')
			return redirect(url_for('goals.view_goals'))
		
		student = User.query.get(goal.student_id)
		if student is None:
			flash('Could not locate this student.', 'error')
			return redirect(url_for('goals.view_goals'))
		goal.toggle_status()
		return redirect (url_for('goals.view_student_goals', student_id = student.id))
	else:
		abort (403)


# Goal template management
@bp.route("/templates")
@login_required
def manage_goal_templates():
	if app.models.is_admin(current_user.username):
		student_goal_templates = StudentGoalTemplate.query.all() # These are saved as JSON.stringify from the API
		parsed_templates = []
		for template in student_goal_templates:
			parsed_templates.append ({
				'id': template.id,
				'title': template.title,
				'template_data': json.loads (template.template_data)
			})
		return render_template('manage_goal_templates.html', student_goal_templates = parsed_templates)
	else:
		abort (403)

# Apply a goal template
@bp.route("/template/<int:template_id>/apply/<int:user_id>")
@login_required
def apply_goal_template(template_id, user_id):
	if app.models.is_admin(current_user.username):
		student_goal_template = StudentGoalTemplate.query.get(template_id)
		user = User.query.get (user_id)

		if student_goal_template is None or user is None:
			flash ('Could not find the template or user', 'warning')
			return redirect (url_for ('goals.view_goals'))
		
		parsed_template_data = json.loads (student_goal_template.template_data)
		for goal in parsed_template_data:
			new_goal = StudentGoal (
				student_id = user_id,
				title = goal['title'],
				description = goal['description'],
				date_due = goal['datefield']
			)
			new_goal.add ()
		flash ('Applied the ' + student_goal_template.title + ' template to ')
		return redirect (url_for('goals.view_student_goals', student_id = user_id))
	else:
		abort (403)


# Add goal template
@bp.route("/templates/add")
@login_required
def add_goal_template():
	if app.models.is_admin(current_user.username):
		form = StudentGoalForm ()
		return render_template('add_goal_template.html', form = form)
	else:
		abort (403)


# Remove goal template
@bp.route("/templates/remove/<int:template_id>")
@login_required
def remove_goal_template(template_id):
	if app.models.is_admin(current_user.username):
		template = StudentGoalTemplate.query.get(template_id)
		if template is None:
			flash ('Could not find this template.', 'error')
		else:
			template.delete ()
			flash ('Template deleted successfully.', 'success')
		return redirect (url_for('goals.manage_goal_templates'))
	else:
		abort (403)