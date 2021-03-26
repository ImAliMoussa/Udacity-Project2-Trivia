# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

These environment variables are set in the `.flaskenv` file and are detected when running the server.
## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET '/questions?page={INSERT_PAGE_NUM}'
DELETE '/questions/{INSERT_QUESTION_ID}'
POST '/questions'
POST '/questions/search'
GET '/categories/{INSERT_CATEGORY_ID}/questions'
POST '/quizzes'

```
***

```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Path parameters: None
- Query parameters: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}

GET '/questions?page={INSERT_PAGE_NUM}'
- Fetches a list of questions, categories and the total number of questions in the database
- Path parameters: None
- Query parameters:
  - page : questions are paginated and each page returns up to 10 questions
  - if page is omitted then the first page is returned by default
- Example route: '/questions?page=1'
- Fetches several attributes
  1. Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  2. Fetches a list of questions, each question is a dictionary of attributes and values. Attributes are id, question, answer, category and difficulty
  3. total_questions which is the total number of questions in the database
{
    "categories": {
        "1": "Science",
        "2": "Art",
        ...
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "total_questions": 22
}


DELETE '/questions/{INSERT_QUESTION_ID}'
- Sends a request to delete a question from the database
- Path parameters:
  - id: id of the question to be deleted, id is an integer
- Query parameters: None
- Path parameter is the 
- Example route: '/questions/1'
- Response of a successful deletion:
{
    "success": true
}

POST '/questions'
- Sends a request to post a new question to the database
- Path parameters: None
- Query parameters: None
- JSON body should contain a dictionary of required attributes, all attributes are required for a successful post request.
- Example body of the request:
{
    "question": "What does a cat say?",
    "answer": "Meow",
    "difficulty": 1,
    "category": 1
}
- Response
{
    "success": true
}


POST '/questions/search'
- Fetches questions that contains a search term as a substring in the question
- Path parameters: None
- Query parameters: None
- JSON body should contain a single attribute "searchTerm" which is the substring that is searched in the database
- Fetches a dictionary that contains 2 attributes
  - questions: list of questions, each question is a dictionary of attributes and their values. Attributes are id, question, answer, category and difficulty.
  - total_questions: length of the questions list
- Example body of the request:
{
    "searchTerm": "what"
}
- Response
{
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        ...
    ],
    "total_questions": 12
}


GET '/categories/{INSERT_CATEGORY_ID}/questions'
- Fetches all questions of a specific category
- Path parameters: 
  - category id: integer of the required category
- Query parameters: None
- Example route: '/categories/1/questions'
- Fetches a dictionary that contains 3 attributes
  - questions: list of questions, each question is a dictionary of attributes and their values. Attributes are id, question, answer, category and difficulty.
  - total_questions: length of the questions list
  - current_category: integer of the required category
- Response
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        ...
    ],
    "total_questions": 7
}


POST '/quizzes'
- Fetches a question per request for the quiz
- Path parameters: None
- Query parameters: None
- Response contains a single attribute question which has 2 possible values
  - A dictionary of attributes. Attributes are id, question, answer, category and difficulty.
  - null, this signals the quiz has ended
- JSON body of the request has 2 attributes:
  - previous_questions: 
    - required
    - a list of questions that have already been asked in the quiz
  - quiz_category
    - optional
    - a dictionary containing a single attribute: id
- Example json body of request 
{
    "previous_questions": [],
    "quiz_category": {
        "id": 1
    }
}
- Response
{
    "question": {
        "answer": "Woof",
        "category": 1,
        "difficulty": 1,
        "id": 26,
        "question": "What does the dog say?"
    }
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
