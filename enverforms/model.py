from . import db
import flask_login

import enum

class SurveyState(enum.Enum):
    new = 1
    online = 2
    closed = 3

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    surveys = db.relationship('Survey', backref='user',
                              lazy=True, passive_deletes=True)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(912))
    state = db.Column(db.Enum(SurveyState), nullable=False)
    timestamp = db.Column(db.Date(), nullable=False)
    questions = db.relationship(
        'Question', backref='survey', lazy=True, passive_deletes=True)
    s_answers = db.relationship(
        'Sanswer', backref='survey', lazy=True, passive_deletes=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey(
        'survey.id', ondelete='CASCADE'), nullable=False)
    statement = db.Column(db.String(512), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    q_answers = db.relationship(
        'Qanswer', backref='question', lazy=True, passive_deletes=True)
    options = db.relationship(
        'Option', backref='question', lazy=True, passive_deletes=True)


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id', ondelete='CASCADE'), nullable=False)
    statement = db.Column(db.String(512), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    chosen_in = db.relationship(
        'Qanswer', backref='option', lazy=True, passive_deletes=True)


class Sanswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey(
        'survey.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    s_a_answers = db.relationship(
        'Qanswer', backref='sanswer', lazy=True, passive_deletes=True)


class Qanswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_answer_id = db.Column(db.Integer, db.ForeignKey(
        'sanswer.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question_option_id = db.Column(
        db.Integer, db.ForeignKey('option.id', ondelete='CASCADE'))
    text = db.Column(db.String(512))
    integer = db.Column(db.Integer)
