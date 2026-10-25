from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    ExerciseDetailsSchema,
    WorkoutSchema,
    ExerciseDetailsSchema,
    WorkoutDetailsSchema,
    WorkoutExerciseWithExerciseSchema,

)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    #sqlite ignores foreign keys unless told otherwise
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_app():
    app = Flask(__name__)

    exercise_schema = ExerciseSchema()
    exercises_schema = ExerciseSchema(many=True)
    exercise_detail_schema = WorkoutDetailsSchema()


    workout_schema = WorkoutSchema()
    workouts_schema = WorkoutSchema(many=True)
    workout_details_schema = WorkoutDetailsSchema()

    workout_exercise__detail_schema = WorkoutExerciseWithExerciseSchema()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    Migrate(app, db)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()

# Exercises
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


@app.route("/workouts", methods=["get"])
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


if __name__ == "__main__":
    app.run(port=5555, debug=True)

    