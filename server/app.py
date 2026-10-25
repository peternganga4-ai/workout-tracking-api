import os

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, MethodNotAllowed

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    ExerciseDetailSchema,
    WorkoutSchema,
    WorkoutDetailSchema,
    WorkoutExerciseWithExerciseSchema,
)


# Enforce SQLite foreign keys on every new connection
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "instance", "app.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# Schema instances (reused across routes)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_detail_schema = WorkoutExerciseWithExerciseSchema()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ---------- Exercises ----------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = exercise_schema.load(request.get_json())
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


# ---------- Workouts ----------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = workout_schema.load(request.get_json())
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)


# ---------- Association: add an exercise to a workout ----------

@app.route(
    "/workouts/<int:wid>/exercises/<int:eid>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(wid, eid):
    workout = db.session.get(Workout, wid)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    exercise = db.session.get(Exercise, eid)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=wid, exercise_id=eid
    ).first()
    if existing is not None:
        return jsonify(
            {"error": "This exercise is already in this workout"}
        ), 409

    data = workout_exercise_detail_schema.load(request.get_json() or {})
    workout_exercise = WorkoutExercise(
        workout_id=wid, exercise_id=eid, **data
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return jsonify(workout_exercise_detail_schema.dump(workout_exercise)), 201


# ---------- Global error handlers ----------

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400


@app.errorhandler(NotFound)
def handle_not_found(err):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(err):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(IntegrityError)
def handle_integrity_error(err):
    db.session.rollback()
    return jsonify({"error": "Database integrity error"}), 409


@app.errorhandler(500)
def handle_server_error(err):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    