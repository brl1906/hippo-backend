import enum
from models.base_model import db
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField
from models.contact_model import ContactSchema
from models.opportunity_model import OpportunitySchema

class ApplicationStage(enum.Enum):
    draft = 0
    submitted = 1

class OpportunityApp(db.Model):
    __tablename__ = 'opportunity_app'

    #table columns
    id = db.Column(db.String, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    opportunity_id = db.Column(db.String, db.ForeignKey('opportunity.id'), nullable=False)
    interest_statement = db.Column(db.String(2000), nullable=True)
    stage = db.Column(db.Integer, nullable=False, default=0)

    contact = db.relationship('Contact', back_populates='applications')

    opportunity = db.relationship('Opportunity')

    #calculated fields
    @hybrid_property
    def status(self):
        return ApplicationStage(self.stage)

    __table_args__ = (
        db.Index('oppapp_contact_opportunity', 
                 'contact_id', 'opportunity_id', unique=True),
    )


class OpportunityAppSchema(Schema):
    id = fields.String(dump_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    opportunity = fields.Nested(OpportunitySchema, dump_only=True)
    interest_statement = fields.String()
    status = EnumField(ApplicationStage, dump_only=True)

    class Meta:
        unknown = EXCLUDE


