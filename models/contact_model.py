from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE, pre_dump, post_dump
from marshmallow_enum import EnumField
from models.experience_model import Experience, ExperienceSchema, Type
from models.email_model import Email, EmailSchema
from models.achievement_model import Achievement
from models.skill_model import Skill, SkillSchema
from models.skill_item_model import ContactSkill
from models.program_contact_model import ProgramContactSchema
from models.program_app_model import ProgramAppSchema
from models.profile_model import ProfileSchema, ContactAddress
from sqlalchemy.ext.hybrid import hybrid_property

UPDATE_FIELDS = ['first_name', 'last_name', 'email', 'phone_primary', 'stage']

def add_skill_error(_):
    assert False, "use contact.add_skill instead of contact.skills.append"

class Contact(db.Model):
    __tablename__ = 'contact'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String)
    phone_primary = db.Column(db.String(25))
    account_id = db.Column(db.String(255), nullable=True)
    terms_agreement =db.Column(db.Boolean, default=False)
    stage = db.Column(db.Integer, default=1)

    #relationships
    emails = db.relationship('Email',
                             back_populates='contact',
                             cascade='all, delete, delete-orphan')
    email_primary = db.relationship("Email",
                                    primaryjoin=db.and_(
                                    id == Email.contact_id,
                                    Email.is_primary == True),
                                    uselist=False)
    addresses = db.relationship('ContactAddress',
                                back_populates='contact')
    address_primary = db.relationship('ContactAddress',
                                      primaryjoin=db.and_(
                                      id == ContactAddress.contact_id,
                                      ContactAddress.is_primary == True),
                                      back_populates='contact',
                                      uselist=False)
    achievements = db.relationship('Achievement',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    skill_items = db.relationship('ContactSkill',
                                  cascade='all, delete, delete-orphan')
    capability_skill_suggestions = db.relationship(
        'CapabilitySkillSuggestion',
        cascade='all, delete, delete-orphan'
    )
    experiences = db.relationship('Experience',
                                  back_populates='contact',
                                  cascade='all, delete, delete-orphan')
    programs = db.relationship('ProgramContact',
                               back_populates='contact',
                               cascade='all, delete, delete-orphan')
    program_apps = db.relationship('ProgramApp',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    applications = db.relationship('OpportunityApp',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    sessions = db.relationship('UserSession',
                               cascade='all, delete, delete-orphan')
    profile = db.relationship('Profile',
                              back_populates='contact',
                              uselist=False,
                              cascade='all, delete, delete-orphan')
    race = db.relationship('Race',
                           back_populates='contact',
                           cascade='all, delete, delete-orphan',
                           uselist=False)

    def add_skill(self, skill):
        contact_skill = (ContactSkill.query
                                .filter_by(contact_id=self.id,
                                           skill_id=skill.id)
                                .first())
        if contact_skill:
            contact_skill.deleted = False
        else:
            contact_skill = ContactSkill(skill, self)
            self.skill_items.append(contact_skill)
        return contact_skill

    @hybrid_property
    def skills(self):
        skills = []
        for skill_item in self.skill_items:
            if not skill_item.deleted:
                skills.append(skill_item.skill)
        return sorted(skills, key=lambda skill: skill.name)

    @hybrid_property
    def email_main(self):
        if not self.email:
            return self.email_primary.email
        else:
            return self.email

    def query_program_contact(self, program_id):
        return next((p for p in self.programs
                     if p.program_id == program_id), None)

    def update(self, **update_dict):
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Nested(EmailSchema)
    email = fields.String()
    phone_primary = fields.String()
    account_id = fields.String()
    skills = fields.Nested(SkillSchema, many=True)
    terms_agreement = fields.Boolean()
    programs = fields.Nested(ProgramContactSchema, many=True, dump_only=True)
    program_apps = fields.Nested(ProgramAppSchema, many=True)
    profile = fields.Nested(ProfileSchema)

    class Meta:
        unknown = EXCLUDE

class ContactShortSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email_main = fields.String(dump_only=True, data_key='email')

    class Meta:
        unknown = EXCLUDE

class ContactProgramSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email_main = fields.String(dump_only=True, data_key='email')
    programs = fields.Nested(ProgramContactSchema, many=True, dump_only=True)

    class Meta:
        unknown = EXCLUDE
