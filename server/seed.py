import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from datetime import date

from app import app

from models import db, Exercise, Workout, WorkoutExercise


def seed():
    with app.app_context():
        