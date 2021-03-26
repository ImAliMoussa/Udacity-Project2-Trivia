import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category
from http import HTTPStatus


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_dialect = "postgresql"
        database_name = "trivia_test"
        database_username = "postgres"
        database_password = "changeme"
        database_host = "localhost:5432"
        self.database_path = f"{database_dialect}://{database_username}:{database_password}@{database_host}/{database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # tests for /categories
    # no tests where this route should fail
    def test_working_get_categories(self):
        res = self.client().get("/categories")
        json_data = res.get_json()
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTrue(json_data.get("categories"))
        self.assertGreater(len(json_data.get("categories")), 0)

    # tests for /questions GET
    def test_working_get_questions_no_page(self):
        res = self.client().get("/questions")
        json_data = res.get_json()
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertGreater(len(json_data.get("questions")), 0)
        self.assertGreater(len(json_data.get("categories")), 0)
        self.assertGreater(json_data.get("total_questions"), 0)

    # not a test, just a helper function
    def getNumberOfQuestionPages(self):
        res = self.client().get("/questions")
        json_data = res.get_json()
        num_questions = int(json_data.get("total_questions"))
        # number of pages is the ceiling of number_questions / questions per page
        num_pages = (num_questions + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
        return num_pages

    # successfully get request
    def test_working_get_questions_with_page(self):
        num_pages = self.getNumberOfQuestionPages()

        for page in range(1, num_pages + 1):
            res = self.client().get("/questions", query_string={"page": page})
            json_data = res.get_json()
            self.assertEqual(res.status_code, HTTPStatus.OK)
            self.assertGreater(len(json_data.get("questions")), 0)
            self.assertGreater(len(json_data.get("categories")), 0)
            self.assertGreater(json_data.get("total_questions"), 0)

    # get request should produce a NOT_FOUND 404 error
    def test_out_of_bounds_page_questions(self):
        num_pages = self.getNumberOfQuestionPages()
        # num_pages + 1 is out of bounds, last correct page is num_pages
        res = self.client().get("/questions", query_string={"page": num_pages + 1})
        json_data = res.get_json()

        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(json_data.get("message"), HTTPStatus.NOT_FOUND.phrase)
        self.assertFalse(json_data.get("success"))

        self.assertFalse(json_data.get("questions"))
        self.assertFalse(json_data.get("categories"))

    # tests for questions delete request
    def test_successful_delete(self):
        # get a single question from db
        setup_res = self.client().get("/questions")
        json_data = setup_res.get_json()

        # get the id of the first question in the result
        key = json_data.get("questions")[0].get("id")

        res = self.client().delete(f"/questions/{key}")
        json_data = res.get_json()

        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTrue(json_data.get("success"))

    def test_unsuccessful_delete(self):
        key_not_in_db = 999999
        res = self.client().delete(f"/questions/{key_not_in_db}")
        json_data = res.get_json()

        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(json_data.get("message"), HTTPStatus.NOT_FOUND.phrase)
        self.assertFalse(json_data.get("success"))

    def test_successful_post_question(self):
        # get one of the categories
        setup_res = self.client().get("/questions")
        json_data = setup_res.get_json()
        category = list(json_data.get("categories"))[0]
        question = {
            "question": "Example question text",
            "answer": "YES!",
            "difficulty": 1,
            "category": category,
        }

        res = self.client().post("/questions", json=question)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTrue(res.get_json().get("success"))

    # this request fails due to a missing required field
    def test_unsuccessful_post_question(self):
        # category is a missing field
        question = {
            "question": "Example question text",
            "answer": "YES!",
            "difficulty": 1,
            # 'category': category
        }

        res = self.client().post("/questions", json=question)
        json = res.get_json()
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(json.get("message"), HTTPStatus.BAD_REQUEST.phrase)
        self.assertFalse(json.get("success"))

    # test search questions functionality
    def test_search_functionality(self):
        body = {"searchTerm": "what"}
        res = self.client().post("/questions/search", json=body)
        json = res.get_json()
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTrue(json.get("questions"))
        self.assertTrue(json.get("total_questions"))

    # test getting questions for a specific category
    def test_get_category_questions(self):
        setup_res = self.client().get("/questions")
        json_data = setup_res.get_json()
        category = list(json_data.get("categories"))[0]
        res = self.client().get(f"categories/{category}/questions")
        json = res.get_json()
        questions = json.get("questions")
        for q in questions:
            self.assertEqual(q.get("category"), int(category))
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertGreater(len(questions), 0)
        self.assertGreater(json.get("total_questions"), 0)

    # test getting questions for unknown category
    def test_get_unknown_category_questions(self):
        category = 9999
        res = self.client().get(f"categories/{category}/questions")
        json = res.get_json()
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        self.assertFalse(json.get("success"))
        self.assertEqual(json.get("message"), HTTPStatus.NOT_FOUND.phrase)

        self.assertFalse(json.get("questions"))
        self.assertFalse(json.get("total_questions"))

    # test quizzes that no question will be repeated
    def test_quiz_no_category(self):
        tmp_res = self.client().get("/questions")
        tmp_json = tmp_res.get_json()
        # get total number of question -> num_questions
        # will make num_questions + 1 requests
        # all will produce status code 200
        # only the last one will return attribute question as None
        # which is not an error but signals the end of the quiz
        num_questions = int(tmp_json.get("total_questions"))
        previous_questions = []
        for i in range(num_questions + 1):
            data = {"previous_questions": previous_questions}
            res = self.client().post("/quizzes", json=data)
            json_res = res.get_json()
            question = json_res.get("question")

            # always 200 OK status code
            self.assertEqual(res.status_code, HTTPStatus.OK)

            if i < num_questions:
                self.assertTrue(json_res.get("question"))
                previous_questions.append(question.get("id"))
            else:
                self.assertFalse(json_res.get("question"))

    # same as last test but for a specific category
    def test_quiz_with_category(self):
        setup_res = self.client().get("/questions")
        json_data = setup_res.get_json()
        category_id = list(json_data.get("categories"))[0]
        category = {"id": category_id}
        res = self.client().get(f"categories/{category_id}/questions")
        json = res.get_json()
        num_questions = int(json.get("total_questions"))
        previous_questions = []
        for i in range(num_questions + 1):
            data = {"previous_questions": previous_questions, "quiz_category": category}
            res = self.client().post("/quizzes", json=data)
            json_res = res.get_json()
            question = json_res.get("question")

            # always 200 OK status code
            self.assertEqual(res.status_code, HTTPStatus.OK)

            if i < num_questions:
                self.assertTrue(json_res.get("question"))
                previous_questions.append(question.get("id"))
            else:
                self.assertFalse(json_res.get("question"))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
