from flask import current_app
from app import db
from datetime import datetime

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

	def complete(self):
		self.completed = True
		db.session.commit ()

	def delete (self):
		db.session.delete(self)
		db.session.commit()


# Delete all records of a grammar check
def delete_all_student_goals_from_user_id(user_id):
	goals = StudentGoal.query.filter_by(user_id=user_id).all()
	if goals is not None:
		for goal in goals:
			db.session.delete(goal)
	db.session.commit()
