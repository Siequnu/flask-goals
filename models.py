from flask import current_app
from app import db
from datetime import datetime

class StudentGoal (db.Model):
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	goal_title = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
	
	def __repr__(self):
		return '<Student Goal {}>'.format(self.id)


# Delete all records of a grammar check
def delete_all_student_goals_from_user_id(user_id):
	goals = StudentGoal.query.filter_by(user_id=user_id).all()
	if goals is not None:
		for goal in goals:
			db.session.delete(goal)
	db.session.commit()
