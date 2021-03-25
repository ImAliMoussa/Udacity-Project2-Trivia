from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins. Delete the
    sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def get_all_categories():
        categories_db = Category.query.order_by(Category.type).all()

        categories_dict = {}
        for c in categories_db:
            category_id, category_type = c.id, c.type
            categories_dict[category_id] = category_type

        return jsonify({"categories": categories_dict})

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_all_questions():
        # pagination start and finish
        page = int(request.args.get("page", default="1"))
        start_index = (page - 1) * QUESTIONS_PER_PAGE
        finish_index = start_index + QUESTIONS_PER_PAGE

        # get all questions from db
        questions_db = Question.query.all()
        total_questions = len(questions_db)

        # if page requested is out of range -> return 404 not found
        if start_index >= total_questions:
            return jsonify(success=False), HTTPStatus.NOT_FOUND

        # drop question not in current page
        questions_db = questions_db[start_index:finish_index]
        questions = [q.format() for q in questions_db]

        # get categories from db and format them in key-value pairs for frontend
        categories_db = Category.query.order_by(Category.type).all()

        categories_dict = {}
        for c in categories_db:
            category_id, category_type = c.id, c.type
            categories_dict[category_id] = category_type

        result = {
            "questions": questions,
            "total_questions": total_questions,
            "categories": categories_dict,
            "current_category": None
        }

        return jsonify(result), HTTPStatus.OK

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:key>", methods=["DELETE"])
    def delete_question(key: int):
        question = Question.query.get(key)
        # if question is not found in the database
        if question is None:
            return jsonify(success=False), HTTPStatus.NOT_FOUND

        question.delete()

        return jsonify(success=True), HTTPStatus.OK

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def post_new_question():
        json = request.get_json()

        question_text = json.get("question")
        answer_text = json.get("answer")
        category = json.get("category")
        difficulty = json.get("difficulty")

        # make sure all required data is present
        if (
            question_text is None
            or answer_text is None
            or category is None
            or difficulty is None
        ):
            return jsonify(success=False), HTTPStatus.BAD_REQUEST

        # create new question and add commit to the db
        question = Question(
            question=question_text,
            answer=answer_text,
            category=category,
            difficulty=difficulty,
        )
        question.insert()

        return jsonify(success=True), HTTPStatus.OK

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"])
    def search_questions():
        json = request.get_json()
        search_term = json.get("searchTerm", default="")
        questions_db = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        questions = [q.format() for q in questions_db]
        total_questions = len(questions)

        result = {
            'questions': questions,
            'total_questions': total_questions,
            'current_category': None
        }

        return jsonify(result), HTTPStatus.OK

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
