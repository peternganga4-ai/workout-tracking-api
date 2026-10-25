from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.orm import validates


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

    #db-level constraints: enforced inside sqlite itself
    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0", name ="name_not_empty")
        CheckConstraint("length(trim(category)) > 0", name="category_not_empty"),

    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)


    #