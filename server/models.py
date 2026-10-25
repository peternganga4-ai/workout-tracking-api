from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.orm import validates

from datetime import date as date_type

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Exercise(db.Model):
    __tablename__ = "exercises"

    # Database-level constraints: enforced inside SQLite itself.
    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name="name_not_empty"),
        CheckConstraint("length(trim(category)) > 0", name="category_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Model-level validations: run in Python when attributes are set.
    @validates("name")
    def validate_name(self, key, value):
        if value is None or not value.strip():
            raise ValueError("Exercise name must not be empty.")
        if len(value) > 100:
            raise ValueError("Exercise name must be 100 characters or fewer.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value is None or not value.strip():
            raise ValueError("Exercise category must not be empty.")
        if len(value) > 50:
            raise ValueError("Exercise category must be 50 characters or fewer.")
        return value.strip()

    @validates("equipment_needed")
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("equipment_needed must be a boolean (true or false).")
        return value

    def __repr__(self):
        return f"<Exercise {self.id} {self.name}>"



class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="duration_positive"),

    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)


    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None:
            raise ValueError("duration_minutes is required.")
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("duration_minutes must be an integer.")
        if value <= 0:
            raise ValueError("duration_minutes must be positive.")
        return value


    @validates("date")
    def validate_date(self, key, value):
        if not isinstance(value, date_type):
            raise ValueError("date must be a valid date (YYYY-MM-DD).")
        return value
    def __repr__(self):
        return f"<Workout {self.id} {sel.date}>"
    