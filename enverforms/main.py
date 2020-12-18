import datetime
from typing import List

import dateutil.tz

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash

from . import db, model
from .model import Survey

import flask_login

import json

bp = Blueprint("main", __name__)


@bp.route("/")
@flask_login.login_required
def index():
    current_user = flask_login.current_user
    # loading the surveys created by the current user
    surveys = model.Survey.query.filter_by(user=current_user).order_by(model.Survey.timestamp.desc()).all()
    return render_template("main/index.html", surveys=surveys)


@bp.route("/change_state", methods=["POST"])
@flask_login.login_required
def change_state():
    survey = model.Survey.query.filter_by(id=request.form.get("survey_id")).first()
    print(request.form.get("state"))
    if request.form.get("state") == "new":
        survey.state = model.SurveyState.new
    elif request.form.get("state") == "online":
        survey.state = model.SurveyState.online
    elif request.form.get("state")=="closed":
        survey.state = model.SurveyState.closed
    db.session.commit()

    current_user = flask_login.current_user
    # loading the surveys created by the current user
    surveys = model.Survey.query.filter_by(user=current_user).order_by(model.Survey.timestamp.desc()).all()
    return render_template("main/index.html", surveys=surveys)

@bp.route("/remove_survey/<int:survey_id>")
@flask_login.login_required
def remove_survey(survey_id):
    # removing the selected survey
    model.Survey.query.filter_by(id=survey_id).delete()
    db.session.commit()

    current_user = flask_login.current_user
    # loading the surveys created by the current user
    surveys = model.Survey.query.filter_by(user=current_user).order_by(
        model.Survey.timestamp.asc()).all()
    return render_template("main/index.html", surveys=surveys)


@bp.route("/add_survey")
@flask_login.login_required
def add_survey():
    return render_template("main/add_survey.html")


@bp.route("/edit_survey/<int:survey_id>")
@flask_login.login_required
def edit_survey(survey_id):
    current_user = flask_login.current_user
    survey = model.Survey.query.filter_by(id=survey_id).first()
    if not survey:
        abort(404, "Suervey id {} doesn't exist.".format(survey_id))
    if current_user.id != survey.user_id:
        abort(404, "Survey %s is not editable through this user, try to login with another account."%(survey.title))
    if survey.state != model.SurveyState.new:
        abort(404, "Survey %s cannot be edited right now."%(survey.title))
    return render_template("main/edit_survey.html", survey=survey)


@bp.route("/add_survey", methods=["POST"])
@bp.route("/edit_survey", methods=["POST"])
@flask_login.login_required
def post_survey():
    # requesting data from the forms
    dic = request.values
    survey_id = request.form.get('survey_id')
    if survey_id:
        # if it is an edited survey, remove that survey
        model.Survey.query.filter_by(id=survey_id).delete()

    # getting the survey data from the forms
    text_title = dic["title"]
    text_description = dic["description"]

    # getting the questions data from the forms
    questions = [i[1] for i in dic.items() if "statement" in i[0]]
    question_types = [i[1] for i in dic.items() if "type" in i[0]]
    options = []

    # getting the options data from the forms
    for q in range(1, len(questions)+1):
        options += [[i[1] for i in dic.items() if "option"+str(q) in i[0]]]
    
    # creating the survey instance
    survey = model.Survey(
        user=flask_login.current_user,
        title=text_title,
        description=text_description,
        state=model.SurveyState.new,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )
    db.session.add(survey)
    
    for i in range(len(questions)):
        # creating the question instances
        text_statement = questions[i]
        question_type = question_types[i]
        question = model.Question(
            survey=survey,
            statement=text_statement,
            type=question_type,
            position=i
        )
        db.session.add(question)

        if question_type == "3" or question_type == "4":
            for j, text_option in enumerate(options[i]):
                # creating the option instances
                option = model.Option(
                    question=question,
                    statement=text_option,
                    position=j
                )
                db.session.add(option)

    # uploading to the database and redirecting
    db.session.commit()
    return redirect(url_for("main.index"))


@bp.route("/answer/<int:survey_id>")
def answer(survey_id):
    survey = model.Survey.query.filter_by(id=survey_id).first()
    if not survey:
        abort(404, "Survey id {} doesn't exist.".format(survey_id))
    if survey.state != model.SurveyState.online:
        abort(404, "The survey %s cannot be answered, it is currently closed."%(survey.title))
    return render_template("main/answer.html", survey=survey)


@bp.route("/answer/<int:survey_id>", methods=["POST"])
def post_answer(survey_id):
    # creating the survey instance
    survey = model.Survey.query.filter_by(id=survey_id).first()
    survey_answer = model.Sanswer(
        survey=survey,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )
    db.session.add(survey_answer)
    
    # storing the requested data from the forms
    for i, question in enumerate(survey.questions):
        # creating the answers instances
        if question.type=="1":
            question_answer = model.Qanswer(      
                sanswer=survey_answer,
                question=question,
                text=request.form.get(str(i))
            )
            db.session.add(question_answer)
        elif question.type == "2":
            if request.form.get(str(i))=="":
                question_answer = model.Qanswer(
                    sanswer=survey_answer,
                    question=question,
                )
            else:
                question_answer = model.Qanswer(
                    sanswer=survey_answer,
                    question=question,
                    integer=request.form.get(str(i))
                )
            db.session.add(question_answer)
        else:
            options_inds = request.form.getlist(str(i))
            for option_ind in options_inds:
                option = model.Option.query.filter_by(
                    question=question, position=int(option_ind)).first()
                question_answer = model.Qanswer(
                    sanswer=survey_answer,
                    question=question,
                    option=option,
                )
                db.session.add(question_answer)
    
    # uploading to the database and redirecting
    db.session.commit()
    return render_template("main/congratulations.html", survey=survey)


@bp.route("/view_answers/<int:survey_id>")
@flask_login.login_required
def view_answers(survey_id):
    # rendering the view answers page
    survey = model.Survey.query.filter_by(id=survey_id).first()
    current_user = flask_login.current_user
    if not survey:
        abort(404, "Post id {} doesn't exist.".format(survey_id))

    if current_user.id != survey.user_id:
        abort(404, "The answers of this survey are private, try with a diferent account")

    if survey.state == model.SurveyState.new:
        abort(404, "The answers of survey {} are not accesible".format(survey.title))
    
    # creating arrays to store the answers and the types of questions
    answers = []
    question_types = []
    question_statements = []

    # storing the answers depending of the type each question
    for question in survey.questions:
        question_answers = []
        question_types += [question.type]
        question_statements += [question.statement]
        if question.type == "1":
            for answer in question.q_answers:
                question_answers += [answer.text]
            answers += [question_answers]
        if question.type == "2":
            for answer in question.q_answers:
                question_answers += [[answer.integer]]
            answers += [question_answers]
        if question.type == "3" or question.type == "4":
            for answer in question.q_answers:
                option = model.Option.query.filter_by(
                    id=answer.question_option_id).first()
                option_text = option.statement
                question_answers += [option_text]
            options_labels = []
            [options_labels.append(
                i) for i in question_answers if i not in options_labels]
            options_count = [question_answers.count(i) for i in options_labels]
            answers += [[[i, j] for i, j in zip(options_labels, options_count)]]

    return render_template("main/view_answers.html", survey=survey, answers=json.dumps(answers), 
                           qtypes=json.dumps(question_types), qstatements=json.dumps(question_statements))


# @bp.route("/user/<int:user_id>")
# @flask_login.login_required
# def user(user_id):
#     user = model.User.query.filter_by(id=user_id).first()
#     messages = model.Survey.query.filter_by(user=user).order_by(model.Survey.timestamp.desc()).all()
#     if not user:
#         abort(404, "User id {} doesn't exist.".format(user_id))
#     return render_template("main/profile.html", posts=messages)




