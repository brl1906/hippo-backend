from models.base_model import db
from models.contact_model import ContactSchema, ContactShortSchema
from models.opportunity_app_model import OpportunityApp, ApplicationStage
from models.resume_model import ResumeSnapshotSchema
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField
from sqlalchemy.ext.hybrid import hybrid_property
import enum


class OpportunityStage(enum.Enum):
    started = 0
    submitted = 1
    approved = 2
    posted = 3
    interviewing = 4
    filled = 5


class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    # table columns
    id = db.Column(db.String, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(2000), nullable=False)
    gdoc_id = db.Column(db.String(200))
    gdoc_link = db.Column(db.String(200), nullable=False)
    card_id = db.Column(db.String)
    program_name = db.Column(db.String)
    stage = db.Column(db.Integer, default=1)
    org_name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # relationships
    applications = db.relationship('OpportunityApp', back_populates='opportunity',
                                   cascade='all, delete, delete-orphan')
    program = db.relationship('Program', back_populates='opportunities')

    @hybrid_property
    def status(self):
        return OpportunityStage(self.stage)


class OpportunityAppSchema(Schema):
    id = fields.String(dump_only=True)
    contact = fields.Nested(ContactShortSchema, dump_only=True)
    # for info on why we use lambda here review this documentation:
    # https://marshmallow.readthedocs.io/en/stable/nesting.html#two-way-nesting
    opportunity = fields.Nested(
        lambda: OpportunitySchema(exclude=('applications',)))
    interest_statement = fields.String()
    status = EnumField(ApplicationStage, dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    resume = fields.Pluck(ResumeSnapshotSchema,
                          field_name='resume', allow_none=True)
    interview_date = fields.Date(allow_none=True)
    interview_time = fields.String(allow_none=True)
    interview_completed = fields.Boolean(dump_only=True)

    class Meta:
        unknown = EXCLUDE


class OpportunitySchema(Schema):
    id = fields.String(required=True, dump_only=True)
    title = fields.String(required=True)
    short_description = fields.String(required=True)
    gdoc_link = fields.String(required=True)
    status = EnumField(OpportunityStage, dump_only=True)
    org_name = fields.String(required=True)
    program_name = fields.String(allow_none=True)
    program_id = fields.Integer(allow_none=True)
    is_active = fields.Boolean(dump_only=True)
    applications = fields.Nested(OpportunityAppSchema(
        exclude=('opportunity', 'resume'), many=True))

    class Meta:
        unknown = EXCLUDE


class ProgramContactShortSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact = fields.Nested(ContactShortSchema, dump_only=True)
    program_id = fields.Integer(dump_only=True)
    is_approved = fields.Boolean(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    applications = fields.Nested(
        OpportunityAppSchema,
        exclude=['contact', 'interest_statement', 'resume'],
        many=True
    )

    class Meta:
        unknown = EXCLUDE
