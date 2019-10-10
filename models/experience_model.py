from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.achievement_model import Achievement, AchievementSchema
from sqlalchemy.ext.hybrid import hybrid_property
import datetime as dt
import math

class Type(enum.Enum):
    work = 'Work'
    service = 'Service'
    accomplishment = 'Accomplishment'
    education = 'Education'


class Degree(enum.Enum):
    high_school = 'High School'
    associates = 'Associates'
    undergraduate = 'Undergraduate'
    masters = 'Masters'
    doctoral = 'Doctoral'

class Month(enum.Enum):
    none = 'none'
    january = 'January'
    february = 'February'
    march = 'March'
    april = 'April'
    may = 'May'
    june = 'June'
    july = 'July'
    august = 'August'
    september = 'September'
    october = 'October'
    november = 'November'
    december = 'December'

class Experience(db.Model):
    __tablename__ = 'experience'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    host = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.Enum(Degree, name='Degree'))
    start_month = db.Column(db.Enum(Month, name='MonthType'))
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.Enum(Month, name='MonthType'))
    end_year = db.Column(db.Integer)
    type = db.Column(db.Enum(Type, name='ExperienceType'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    location_city = db.Column(db.String(100))
    location_state = db.Column(db.String(100))

    #relationships
    contact = db.relationship('Contact')
    achievements = db.relationship('Achievement', back_populates='experience',
                                   cascade='all, delete, delete-orphan')
    resumes = db.relationship('ResumeItem', back_populates='experience',
                              cascade='all, delete, delete-orphan')

    #calculated fields
    @hybrid_property
    def date_end(self):
        if self.end_month==Month.none and self.end_year==0:
            return dt.datetime.today()
        else:
            end_str = f'1 {self.end_month.value}, {self.end_year}'
            return dt.datetime.strptime(end_str, '%d %B, %Y')

    @hybrid_property
    def date_start(self):
        start_str = f'1 {self.start_month.value}, {self.start_year}'
        return dt.datetime.strptime(start_str, '%d %B, %Y')

    @hybrid_property
    def date_length(self):
        end = self.date_end
        start = self.date_start
        return (end.year - start.year) * 12 + end.month - start.month

    @hybrid_property
    def length_year(self):
        return math.floor(self.date_length/12)

    @hybrid_property
    def length_month(self):
        return self.date_length % 12

    @hybrid_property
    def is_current(self):
        if self.end_month==Month.none and self.end_year==0:
            return True
        else:
            return False


class ExperienceSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = EnumField(Degree, by_value=True, missing=None)
    is_current = fields.Boolean(dump_only=True)
    start_month = EnumField(Month, by_value=True, required=True)
    start_year = fields.Integer(required=True)
    end_month = EnumField(Month, by_value=True, missing=None)
    end_year = fields.Integer(allow_none=True)
    length_year = fields.Integer(dump_only=True)
    length_month = fields.Integer(dump_only=True)
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer(required=True)
    location_city = fields.String()
    location_state = fields.String()
    achievements = fields.Nested(AchievementSchema, many=True)
