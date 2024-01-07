from flask import Flask, request, render_template, redirect,flash, session
from flask_debugtoolbar import DebugToolbarExtension
from survey import satisfaction_survey as survey 

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "hush-hush!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def select_survey():
    return render_template('survey.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def got_answers():

    # get the choice
    choice = request.form['answer']

    # add responses
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses


    if(len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')
    
@app.route("/questions/<int:id>")
def show_question(id):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # if user skips question
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # completed questions
        return redirect("/complete")

    if (len(responses) != id):
        # invalid question 
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template("questions.html", question_num=id, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completed.html")