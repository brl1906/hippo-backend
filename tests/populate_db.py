import datetime as dt
# imports models related to the contact
from models.contact_model import (
    Contact,
)
from models.email_model import (
    Email,
    Type as EmailType,
)

# imports models related to experiences
from models.experience_model import (
    Experience,
    Degree,
    Type as ExpType,
    Month,
)
from models.achievement_model import Achievement

# imports models related to skills
from models.tag_model import (
    Tag,
    TagType,
    TagStatusType,
)
from models.tag_item_model import TagItem
from models.skill_model import (
    Skill,
    Capability,
    SkillRecommendation,
    CapabilitySkillSuggestion
)
from models.skill_item_model import ContactSkill
from resources.skill_utils import get_skill_id, make_skill

# imports models related to the resume
from models.resume_model import ResumeSnapshot

# imports models related to the program and cycle
from models.program_model import Program
from models.program_contact_model import ProgramContact
from models.program_app_model import ProgramApp
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp
from models.session_model import UserSession
from models.profile_model import (
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted
)

billy = Contact(
    id=123,
    first_name='Billy',
    last_name='Daly',
    email_primary=Email(
        id=45,
        is_primary=True,
        email='billy@example.com',
        type=EmailType.personal,
    ),
    email='billy@example.com',
    phone_primary='555-245-2351',
    account_id='test-valid|0123456789abcdefabcdefff',
    terms_agreement=True
)
obama = Contact(
    id=124,
    first_name='Barack',
    last_name='Obama',
    email='obama@whitehouse.gov',
    email_primary=Email(
        id=90,
        is_primary=True,
        email='obama@whitehouse.gov',
        type=EmailType('Work'),
    ),
    phone_primary='555-444-4444',
    terms_agreement=True

)

billy_profile = Profile(
    id=123,
    contact_id=123,
    gender='Male',
    gender_other=None,
    pronoun='He/Him/His',
    pronoun_other=None,
    years_exp='3-5',
    job_search_status='Actively looking',
    current_job_status='Employed',
    current_edu_status='Full-time Student',
    previous_bcorps_program='Yes',
    needs_help_programs=True,
    hear_about_us='Facebook',
    hear_about_us_other='Other',
    value_question1='Test response',
    value_question2='Test response',
)

billy_address = ContactAddress(
    id=123,
    contact_id=123,
    profile_id=123,
    street1='123 Main St',
    street2='Apt 3',
    city='Baltimore',
    state='Maryland',
    zip_code='21218',
    country='United States',
)

billy_race = Race(
    id=123,
    contact_id=123,
    profile_id=123,
    american_indian=False,
    asian=False,
    black=False,
    hispanic=False,
    hawaiian=False,
    south_asian=False,
    white=True,
    not_listed=False,
    race_other=None,
)

billy_roles = RoleChoice(
    id=123,
    profile_id=123,
    advocacy_public_policy=True,
    community_engagement_outreach=True,
    data_analysis=True,
    fundraising_development=False,
    program_management=False,
    marketing_public_relations=False
)

billy_programs_completed = ProgramsCompleted(
    id=123,
    profile_id=123,
    mayoral_fellowship=True,
    fellowship=False,
    kiva=False,
    public_allies=False,
    civic_innovators=False,
    elevation_awards=False
)

billy_session = UserSession(
    id=123,
    auth_id='test-valid|0123456789abcdefabcdefff',
    contact_id=123,
    jwt='test_jwt',
    expiration=dt.datetime.utcnow(),
)

exp_columbia = Experience(
    id=511,
    host='Columbia University',
    title='Political Science',
    description='Test description',
    link='www.google.com',
    link_name="Google",
    start_month=Month('September'),
    start_year=1979,
    end_month=Month('May'),
    end_year=1983,
    type=ExpType('Accomplishment'),
    location='New York, NY, USA',
    contact_id=124,
)


exp_goucher = Experience(
    id=512,
    host='Goucher College',
    title='Economics',
    degree='Undergraduate',
    degree_other='Study Abroad',
    start_month=Month('September'),
    start_year=2012,
    end_month=Month('May'),
    end_year=2016,
    type=ExpType('Education'),
    location='Towson, MD, USA',
    contact_id=123,
)

exp_baltimore = Experience(
    id=513,
    host='Baltimore Corps',
    description='Test description here',
    title='Systems Design Manager',
    start_month=Month('January'),
    start_year=2000,
    end_month='none',
    end_year=0,
    type=ExpType('Work'),
    location='Baltimore, MD, USA',
    contact_id=123,
)

a_baltimore1 = Achievement(
    id=81,
    exp_id=513,
    contact_id=123,
    description='Redesigned the Salesforce architecture to facilitate easier reporting.'
)
a_baltimore2 = Achievement(
    id=82,
    exp_id=513,
    contact_id=123,
    description='Formalized organizational strategy for defining and analyzing KPIs.'
)
a_baltimore3 = Achievement(
    id=83,
    exp_id=513,
    contact_id=123,
    description='Developed recruitment projection tools to model and track progress to goals.'
)
a_goucher1 = Achievement(
    id=84,
    exp_id=512,
    contact_id=123,
    description='Did some stuff'
)


skills = [
    Skill(
        id=get_skill_id(name),
        name=name,
    )
    for name in [
        'Python',
        'C++',
        'Web Development',
        'Public Health',
        'Advocacy and Public Policy',
        'Community Organizing',
        'Canvassing',
        'Advocacy',
        'Policy Writing',
        'Volunteer Mobilization',
        'Community Engagement and Outreach',
        'Community Engagement',
        'Client Recruitment',
        'Partnership Building',
        'Event Planning',
        'Information Technology',
        'Flask',
    ]
]

advocacy_capability = Capability(
    id='cap:advocacy',
    name='Advocacy and Public Policy',
)
advocacy_recommendations = [
    SkillRecommendation(
        capability_id='cap:advocacy',
        skill_id=get_skill_id(name),
        order=i
    )
    for (i, name) in enumerate([
        'Community Organizing',
        'Canvassing',
        'Advocacy',
        'Policy Writing',
        'Volunteer Mobilization',
    ])
]
outreach_capability = Capability(
    id='cap:outreach',
    name='Community Engagement and Outreach',
)
outreach_recommendations = [
    SkillRecommendation(
        capability_id='cap:outreach',
        skill_id=get_skill_id(name),
        order=i
    )
    for (i, name) in enumerate([
        'Community Engagement',
        'Client Recruitment',
        'Partnership Building',
        'Event Planning',
        'Community Organizing',
    ])
]
it_capability = Capability(
    id='cap:it',
    name='Information Technology',
)

billy_flask_suggestion = CapabilitySkillSuggestion(
    contact_id=123,
    capability_id='cap:it',
    skill_id='QUEVjv1tcq6uLmzCku6ikg=='
)

program_pfp = Program(
    id=1,
    name='Place for Purpose',
    trello_board_id='5e37744114d9d01a03ddbcfe',
)

program_mayoral = Program(
    id=2,
    name='Mayoral Fellowship',
    trello_board_id='5e37744114d9d01a03ddbcfe',
)


billy_pfp = ProgramContact(
    id=5,
    program_id=1,
    contact_id=123,
    card_id='5e4af2d6fc3c0954ff187ddc',
    stage=1,
    is_approved=True
)

billy_mayoral = ProgramContact(
    id=7,
    program_id=2,
    contact_id=123,
    card_id='card',
    stage=1,
    is_approved=False
)

billy_pfp_app = ProgramApp(
    id=7,
    contact_id=123,
    program_id=1,
    is_interested=True,
    is_approved=True,
    decision_date='2020-01-01'
)

billy_mayoral_app = ProgramApp(
    id=8,
    contact_id=123,
    program_id=2,
)

obama_pfp = ProgramContact(
    id=6,
    program_id=1,
    contact_id=124,
    card_id='card',
    stage=1,
)

test_opp1 = Opportunity(
    id='123abc',
    title="Test Opportunity",
    short_description="This is a test opportunity.",
    gdoc_id="ABC123xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=1,
    program_name="Place for Purpose"
)

test_opp2 = Opportunity(
    id='222abc',
    title="Another Test Opportunity",
    short_description="This is another test opportunity.",
    gdoc_id="BBB222xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=2,
    program_name="Mayoral Fellowship"
)

test_opp3 = Opportunity(
    id='333abc',
    title="A Third Test Opportunity",
    short_description="This is another test opportunity.",
    gdoc_id="CCC333xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=1,
    program_name="Place for Purpose"
)

snapshot1 = ResumeSnapshot(
    id=1111,
    resume='{"test":"snapshot1"}',
)

app_billy = OpportunityApp(
    id='a1',
    contact_id=123,
    opportunity_id='123abc',
    interest_statement="I'm interested in this test opportunity",
    stage=1,
    resume_id=1111,
)

app_billy2 = OpportunityApp(
    id='a2',
    contact_id=123,
    opportunity_id='222abc',
    interest_statement="I'm also interested in this test opportunity",
    stage=0,
)

app_obama = OpportunityApp(
    id='a3',
    contact_id=124,
    opportunity_id='123abc',
    interest_statement="I'm also interested in this test opportunity",
    stage=2,
)


def get_skill(name):
    return Skill.query.get(get_skill_id(name))


def get_contact_skill(contact_id, skill_name):
    return ContactSkill.query.filter_by(
        contact_id=contact_id, skill_id=get_skill_id(skill_name)).first()


def populate(db):
    for skill in skills:
        db.session.add(skill)
    db.session.commit()

    db.session.add(billy)
    db.session.add(obama)
    db.session.add(billy_profile)
    db.session.add(billy_race)
    db.session.add(billy_address)
    db.session.add(billy_roles)
    db.session.add(billy_programs_completed)
    db.session.add(billy_session)
    db.session.add(exp_columbia)
    db.session.add(exp_goucher)
    db.session.add(exp_baltimore)
    db.session.add(a_goucher1)
    db.session.add(a_baltimore1)
    db.session.add(a_baltimore2)
    db.session.add(a_baltimore3)
    db.session.add(program_pfp)
    db.session.add(program_mayoral)
    db.session.add(billy_pfp)
    db.session.add(billy_mayoral)
    db.session.add(billy_pfp_app)
    db.session.add(billy_mayoral_app)
    db.session.add(obama_pfp)
    db.session.add(test_opp1)
    db.session.add(test_opp2)
    db.session.add(test_opp3)
    db.session.add(snapshot1)
    db.session.add(app_billy)
    db.session.add(app_billy2)
    db.session.add(app_obama)

    db.session.commit()

    billy.add_skill(get_skill('Public Health'))
    billy.add_skill(get_skill('Community Organizing'))
    obama.add_skill(get_skill('Public Health'))

    exp_baltimore.add_skill(get_skill('Python'))
    exp_baltimore.add_skill(get_skill('Web Development'))
    a_baltimore1.add_skill(get_skill('Flask'), it_capability)
    a_baltimore2.add_skill(
        get_skill('Community Organizing'), advocacy_capability)
    a_baltimore3.add_skill(get_skill('Web Development'), it_capability)
    a_goucher1.add_skill(get_skill('Python'), it_capability)

    billy.add_skill(get_skill('Flask'))
    db.session.add(billy_flask_suggestion)

    # Test deleted skills as well
    billy.add_skill(get_skill('Event Planning'))
    outreach_capability.related_skills.append(get_skill('Event Planning'))
    a_baltimore2.add_skill(get_skill('Event Planning'))
    billy_eventplan = get_contact_skill(123, 'Event Planning')
    billy_eventplan.deleted = True

    advocacy_capability.related_skills.append(
        get_skill('Community Organizing'))
    outreach_capability.related_skills.append(
        get_skill('Community Organizing'))
    it_capability.related_skills.append(get_skill('Python'))
    it_capability.related_skills.append(get_skill('C++'))
    it_capability.related_skills.append(get_skill('Web Development'))

    db.session.add(advocacy_capability)
    for rec in advocacy_recommendations:
        db.session.add(rec)
    db.session.add(outreach_capability)
    for rec in outreach_recommendations:
        db.session.add(rec)
    db.session.add(it_capability)

    db.session.commit()
