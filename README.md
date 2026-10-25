# Workout Tracking REST API

A Flask REST API for tracking workouts, exercises, and the exercises performed
in each workout. Built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow,
backed by SQLite.

## Features

- Manage workouts and exercises (create, list, view, delete)
- Record which exercises belong to a workout, with reps / sets / duration
- Input validation and uniform JSON error responses
- Automated test suite (pytest) with an in-memory database

## Tech Stack

- Python 3.8
- Flask + Flask-SQLAlchemy + Flask-Migrate
- Marshmallow (serialization & validation)
- SQLite
- pytest

## Setup

Clone the repo and install dependencies with Pipenv:

```bash
pipenv install --dev
pipenv shell

# create and migrate
cd server
flask db upgrade


python seed.py

#running api
python app.py

#tests
pipenv run pytest -v
#api endpoints

Method 	Endpoint 	Description
GET 	/health 	Health check
GET 	/exercises 	List all exercises
POST 	/exercises 	Create an exercise
GET 	/exercises/<id> 	Get one exercise (with workouts)
DELETE 	/exercises/<id> 	Delete an exercise
GET 	/workouts 	List all workouts
POST 	/workouts 	Create a workout
GET 	/workouts/<id> 	Get one workout (with exercises)
DELETE 	/workouts/<id> 	Delete a workout
POST 	/workouts/<wid>/exercises/<eid>/workout_exercises

#error responses

Status 	Meaning
400 	Validation error (invalid or missing fields)
404 	Resource not found
405 	Method not allowed
409 	Duplicate / integrity conflict
500 	Internal server error