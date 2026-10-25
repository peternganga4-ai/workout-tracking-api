import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from datetime import date

from app import app

from models import db, Exercise, Workout, WorkoutExercise


def seed():
    with app.app_context():
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()


        pushups = Exercise(name="Push-ups", category="strength", equipment_needed=False)
        squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
        plank = Exercise(name="Plank", category="Core", equipment_needed=False)
        bench = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
        running = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
        db.session.add_all([pushups, squats, plank, bench, running])
        db.session.commit()


        #Workouts

        morning = Workout(date=date(2026, 1, 15), duration_minutes=45, notes="Morning session")
        evening = Workout(date=date(2026, 1, 16), duration_minutes=30, notes="Evening quick session")
        db.session.commit()


        #associations (reps/sets or duration seconds)

        associations = [
            WorkoutExercise(workout=morning, exercise=pushups, reps=15, sets=3),
            WorkoutExercise(workout=morning, exercise=plank, duration_seconds=60),
            WorkoutExercise(workout=morning, exercise=squats, reps=20, sets=4),
            # Push-ups reused in a second workout with different numbers:
            WorkoutExercise(workout=evening, exercise=pushups, reps=10, sets=5),
            WorkoutExercise(workout=evening, exercise=running, duration_seconds=1200),
        ]
        db.session.add_all(associations)
        db.session.commit()



        print("Seed complete:")
        print(f"  Exercises:        {Exercise.query.count()}")
        print(f"  Workouts:         {Workout.query.count()}")
        print(f"  WorkoutExercises: {WorkoutExercise.query.count()}")


if __name__ == "__main__":
    seed()
