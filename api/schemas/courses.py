from marshmallow import Schema, fields, validate


class CourseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    lectures_count = fields.Int()
    start_date = fields.Date('%m-%d-%Y')
    end_date = fields.Date('%m-%d-%Y')
