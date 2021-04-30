from marshmallow import Schema, fields, validate


class CourseSchema(Schema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            error='Course name must be at least 2 symbols long.'
        )
    )
    lectures_count = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            error="Value must be greater than 0"
        )
    )
    start_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    end_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )


class IdSchema(Schema):
    id = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            error="Value must be greater than 0"
        )
    )


class CourseFilterSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            error='Course name must be at least 1 symbols long.'
        )
    )
    start_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
    end_date = fields.Date(
        required=True,
        format='%Y-%m-%d'
    )
