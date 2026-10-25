from marshamallow import Schema, fields, validate, validates, validationError, EXCLUDE

class ExerciseSchema(Schema):
    class Meta:
        unknown = EXCLUDE #ignore unexpected keys instead of erroring

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)


    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Exercise name must not be empty or whitespace.")


class WorkoutSchema(Schema):
    class Meta:
        unknown = EXCLUDE


    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))



#detail schemas: serialize relationship without recursion


