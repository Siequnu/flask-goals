from flask import current_app
from app import db
from datetime import datetime
from app.models import User

class StudentGoal (db.Model):
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	title = db.Column(db.String(140))
	description = db.Column(db.String(250))
	date_due = db.Column(db.DateTime, index=True, default=datetime.now())
	completed = db.Column(db.Boolean, unique=False, default=False)
	
	def __repr__(self):
		return '<Student Goal {}>'.format(self.id)

	def add (self):
		db.session.add(self)
		db.session.commit()

	def toggle_status(self):
		self.completed = not self.completed
		db.session.commit ()

	def delete (self):
		db.session.delete(self)
		db.session.commit()

class StudentGoalTemplate (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	template_data = db.Column(db.String(5000))
	
	def __repr__(self):
		return '<Student Goal Template {}>'.format(self.id)

	def add (self):
		db.session.add(self)
		db.session.commit()

	def delete (self):
		db.session.delete(self)
		db.session.commit()


# Delete all student goals, used when deleting a user
def delete_all_student_goals_from_user_id(user_id):
	goals = StudentGoal.query.filter_by(user_id=user_id).all()
	if goals is not None:
		for goal in goals:
			db.session.delete(goal)
	db.session.commit()

# Get specific goals from a student id
def get_student_goals_from_user_id (user_id):
	return StudentGoal.query.filter_by(student_id = user_id).order_by(StudentGoal.date_due.asc()).all()

# Get goal complete percentage from user id
def get_complete_goal_information_from_user_id (user_id):
	goals = get_student_goals_from_user_id(user_id)
	
	if not goals:
		return False
	else:
		amount_of_goals = len(goals)
		complete_goals = 0
		for goal in goals:
			if goal.completed == True:
				complete_goals += 1
		
		completion_percentage = int(float(complete_goals)/float(amount_of_goals) * 100)

		student_goals_data = {
			'amount_of_goals': amount_of_goals,
			'complete_goals': complete_goals,
			'completion_percentage': completion_percentage,
			'items_remaining': amount_of_goals - complete_goals
		}

		return student_goals_data


# Get all goals info
def get_all_goals_info ():
	students = User.query.filter_by(is_admin = False).all()
	student_goals_info_array = []
	for student in students:
		# Convert SQL object to dictionary and remove personal info
		student_dict = student.__dict__	
		del student_dict['password_hash']

		# Add additional info to this
		student_dict['student_goals'] = get_student_goals_from_user_id (student.id)
		student_dict['student_goals_data'] = get_complete_goal_information_from_user_id (student.id)
		
		# Add this to the main array
		student_goals_info_array.append (student_dict)

	return student_goals_info_array