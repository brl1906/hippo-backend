import json
import datetime as dt
from pprint import pprint
import pytest
import math
import copy

from models.base_model import db
from models.contact_model import Contact
from models.experience_model import Experience, Month
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.program_contact_model import ProgramContact
from models.session_model import UserSession
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp, ApplicationStage
from models.profile_model import Profile

from models.skill_model import (
    CapabilitySkillSuggestion
)
from models.skill_item_model import (
    ContactSkill,
    ExperienceSkill,
    AchievementSkill,
)

from flask import g

SKILLS = {
    'billy': [
        {
            'id': '74BgThI2os9wEdyArofEKA==',
            'name': 'Community Organizing',
        },
        {
            'id': 'QUEVjv1tcq6uLmzCku6ikg==',
            'name': 'Flask',
        },
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
        },
        {
            'id': '4R9tqGuK2672PavRTJrN_A==',
            'name': 'Python',
        },
        {
            'id': 'hbBWJS6x6gDxGMUC5HAOYg==',
            'name': 'Web Development',
        },
    ],
    'obama': [
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
        },
    ],
}

CAPABILITIES = {
    'billy': {
        'contact_id': 123,
        'capabilities': [
            {
                'id': 'cap:it',
                'name': 'Information Technology',
                'score': 2,
                'skills': [
                    {'id': '4R9tqGuK2672PavRTJrN_A==', 'name': 'Python'},
                    {'id': 'hbBWJS6x6gDxGMUC5HAOYg==', 'name': 'Web Development'}
                ],
                'suggested_skills': [
                    {'id': 'QUEVjv1tcq6uLmzCku6ikg==', 'name': 'Flask'}
                ]
            },
            {
                'id': 'cap:advocacy',
                'name': 'Advocacy and Public Policy',
                'score': 1,
                'skills': [
                    {'id': '74BgThI2os9wEdyArofEKA==', 'name': 'Community Organizing'}
                ],
                'suggested_skills': []
            },
            {
                'id': 'cap:outreach',
                'name': 'Community Engagement and Outreach',
                'score': 0,
                'skills': [
                    {'id': '74BgThI2os9wEdyArofEKA==', 'name': 'Community Organizing'}
                ],
                'suggested_skills': []
            }
        ],
        'other_skills': [
            { 'id': 'n1N02ypni69EZg0SggRIIg==', 'name': 'Public Health'}
        ]
    }
}


PROGRAMS = {
    'pfp': {
        'id': 1,
        'name': 'Place for Purpose'
    },
    'mayoral': {
        'id': 2,
        'name': 'Mayoral Fellowship'
    }
}

PROGRAM_CONTACTS = {
    'billy_pfp': {
        'id': 5,
        'contact_id': 123,
        'program': PROGRAMS['pfp'],
        'card_id': '5e4af2d6fc3c0954ff187ddc',
        'stage': 1,
        'is_active': True,
        'is_approved': True,
    },
    'obama_pfp': {
        'id': 6,
        'contact_id': 124,
        'program': PROGRAMS['pfp'],
        'card_id': 'card',
        'stage': 1,
        'is_active': True,
        'is_approved': False,
    },
    'billy_mayoral': {
        'id': 7,
        'contact_id': 123,
        'program': PROGRAMS['mayoral'],
        'card_id': 'card',
        'stage': 1,
        'is_active': True,
        'is_approved': False,
    }
}

PROGRAM_APPS = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy@example.com",
        'program_apps': [
            {'id': 7,
             'program': {'id': 1, 'name': 'Place for Purpose'},
             'is_interested': True,
             'is_approved': True,
             'decision_date': '2020-01-01',
             'status': 'Eligible'},
            {'id': 8,
             'program': {'id': 2, 'name': 'Mayoral Fellowship'},
             'is_interested': False,
             'is_approved': False,
             'status': 'Not interested',
             'decision_date': None},
        ]},
    'obama_put': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
        'program_apps': [
            {'program': {'id': 1, 'name': 'Place for Purpose'},
             'is_interested': True},
            {'program': {'id': 2, 'name': 'Mayoral Fellowship'},
             'is_interested': False},
        ]},
    'obama_get': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
        'program_apps': [
            {'id': 1,
             'program': {'id': 1, 'name': 'Place for Purpose'},
             'is_interested': True,
             'is_approved': False,
             'decision_date': None,
             'status': 'Waiting for approval'},
            {'id': 2,
             'program': {'id': 2, 'name': 'Mayoral Fellowship'},
             'is_interested': False,
             'is_approved': False,
             'status': 'Not interested',
             'decision_date': None},
    ]}
}

CONTACT_PROFILE = {
    'billy_profile': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy@example.com",
        'phone_primary': "555-245-2351",
        'profile': {
            'id': 123,
            'gender': 'Male',
            'gender_other': None,
            'pronoun': 'He/Him/His',
            'pronoun_other': None,
            'years_exp': '3-5',
            'job_search_status': 'Actively looking',
            'current_job_status': 'Employed',
            'current_edu_status': 'Full-time Student',
            'previous_bcorps_program': 'Yes',
            'value_question1': 'Test response',
            'value_question2': 'Test response',
            'needs_help_programs': True,
            'hear_about_us': 'Facebook',
            'hear_about_us_other': 'Other',
            'programs_completed': {
                'fellowship': False,
                'public_allies': False,
                'mayoral_fellowship': True,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False
            },
            'address_primary': {
                'street1': '123 Main St',
                'street2': 'Apt 3',
                'city': 'Baltimore',
                'state': 'Maryland',
                'zip_code': '21218',
                'country': 'United States',
             },
            'race': {
                'american_indian': False,
                'asian': False,
                'black': False,
                'hispanic': False,
                'hawaiian': False,
                'south_asian': False,
                'white': True,
                'not_listed': False,
                'race_other': None,
            },
            'roles': {
                'advocacy_public_policy': True,
                'community_engagement_outreach': True,
                'data_analysis': True,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        }
    },
    'billy_update': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy_new@email.com", # updated
        'phone_primary': "555-245-2351",
        'profile': {
            'id': 1,
            'gender': 'Male',
            'gender_other': None,
            'pronoun': 'He/Him/His',
            'pronoun_other': None,
            'years_exp': '3-5',
            'job_search_status': 'Actively looking',
            'current_job_status': 'Employed',
            'current_edu_status': 'Full-time Student',
            'previous_bcorps_program': 'Yes',
            'value_question1': 'Test response',
            'value_question2': 'Test response',
            'needs_help_programs': True,
            'hear_about_us': 'Facebook',
            'hear_about_us_other': 'Other New',
            'programs_completed': {
                'fellowship': False,
                'public_allies': False,
                'mayoral_fellowship': False,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False
            },
            'address_primary': {
                'street1': '124 Main St', # updated
                'street2': 'Apt 3',
                'city': 'Baltimore',
                'state': 'Maryland',
                'zip_code': '21218',
                'country': 'United States',
             },
            'race': {
                'american_indian': False,
                'asian': False,
                'black': False,
                'hispanic': True, # updated
                'hawaiian': False,
                'south_asian': False,
                'white': True,
                'not_listed': False,
                'race_other': None,
            },
            'roles': {
                'advocacy_public_policy': True,
                'community_engagement_outreach': True,
                'data_analysis': False,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        }
    },
    'obama_blank': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
        'phone_primary': "555-444-4444",
        'profile': {
            'id': 1,
            'gender': None,
            'gender_other': None,
            'pronoun': None,
            'pronoun_other': None,
            'years_exp': None,
            'job_search_status': None,
            'current_job_status': None,
            'current_edu_status': None,
            'previous_bcorps_program': None,
            'value_question1': None,
            'value_question2': None,
            'hear_about_us': None,
            'hear_about_us_other': None,
            'needs_help_programs': None,
            'programs_completed': {
                'fellowship': False,
                'public_allies': False,
                'mayoral_fellowship': False,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False,
            },
            'address_primary': {
                'street1': None,
                'street2': None,
                'city': None,
                'state': None,
                'zip_code': None,
                'country': None,
             },
            'race': {
                'american_indian': False,
                'asian': False,
                'black': False,
                'hispanic': False,
                'hawaiian': False,
                'south_asian': False,
                'white': False,
                'not_listed': False,
                'race_other': None,
            },
            'roles': {
                'advocacy_public_policy': False,
                'community_engagement_outreach': False,
                'data_analysis': False,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        }
    },
    'billy_null': {
        'email': 'billy@example.com',
        'first_name': 'Billy',
        'last_name': 'Daly',
        'id': 123,
        'profile': {
            'address_primary': {
                'city': 'Baltimore',
                'country': 'United States',
                'state': 'Maryland',
                'street1': '123 Main St.',
                'street2': 'Apt 3',
                'zip_code': '21111',
            },
            'current_edu_status': 'Full-time student',
            'current_job_status': 'Unemployed',
            'gender': 'Not Listed',
            'gender_other': 'sads',
            'hear_about_us': None,
            'hear_about_us_other': None,
            'id': 1,
            'job_search_status': 'Looking for a job in the next 2-6 months',
            'needs_help_programs': None,
            'previous_bcorps_program': 'No',
            'programs_completed': None,
            'pronoun': 'They/Them/Their',
            'pronoun_other': None,
            'value_question1': 'sasdsad',
            'value_question2': 'asdsdasd',
            'years_exp': '5+ years',
            'race': {
                'american_indian': False,
                'asian': True,
                'black': False,
                'hawaiian': False,
                'hispanic': False,
                'not_listed': False,
                'race_other': None,
                'south_asian': False,
                'white': True,
            },
            'roles': {
                'advocacy_public_policy': False,
                'community_engagement_outreach': None,
                'data_analysis': True,
                'fundraising_development': False,
                'marketing_public_relations': False,
                'program_management': True,
            },
        },
    }
}

OPPORTUNITIES = {
    'test_opp1': {
        'id': '123abc',
        'title': "Test Opportunity",
        'short_description': "This is a test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose"
    },
    'test_opp2': {
        'id': '222abc',
        'title': "Another Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 2,
        'is_active': True,
        'program_name': "Mayoral Fellowship"
    },
    'test_opp3': {
        'id': '333abc',
        'title': "A Third Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose"
    },

}


CONTACTS = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email_primary': {
            'id': 45,
            'is_primary': True,
            'email': "billy@example.com",
            'type': "Personal",
        },
        'phone_primary': "555-245-2351",
        'account_id': 'test-valid|0123456789abcdefabcdefff',
        'skills': SKILLS['billy'],
        'programs': [PROGRAM_CONTACTS['billy_pfp'],
                     PROGRAM_CONTACTS['billy_mayoral']],
        'program_apps': PROGRAM_APPS['billy']['program_apps'],
        'terms_agreement': True,
        'profile': CONTACT_PROFILE['billy_profile']['profile']
    },

    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email_primary': {
            'id': 90,
            'is_primary': True,
            'email': "obama@whitehouse.gov",
            'type': "Work",
        },
        'phone_primary': "555-444-4444",
        'account_id': None,
        'skills': SKILLS['obama'],
        'programs': [PROGRAM_CONTACTS['obama_pfp']],
        'program_apps': [],
        'terms_agreement': True,
        'profile': None
    },
    'billy_bug': {
        "program_apps":[],
        "account_id":"google-oauth2|107132552139022184223",
        "email_primary":{
            "email":"billy@baltimorecorps.org",
            "id":123,
            "type":"Personal",
            "is_primary":True},
        "first_name":"Billy",
        "profile":{
            "pronoun_other":None,
            "needs_help_programs":None,
            "pronoun":None,
            "previous_bcorps_program":"No",
            "job_search_status":"Looking for a job in the next 2-6 months",
            "hear_about_us":None,
            "years_exp":"0-2 years",
            "current_job_status":"Unemployed",
            "gender":None,
            "gender_other":None,
            "roles":{
                "community_engagement_outreach":None,
                "advocacy_public_policy":None,
                "data_analysis":True,
                "marketing_public_relations":True,
                "fundraising_development":None,
                "program_management":None},
                "address_primary":{
                    "zip_code":None,
                    "country":None,
                    "city":None,
                    "state":None,
                    "street1":None,
                    "street2":None
                },
                "current_edu_status":"Full-time student",
                "value_question2":None,
                "id":6,
                "value_question1":None,
                "race":{
                    "asian":None,
                    "american_indian":None,
                    "white":None,
                    "black":None,
                    "race_other":None,
                    "hawaiian":None,
                    "hispanic":None,
                    "south_asian":None,
                    "not_listed":None
                },
                "programs_completed":{
                    "public_allies":False,
                    "civic_innovators":False,
                    "kiva":False,
                    "elevation_awards":False,
                    "mayoral_fellowship":False,
                    "fellowship":False
                },
                "hear_about_us_other":None
            },
            "phone_primary":"+1 (908) 578-4622",
            "programs":[
                {"is_approved":True,
                "contact_id":74,
                "is_active":True,
                "program":{"id":1,"name":"Place for Purpose"},
                "stage":None,
                "card_id":None,
                "id":74}
            ],
            "id":74,
            "last_name":"Daly1",
            "skills":[
                {"id":"FsleYWdpSaCA_qO3nkdMVw==","name":"Budgeting"},
                {"id":"YtCEwpoJ8IcV5KPCU7BURg==","name":"Data Visualization"},
                {"id":"qXGYjA77UThj7WPKlvxBtg==","name":"Documentation"},
                {"id":"RMjj5QJ3seZnbRPDmDg8pQ==","name":"Grant Reporting"},
                {"id":"oVUnhdEA5BJ_DLg0G4d1bw==","name":"Graphic Design"},
                {"id":"opfNJLiUftLHJH0cjBMMNg==","name":"Project Planning"},
                {"id":"8Z8qGXdVMDR2Q7OH3lkueA==","name":"Public Relations"},
                {"id":"ZFXHeJ5WsDwZSsQl_ge0MQ==","name":"Python Script"},
                {"id":"BPxYULhlGt-9tzxHsJNLSA==","name":"Report Writing"},
                {"id":"BU7_v3jWFFgHpmHcw50xqg==","name":"Social Media Management"},
                {"id":"8t48rV-NkxP0h0Y0E8h-vQ==","name":"Technical Requirements"}
            ],
            "terms_agreement":True,
            "capabilities":{
                "cap:analysis":{
                    "id":"cap:analysis",
                    "name":"Data Analysis",
                    "skills":[{"id":"YtCEwpoJ8IcV5KPCU7BURg==","name":"Data Visualization"}],
                    "suggested_skills":[],
                    "score":1
                },
                "cap:fundraising":{
                    "id":"cap:fundraising",
                    "name":"Fundraising and Development",
                    "skills":[],
                    "suggested_skills":[{"id":"RMjj5QJ3seZnbRPDmDg8pQ==","name":"Grant Reporting"}],
                    "score":0
                },
                "cap:marketing":{
                    "id":"cap:marketing",
                    "name":"Marketing and Public Relations",
                    "skills":[
                        {"id":"8Z8qGXdVMDR2Q7OH3lkueA==","name":"Public Relations"},
                        {"id":"BU7_v3jWFFgHpmHcw50xqg==","name":"Social Media Management"}],
                    "suggested_skills":[{"id":"oVUnhdEA5BJ_DLg0G4d1bw==","name":"Graphic Design"}],"score":2},
                    "cap:prog_mgmt":{
                        "id":"cap:prog_mgmt",
                        "name":"Program Management",
                        "skills":[{"id":"FsleYWdpSaCA_qO3nkdMVw==","name":"Budgeting"}],
                    "suggested_skills":[],
                    "score":2
                    }
                },
                "other_skills":[{"id":"qXGYjA77UThj7WPKlvxBtg==","name":"Documentation"},{"id":"opfNJLiUftLHJH0cjBMMNg==","name":"Project Planning"},{"id":"ZFXHeJ5WsDwZSsQl_ge0MQ==","name":"Python Script"},{"id":"BPxYULhlGt-9tzxHsJNLSA==","name":"Report Writing"},{"id":"8t48rV-NkxP0h0Y0E8h-vQ==","name":"Technical Requirements"}],"email":"billy@baltimorecorps.org"}
}

CONTACTS_SHORT = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy@example.com",
    },
    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
    }
}

SNAPSHOTS = {
    'snapshot1': {
        'test': 'snapshot1'
    },
    'snapshot2': {
        'test': 'snapshot2'
    },
}

APPLICATIONS_INTERNAL = {
    'billy_pfp': {
        'id': 5,
        'is_approved': True,
        'is_active': True,
        'program_id': 1,
        'contact': CONTACTS_SHORT['billy'],
        'applications': [{
            'id': 'a1',
            'status': 'submitted',
            'is_active': True,
            'opportunity': OPPORTUNITIES['test_opp1'],
            'interview_date': None,
            'interview_time': None,
            'interview_completed': False
        }]
    },
    'obama_pfp': {
        'contact': CONTACTS_SHORT['obama'],
        'id': 6,
        'is_active': True,
        'is_approved': False,
        'program_id': 1,
        'applications': [{
            'id': 'a3',
            'status': 'recommended',
            'is_active': True,
            'opportunity': OPPORTUNITIES['test_opp1'],
            'interview_date': None,
            'interview_time': None,
            'interview_completed': False
        }]
    },
    'billy_mayoral': {
        'id': 7,
        'is_approved': True,
        'is_active': True,
        'program_id': 2,
        'contact': CONTACTS_SHORT['billy'],
        'applications': [{
            'id': 'a2',
            'status': 'draft',
            'is_active': True,
            'opportunity': OPPORTUNITIES['test_opp2'],
            'interview_date': None,
            'interview_time': None,
            'interview_completed': False
        }]
    },
}

CONTACT_PROGRAMS = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy@example.com",
        'programs': [
            PROGRAM_CONTACTS['billy_pfp'],
            PROGRAM_CONTACTS['billy_mayoral']
        ]
    },
    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
        'programs': [PROGRAM_CONTACTS['obama_pfp']]
    }
}

OPPORTUNITIES_INTERNAL = {
    'test_opp1': {
        'id': '123abc',
        'title': "Test Opportunity",
        'short_description': "This is a test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose",
        'applications': [{'id': 'a1',
                          'contact': CONTACTS_SHORT['billy'],
                          'interest_statement': "I'm interested in this test opportunity",
                          'status': 'submitted',
                          'is_active': True,
                          'interview_date': None,
                          'interview_time': None,
                          'interview_completed': False},
                         {'id': 'a3',
                          'contact': CONTACTS_SHORT['obama'],
                          'interest_statement': "I'm also interested in this test opportunity",
                          'status': 'recommended',
                          'is_active': True,
                          'interview_date': None,
                          'interview_time': None,
                          'interview_completed': False}]
    },
    'test_opp2': {
        'id': '222abc',
        'title': "Another Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 2,
        'is_active': True,
        'program_name': "Mayoral Fellowship",
        'applications': [{'id': 'a2',
                          'contact': CONTACTS_SHORT['billy'],
                          'interest_statement': "I'm also interested in this test opportunity",
                          'status': 'draft',
                          'is_active': True,
                          'interview_date': None,
                          'interview_time': None,
                          'interview_completed': False}]
    },
    'test_opp3': {
        'id': '333abc',
        'title': "A Third Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose",
        'applications': []
    },
}

APPLICATIONS = {
    'app_billy': {
        'id': 'a1',
        'contact': CONTACTS_SHORT['billy'],
        'opportunity': OPPORTUNITIES['test_opp1'],
        'interest_statement': "I'm interested in this test opportunity",
        'status': 'submitted',
        'resume': SNAPSHOTS['snapshot1'],
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
        'interview_completed': False
    },
    'app_billy2': {
        'id': 'a2',
        'contact': CONTACTS_SHORT['billy'],
        'opportunity': OPPORTUNITIES['test_opp2'],
        'interest_statement': "I'm also interested in this test opportunity",
        'status': 'draft',
        'resume': None,
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
        'interview_completed': False,
    },

}


ACHIEVEMENTS = {
    'baltimore1': {
        'id': 81,
        'description': 'Redesigned the Salesforce architecture to facilitate easier reporting.',
        'skills': [{
            'name': 'Flask', 'capability_id': 'cap:it',
        }],
    },
    'baltimore2': {
        'id': 82,
        'description': 'Formalized organizational strategy for defining and analyzing KPIs.',
        'skills': [{
            'name': 'Community Organizing', 'capability_id': 'cap:advocacy',
        }],
    },
    'baltimore3': {
        'id': 83,
        'description': 'Developed recruitment projection tools to model and track progress to goals.',
        'skills': [{
            'name': 'Web Development', 'capability_id': 'cap:it',
        }],
    },
    'goucher1': {
        'id': 84,
        'description': 'Did some stuff',
        'skills': [{
            'name': 'Python', 'capability_id': 'cap:it',
        }],
    }
}

DATE_START = dt.date(2000, 1, 1)
DATE_END = dt.datetime.today()
DATE_LENGTH = ((DATE_END.year - DATE_START.year) * 12
               + DATE_END.month - DATE_START.month)

#Changes made to the EXPERIENCES constant also need to be
#made to the data in the populate_db.py script
#in the common directory

EXPERIENCES = {
    'columbia': {
        'id': 511,
        'description': 'Test description',
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': None,
        'degree_other': None,
        'link': 'www.google.com',
        'link_name': 'Google',
        'is_current': False,
        'start_month': 'September',
        'start_year': 1979,
        'end_month': 'May',
        'end_year': 1983,
        'length_year': 3,
        'length_month': 8,
        'type': 'Accomplishment',
        'contact_id': 124,
        'location': 'New York, NY, USA',
        'achievements': [],
        'skills': [
        ],
    },
    'goucher': {
        'id': 512,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'degree_other': 'Study Abroad',
        'link': None,
        'link_name': None,
        'is_current': False,
        'start_month': 'September',
        'start_year': 2012,
        'end_month': 'May',
        'end_year': 2016,
        'length_year': 3,
        'length_month': 8,
        'type': 'Education',
        'contact_id': 123,
        'location': 'Towson, MD, USA',
        'achievements': [
            ACHIEVEMENTS['goucher1'],
        ],
        'skills': [
            SKILLS['billy'][3],
        ],
    },
    'baltimore' : {
        'id': 513,
        'description': 'Test description here',
        'host': 'Baltimore Corps',
        'title': 'Systems Design Manager',
        'degree': None,
        'degree_other': None,
        'link': None,
        'link_name': None,
        'is_current': True,
        'start_month': 'January',
        'start_year': 2000,
        'end_month': 'none',
        'end_year': 0,
        'length_year': math.floor(DATE_LENGTH/12),
        'length_month': DATE_LENGTH % 12,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Baltimore, MD, USA',
        'achievements': [
            ACHIEVEMENTS['baltimore1'],
            ACHIEVEMENTS['baltimore2'],
            ACHIEVEMENTS['baltimore3'],
        ],
        'skills': SKILLS['billy'][0:2] + SKILLS['billy'][3:5],
    },
}

TAGS = {
    'python': {
        'id': 123,
        'name': 'Python',
        'type': 'Skill',
        'status': 'Active',
    },
    'webdev': {
        'id': 124,
        'name': 'Web Development',
        'type': 'Function',
        'status': 'Active',
    },
    'health': {
        'id': 125,
        'name': 'Public Health',
        'type': 'Topic',
        'status': 'Active',
    },
}

TAG_ITEMS = {
    'billy_webdev': {
        'id': 21,
        'name': 'Web Development',
        'type': 'Function',
        'contact_id': 123,
        'tag_id': 124,
        'score': 2,
    }
}

# This is kind of gross -- maybe we should consider standardizing the resume
# responses so that they're the same as everything else?
def filter_dict(d, keys):
    return {k:v for k, v in d.items() if k not in keys}

RESUME_SECTIONS = {
    'billy_work': {
        'id': 61,
        'resume_id': 51,
        'max_count': None,
        'min_count': None,
        'name': "Work Experience",
        'items': [
            {
                'resume_order': 0,
                'indented': False,
                'achievement': None,
                'tag': None,
                'experience': filter_dict(EXPERIENCES['baltimore'],
                                          {'achievements', 'contact_id'}),
            },
        ],
    },
    'billy_skills': {
        'id': 62,
        'resume_id': 51,
        'max_count': None,
        'min_count': None,
        'name': "Skills",
        'items': [
            {
                'resume_order': 0,
                'indented': False,
                'achievement': None,
                'experience': None,
                'tag': filter_dict(TAG_ITEMS['billy_webdev'], {'contact_id'}),
            },
        ],
    },
}

RESUMES = {
    'billy': {
        'id': 51,
        'contact': CONTACTS['billy'],
        'name': "Billy's Resume",
        'date_created': '2019-05-04',
        'gdoc_id': 'abcdefghijklmnopqrstuvwxyz1234567890-_',
    },
}

RESUME_OUTPUT = {
    'name': 'Billy Resume',
    'date_created': dt.datetime.today().strftime('%Y-%m-%d'),
    'contact': CONTACTS['billy'],
    'gdoc_link': None,
    'relevant_exp_dump': [EXPERIENCES['goucher']],
    'other_exp_dump': [EXPERIENCES['baltimore']],
    'relevant_edu_dump': [EXPERIENCES['goucher']],
    'other_edu_dump': [EXPERIENCES['baltimore']],
    'relevant_achieve_dump': [EXPERIENCES['baltimore']],
    'other_achieve_dump': [EXPERIENCES['goucher']],
    'relevant_skills_dump': [TAG_ITEMS['billy_webdev']],
    'other_skills_dump': [TAG_ITEMS['billy_webdev']]
}


POSTS = {
    'experience': {
        'description': 'Test description',
        'host': 'Test Org',
        'title': 'Test title',
        'start_month': 'September',
        'start_year': 2000,
        'end_month': 'May',
        'end_year': 2019,
        'link': None,
        'link_name': None,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Test City, MD, USA',
        'achievements': [
            {'description': 'Test achievement 1'},
            {'description': 'Test achievement 2', 'skills': [
                { 'name': 'Community Organizing', 'capability_id': 'cap:advocacy' },
                { 'name': 'Test Skill 1' }
            ]},
        ],
    },
    'portfolio': {
        'description': 'Test description',
        'host': 'Test Org',
        'title': 'Test title',
        'start_month': 'September',
        'start_year': 2000,
        'end_month': 'none',
        'end_year': 0,
        'link': None,
        'link_name': None,
        'type': 'Accomplishment',
        'contact_id': 123,
        'location': 'Test City, MD, USA',
        'achievements': [
            {'description': 'Test achievement 1'},
            {'description': 'Test achievement 2', 'skills': [
                { 'name': 'Community Organizing', 'capability_id': 'cap:advocacy' },
                { 'name': 'Test Skill 1' }
            ]},
        ],
    },
    'resume': {
        'name': 'Billy Resume',
        'gdoc_link': None,
        'contact_id': 123,
        'relevant_exp': [512],
        'other_exp': [513],
        'relevant_edu': [512],
        'other_edu': [513],
        'relevant_achieve': [513],
        'other_achieve': [512],
        'relevant_skills': [21],
        'other_skills': [21],
    },
    'program_contact': {
        'id': 5,
        'program_id': 1,
        'contact_id': 124,
        'card_id': 'card',
        'stage': 1
    },
    'contact': {
        "first_name": "Tester",
        "last_name": "Byte",
        "email_primary": {
            "email": "testerb@example.com",
            "is_primary": True,
        },
        "phone_primary": "111-111-1111",
        "account_id": 'test-valid|0123456789',
        "terms_agreement": True
    },
    'opportunity': {
        "title": "Test Opportunity",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "cycle_id": 1,
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Place for Purpose"
    },
    'mayoral_opportunity': {
        "title": "Mayoral Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Mayoral Fellowship"
    },
    'blank_opportunity': {
        "title": "Blank Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': None,
    },
}

APP_PUT_FULL = {
    "opportunity": OPPORTUNITIES['test_opp1'],
    "interest_statement": "dfdddsdfff",
    "id": "052904ba-7b83-436c-aee3-334a208fefd9",
    "contact": CONTACTS['billy'],
    "status": "draft",
    'interview_date': None,
    'interview_time': None,
  }

def post_request(app, url, data):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data),
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None
        id = data['id']
        return id, data


@pytest.mark.parametrize(
    "url,data,query",
    [pytest.param('/api/contacts/',
      POSTS['contact'],
      lambda id: Contact.query.get(id),
      marks=pytest.mark.skip
      # TODO: unskip when trello stuff is mocked out
      )
    ,('/api/contacts/123/experiences/',
      POSTS['experience'],
      lambda id: Experience.query.get(id)
      )
    ,('/api/contacts/123/skills/',
      {
        'name': 'C++',
      },
      lambda id: ContactSkill.query.filter_by(
          skill_id='sEVDZsMOqdfQ-vwoIAEk5A==', contact_id=123).first()
      )
     ,('/api/contacts/123/capabilities/cap:it/suggestion/',
      {
        'name': 'Network Architecture',
      },
      lambda id: CapabilitySkillSuggestion.query.get(
          (123, 'cap:it', '_s-apdaP_WZpH69G8hlcGA=='))
      )

    ,pytest.param('/api/contacts/124/programs/',
      POSTS['program_contact'],
      lambda id: ProgramContact.query.filter_by(contact_id=124,program_id=1).first(),
      marks=pytest.mark.skip
      # TODO: unskip when trello stuff is mocked out
      )
    ,('/api/opportunity/',
      POSTS['opportunity'],
      lambda id: Opportunity.query.filter_by(title="Test Opportunity").first()
      )
    ,pytest.param('/api/contacts/124/app/333abc/',
      {},
      lambda id: (OpportunityApp.query
                  .filter_by(contact_id=124, opportunity_id='123abc').first()),
      )
    ]
)
def test_post(app, url, data, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    id_, _ = post_request(app, url, data)
    assert query(id_) is not None

@pytest.mark.parametrize(
    "data,program_id",
    [(POSTS['opportunity'], 1),
    (POSTS['mayoral_opportunity'], 2),
    (POSTS['blank_opportunity'], 1)]
)
def test_post_opp_program(app, data, program_id):
    id_, data = post_request(app, '/api/opportunity/', data)
    opp = Opportunity.query.filter_by(title=data['title']).first()
    assert opp is not None
    assert opp.program_id == program_id

@pytest.mark.skip
def test_create_program_contact_with_contact(app):
    id_, _ = post_request(app, '/api/contacts/', POSTS['contact'])
    program_contacts = Contact.query.get(id_).programs
    assert len(program_contacts) == 1
    assert program_contacts[0].program_id == 1
    assert program_contacts[0].stage == 1
    assert program_contacts[0].program.name == 'Place for Purpose'
    assert program_contacts[0].is_active == True
    assert program_contacts[0].is_approved == False

def test_post_experience_date(app):
    id_, _ = post_request(app, '/api/contacts/123/experiences/',
                          POSTS['experience'])
    assert Experience.query.get(id_).end_month == Month.may
    assert Experience.query.get(id_).end_year == 2019
    assert Experience.query.get(id_).start_month == Month.september
    assert Experience.query.get(id_).start_year == 2000

def test_post_opportunity_app_status(app):
    id_, _ = post_request(app, '/api/contacts/124/app/333abc/', {})
    assert OpportunityApp.query.get(id_).stage == ApplicationStage.draft.value

def test_post_about_me(app):
    id_, data = post_request(app, '/api/contacts/124/about-me/', {})
    contact = Contact.query.get(124)
    assert contact.profile != {}
    pprint(data)
    pprint(CONTACT_PROFILE['obama_blank'])
    assert data == CONTACT_PROFILE['obama_blank']


def test_post_experience_null_start_date(app):
    exp = POSTS['experience'].copy()
    exp['start_month'] = 'none'
    exp['start_year'] = 0
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).start_month == Month.none
    assert Experience.query.get(id_).start_year == 0
    pprint(Experience.query.get(id_).start_month)
    pprint(Experience.query.get(id_).start_year)

def test_post_experience_current(app):
    exp = POSTS['experience'].copy()
    exp['end_month'] = 'none'
    exp['end_year'] = 0
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).is_current == True

def test_post_experience_dump_only(app):
    exp = POSTS['experience'].copy()
    exp['length_year'] = 18
    exp['length_month'] = 8
    exp['is_current'] = False
    exp['id'] = 1
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None

def test_post_experience_skills(app):
    exp = POSTS['experience'].copy()
    exp['skills'] = [{'name': 'C++'}, {'name': 'Python'}]
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_).skills[0].name == 'C++'
    assert Experience.query.get(id_).skills[1].name == 'Community Organizing'
    assert Experience.query.get(id_).skills[2].name == 'Python'
    assert Experience.query.get(id_).skills[3].name == 'Test Skill 1'

def test_post_experience_achievement_skills(app):
    exp = POSTS['experience']
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    skills = Experience.query.get(id_).achievements[1].skills
    assert len(Experience.query.get(id_).achievements[1].skills) == 2
    assert skills[0]['name'] == 'Community Organizing'
    assert skills[0]['capability_id'] == 'cap:advocacy'
    assert skills[1]['name'] == 'Test Skill 1'
    assert skills[1]['capability_id'] is None


def test_post_contact_skill(app):
    url, update = ('/api/contacts/123/skills/', { 'name': 'C++', })

    _, response = post_request(app, url, update)
    assert 'suggested_capabilities' in response
    assert response['suggested_capabilities'] == []
    assert 'capabilities' in response
    assert len(response['capabilities']) == 1
    assert response['capabilities'][0]['id'] == 'cap:it'

    contact_skill = ContactSkill.query.filter_by(
        contact_id=123,
        skill_id='sEVDZsMOqdfQ-vwoIAEk5A==',
        deleted=False,
    ).first()
    assert contact_skill is not None

def test_post_contact_skill_suggestion(app):
    url, update = (
        '/api/contacts/123/capabilities/cap:it/suggestion/',
        {
            'name': 'Network Architecture',
        }
    )

    _, response = post_request(app, url, update)
    assert 'capabilities' in response
    assert response['capabilities'] == []
    assert 'suggested_capabilities' in response
    assert len(response['suggested_capabilities']) == 1
    assert response['suggested_capabilities'][0]['id'] == 'cap:it'

    contact_skill = ContactSkill.query.filter_by(
        contact_id=123,
        skill_id='_s-apdaP_WZpH69G8hlcGA==',
        deleted=False,
    ).first()
    assert contact_skill is not None

def test_post_contact_skill_undelete(app):
    url, update = ('/api/contacts/123/skills/', { 'name': 'Event Planning', })

    _, response = post_request(app, url, update)
    exp = Experience.query.get(513)
    exp_skills = list(map(lambda s: s.name, exp.skills))
    print(exp_skills)
    assert 'Event Planning' in exp_skills
    achievement_skills = list(map(lambda s: s['name'], exp.achievements[1].skills))
    print(achievement_skills)
    assert 'Event Planning' in achievement_skills

def test_get_no_profile(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }
    with app.test_client() as client:
        response = client.get('/api/contacts/124/about-me', headers=headers)
        assert response.status_code == 404
        assert response.json['message'] == 'Profile does not exist'

# TODO: unskip when trello stuff is mocked out
@pytest.mark.skip
def test_post_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789',
    }
    with app.test_client() as client:
        response = client.post('/api/contacts/',
                               data=json.dumps(POSTS['contact']),
                               headers=headers)
        assert response.status_code == 201
        set_cookie = response.headers.get('set-cookie')
        assert set_cookie is not None
        assert set_cookie.find('HttpOnly;') is not -1
        # Note: Can't test "secure" due to non-https connection
        contact = Contact.query.filter_by(account_id='test-valid|0123456789').first()
        assert contact.first_name == 'Tester'

        assert UserSession.query.filter_by(contact_id=contact.id).first()

def test_post_session(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789abcdefabcdefff',
    }
    with app.test_client() as client:
        response = client.post('/api/session/', headers=headers)
        assert response.status_code == 201
        set_cookie = response.headers.get('set-cookie')
        assert set_cookie is not None
        assert set_cookie.find('HttpOnly;') is not -1
        # Note: Can't test "secure" due to non-https connection

        assert UserSession.query.filter_by(contact_id=123).first().contact.first_name == 'Billy'


@pytest.mark.skip
def test_post_formassembly_opportunity_intake(app):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    gdoc_id ='1b5erb67lgwvxj-g8u2iitvihhti6_nv-7dehdh8ldfw'

    url = '/api/form-assembly/opportunity-app/'
    data = f'google_doc_id={gdoc_id}&org=Balti&title=QA+Tester&salary_lower=50000&salary_upper=60000&google_doc_link=&capabilities%5B0%5D=tfa_16677&capabilities%5B1%5D=tfa_16678&supervisor_first_name=Billy&supervisor_last_name=Daly&supervisor_title=Director+of+Data&supervisor_email=billy%40baltimorecorps.org&supervisor_phone=4436408904&is_supervisor=tfa_16674&race=tfa_16656&gender=tfa_16662&pronouns=tfa_16668&response_id=157007055'

    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']

        assert 'gdoc_id' in data
        assert data['gdoc_id'] == gdoc_id
        assert 'title' in data
        assert data['title'] == 'QA Tester'

        opp = Opportunity.query.filter_by(gdoc_id=gdoc_id).first()
        assert opp is not None
        assert opp.title == 'QA Tester'

def skill_name(skill):
    return skill.name

@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly'},
      lambda: Contact.query.get(123),
      lambda e: e.first_name == 'William',
      ),
     ('/api/contacts/123/',
      {'first_name': 'William', 'programs': 'This should be excluded from load'},
       lambda: Contact.query.get(123),
       lambda e: e.first_name == 'William'
     ),
     ('/api/contacts/123/',
      {'skills': [
          { 'name': 'Python' },
          { 'name': 'Workforce Development' },
      ]},
      lambda: Contact.query.get(123),
      lambda e: (len(e.skills) == 2
                 and sorted(e.skills, key=skill_name)[0].name == 'Python'
                 and sorted(e.skills, key=skill_name)[1].name == 'Workforce Development'),
      ),
     ('/api/experiences/512/',
      {'end_month': 'January', 'end_year': 2017},
      lambda: Experience.query.get(512),
      lambda e: e.end_month == Month.january and e.end_year == 2017,
      )
    ,('/api/experiences/512/',
      {'achievements': EXPERIENCES['goucher']['achievements'] + [
          {'description': 'test'}
      ]},
      lambda: Experience.query.get(512),
      lambda e: e.achievements[-1].description == 'test',
      )
    ,('/api/experiences/513/',
      {'achievements': EXPERIENCES['baltimore']['achievements'][0:2] + [{
          'id': 83,
          'description': 'Developed recruitment projection tools to model and track progress to goals.',
          'skills': [{'name': 'Python', 'capability_id': 'cap:it'}],
      }]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.achievements[-1].skills) == 1
                 and e.achievements[-1].skills[0]['name'] == 'Python'
                 and e.achievements[-1].skills[0]['capability_id'] == 'cap:it'),
      )
    ,('/api/experiences/513/',
      {'achievements': EXPERIENCES['baltimore']['achievements'][0:2] + [{
          'id': 83,
          'description': 'Developed recruitment projection tools to model and track progress to goals.',
          'skills': [{'name': 'Recruitment', 'capability_id': 'cap:outreach'}],
      }]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.achievements[-1].skills) == 1
                 and e.achievements[-1].skills[0]['name'] == 'Recruitment'
                 and e.achievements[-1].skills[0]['capability_id'] == 'cap:outreach'),
      )

    ,('/api/experiences/513/',
      {'skills': SKILLS['billy'][0:2] + [{'name': 'Test'}]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.skills) == 3
                 and sorted(e.skills, key=skill_name)[0].name == 'Community Organizing'
                 and sorted(e.skills, key=skill_name)[1].name == 'Flask'
                 and sorted(e.skills, key=skill_name)[2].name == 'Test'),
      )
    ,('/api/contacts/123/programs/1/',
      {'stage': 2},
      lambda: ProgramContact.query.get(5),
      lambda r: r.stage == 2,
      )
    ,pytest.param('/api/opportunity/123abc/',
      {'title': "New title"},
      lambda: Opportunity.query.get('123abc'),
      lambda r: r.title == 'New title',
      marks=pytest.mark.skip
      )
    ,('/api/contacts/123/app/123abc',
      {'interest_statement': "New interest statement", 'resume': None},
      lambda: OpportunityApp.query.get('a1'),
      lambda r: r.interest_statement == 'New interest statement',
      )
    ,('/api/contacts/123/app/123abc',
      {'resume': {'test': 'snapshotnew'}},
      lambda: OpportunityApp.query.get('a1'),
      lambda r: r.resume.resume == '{"test":"snapshotnew"}',
      )
    ,('/api/contacts/123/app/222abc',
      {'resume': {'test': 'snapshotnew'}},
      lambda: OpportunityApp.query.get('a2'),
      lambda r: r.resume and r.resume.resume == '{"test":"snapshotnew"}',
      )
     ,('/api/contacts/123/app/123abc',
       APP_PUT_FULL,
       lambda: OpportunityApp.query.get('a1'),
       lambda r: r.interest_statement == 'dfdddsdfff',
       )
     ,('/api/contacts/123/about-me',
       CONTACT_PROFILE['billy_update'],
       lambda: Profile.query.get(123),
       lambda r: (r.contact.email == 'billy_new@email.com'
                  and r.address_primary.street1 == '124 Main St'
                  and r.race.hispanic == True
                  and r.roles.data_analysis == False),
       )
    ]
)
def test_put(app, url, update, query, test):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        assert not test(query())
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        assert test(query())

def test_put_contact_saves_deleted_skills(app):
    url, update = ('/api/contacts/123/', {'skills': [
          { 'name': 'Python' },
          { 'name': 'Workforce Development' },
      ]})

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        public_health = ContactSkill.query.filter_by(
            skill_id='n1N02ypni69EZg0SggRIIg==',
            contact_id=123).first()
        assert public_health is not None
        assert public_health.deleted

def test_put_program_apps_new(app):
    url = '/api/contacts/124/program-apps/interested'
    update = PROGRAM_APPS['obama_put']

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    obama = Contact.query.get(124)
    assert obama.program_apps == []

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        assert data == PROGRAM_APPS['obama_get']

def test_put_program_apps_update(app):
    url = '/api/contacts/123/program-apps/interested'
    update = copy.deepcopy(PROGRAM_APPS['billy'])
    update['program_apps'][0]['is_interested'] = False
    update['program_apps'][1]['is_interested'] = True

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    billy = Contact.query.get(123)
    assert billy.program_apps[0].is_interested == True
    assert billy.program_apps[1].is_interested == False

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        billy = Contact.query.get(123)
        assert billy.program_apps[0].is_interested == False
        assert billy.program_apps[1].is_interested == True

def test_put_contact_dict_error(app):
    url = '/api/contacts/123/'
    update = CONTACTS['billy_bug']

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    billy = Contact.query.get(123)

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200

def test_put_programs_completed_nullable(app):
    url = '/api/contacts/123/about-me'
    update = CONTACT_PROFILE['billy_null']

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    billy = Contact.query.get(123)
    assert billy.profile.programs_completed is not None

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        billy = Contact.query.get(123)
        assert billy.profile.programs_completed.kiva == False

def test_put_about_me_email(app):
    url = '/api/contacts/123/about-me'
    update = CONTACT_PROFILE['billy_update']

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    billy = Contact.query.get(123)
    assert billy.email == 'billy@example.com'
    assert billy.email_primary.email == 'billy@example.com'
    assert billy.email_main == 'billy@example.com'

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200

        billy = Contact.query.get(123)
        data = response.json['data']
        assert data['email'] == 'billy_new@email.com'

        assert billy.email == 'billy_new@email.com'
        assert billy.email_main == 'billy_new@email.com'
        assert billy.email_primary.email == 'billy_new@email.com'

@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly'},
      lambda: Contact.query.get(123),
      lambda e: len(e.skills) == len(SKILLS['billy']),
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.achievements) == len(EXPERIENCES['baltimore']['achievements'])
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.skills) == len(EXPERIENCES['baltimore']['skills'])
      )
    ])
def test_put_preserves_list_fields(app, url, update, query, test):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        assert test(query())

def test_put_update_achievement_skills(app):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url = '/api/experiences/513/'
    update = {
        'achievements':
              EXPERIENCES['baltimore']['achievements'][0:2] + [{
                  'id': 83,
                  'description': 'Developed recruitment projection tools to model and track progress to goals.',
                  'skills': [{'name': 'Python', 'capability_id': 'cap:it'}],
              }],
        # Achievement skills should add to experience level skills
        'skills': [],
    }
    query = lambda: Experience.query.get(513)
    test = lambda e: (len(e.achievements[-1].skills) == 1
                      and e.achievements[-1].skills[0]['name'] == 'Python')
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        assert not test(query())
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        assert data['achievements'][-1]['skills'][0]['name'] == 'Python'
        assert data['achievements'][-1]['skills'][0]['capability_id'] == 'cap:it'
        exp = query()
        assert test(exp)
        skill_names = {skill.name for skill in exp.skills}
        assert 'Python' in skill_names


def test_contact_put_preserves_experience_skills(app):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = { 'skills': EXPERIENCES['baltimore']['skills'] }
    with app.test_client() as client:
        response = client.put('/api/contacts/123/', data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200

        e = Experience.query.get(513)
        assert len(e.skills) == len(EXPERIENCES['baltimore']['skills'])

@pytest.mark.parametrize(
    "url,update,old_id,new_id",
    [('/api/contacts/123/',
      {'id': 111, 'first_name': 'test'},
      lambda: Contact.query.get(123),
      lambda: Contact.query.get(111),
      ),
     ('/api/experiences/512/',
      {'id': 555, 'host': 'test'},
      lambda: Experience.query.get(512),
      lambda: Experience.query.get(555),
      )
    ,('/api/contacts/123/programs/1/',
      {'id': 555, 'stage': 2},
      lambda: ProgramContact.query.get(5),
      lambda: ProgramContact.query.get(555),
      )
    ,('/api/opportunity/123abc/',
      {'id': 'aaaaaa', 'title': 'new title'},
      lambda: Opportunity.query.get('123abc'),
      lambda: Opportunity.query.get('aaaaaa'),
      )
    ]
)
def test_put_rejects_id_update(app, url, update, old_id, new_id):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert old_id() is not None, "Item to update should exist"
        assert new_id() is None, "New id should not exist before test"
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert old_id() is not None, "Item to update should still exist"
        assert new_id() is None, "New id should not exist after test"

def test_put_rejects_app_stage_update(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {
        'stage': 0,
        'status': 'draft',
    }
    with app.test_client() as client:
        response = client.put('/api/contacts/123/app/123abc/',
                              data=json.dumps(update),
                              headers=headers)
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value

def test_opportunity_app_not_a_fit(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').is_active == True
        response = client.post('/api/contacts/123/app/123abc/not-a-fit/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').is_active == False

def test_opportunity_app_submit(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a2').stage == ApplicationStage.draft.value
        response = client.post('/api/contacts/123/app/222abc/submit/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a2').stage == ApplicationStage.submitted.value

def test_opportunity_app_interview_completed_property(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        opp_app = OpportunityApp.query.get('a1')
        assert  opp_app.interview_completed == False

        # set interview to a scheduled date
        now = dt.datetime.now()
        scheduled = now + dt.timedelta(hours=1)
        completed = now - dt.timedelta(hours=1)
        opp_app.interview_date = scheduled.date()
        opp_app.interview_time = scheduled.strftime('%H:%M:%S')
        db.session.commit()

        # test that interview fields were set
        # and that interview_completed == False
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.interview_date == scheduled.date()
        assert opp_app.interview_time == scheduled.strftime('%H:%M:%S')
        assert opp_app.interview_completed == False

        # set interview to a completed date
        opp_app.interview_date = completed.date()
        opp_app.interview_time = completed.strftime('%H:%M:%S')
        db.session.commit()

        # test that interview fields were set
        # and that interview_completed == False
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.interview_date == completed.date()
        assert opp_app.interview_time == completed.strftime('%H:%M:%S')
        assert opp_app.interview_completed == True

def test_opportunity_app_interview(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {'interview_date': '2050-02-01',
              'interview_time': '13:00:00'}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/interview/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.interviewed.value
        assert opp_app.is_active == True
        assert opp_app.interview_date == dt.date(2050,2,1)
        assert opp_app.interview_time == '13:00:00'
        assert opp_app.interview_completed == False

def test_opportunity_app_consider(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/consider/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.considered_for_role.value
        assert OpportunityApp.query.get('a1').is_active == True

def test_opportunity_app_recommend_from_not_a_fit(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        OpportunityApp.query.get('a1').is_active = False
        db.session.commit()
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.submitted.value
        assert opp_app.is_active == False
        response = client.post('/api/contacts/123/app/123abc/recommend/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.recommended.value
        assert opp_app.is_active == True

def test_opportunity_app_recommend(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/recommend/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.recommended.value

def test_opportunity_app_reopen(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/reopen/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.draft.value

def test_opportunity_deactivate(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert Opportunity.query.get('123abc').is_active == True
        response = client.post('/api/opportunity/123abc/deactivate/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert Opportunity.query.get('123abc').is_active == False

def test_opportunity_activate(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        opp = Opportunity.query.get('123abc')
        opp.is_active = False
        db.session.commit()
        assert Opportunity.query.get('123abc').is_active == False
        response = client.post('/api/opportunity/123abc/activate/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert Opportunity.query.get('123abc').is_active == True

def test_approve_many_program_contacts_new(app, ):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload = [CONTACTS_SHORT['obama']]
    with app.test_client() as client:
        program_contact = (ProgramContact
                           .query
                           .filter_by(contact_id=124, program_id=2)
                           .first())
        assert program_contact is None
        response = client.post('/api/programs/2/contacts/approve-many/',
                              data=json.dumps(payload),
                              headers=headers)
        assert response.status_code == 200
        program_contact = (ProgramContact
                           .query
                           .filter_by(contact_id=124, program_id=2)
                           .first())
        assert program_contact is not None
        assert program_contact.is_approved == True
        data = json.loads(response.data)['data']
        obama_mayoral = APPLICATIONS_INTERNAL['obama_pfp'].copy()
        obama_mayoral['program_id'] = 2
        obama_mayoral['id'] = 1
        obama_mayoral['is_approved'] = True
        obama_mayoral['applications'] = []
        expected = [obama_mayoral]
        print(expected)
        for item in data:
            print(item)
            assert item in expected

def test_approve_many_program_contacts_existing(app, ):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload = [CONTACTS_SHORT['obama']]
    with app.test_client() as client:
        assert ProgramContact.query.get(6).is_approved == False
        response = client.post('/api/programs/1/contacts/approve-many/',
                              data=json.dumps(payload),
                              headers=headers)
        assert response.status_code == 200
        assert ProgramContact.query.get(6).is_approved == True
        data = json.loads(response.data)['data']
        expected = [APPLICATIONS_INTERNAL['obama_pfp']]
        expected[0]['is_approved'] = True
        print(expected)
        for item in data:
            print(item)
            assert item in expected

def test_reapprove_many_program_contacts(app, ):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload = [CONTACTS_SHORT['billy'], CONTACTS_SHORT['obama']]
    with app.test_client() as client:
        assert ProgramContact.query.get(6).is_approved == False
        assert ProgramContact.query.get(5).is_approved == True
        response = client.post('/api/programs/1/contacts/approve-many/',
                              data=json.dumps(payload),
                              headers=headers)
        assert response.status_code == 200
        assert ProgramContact.query.get(6).is_approved == True
        assert ProgramContact.query.get(5).is_approved == True
        data = json.loads(response.data)['data']
        expected = [APPLICATIONS_INTERNAL['obama_pfp'],
                    APPLICATIONS_INTERNAL['billy_pfp']]
        print(expected)
        for item in data:
            print(item)
            assert item in expected

def test_approve_program_contact_fake_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload = [{'id': 4,
                'first_name': 'Fake',
                'last_name': 'Person',
                'email': 'fake@gmail.com'}]
    with app.test_client() as client:
        assert ProgramContact.query.get(5).is_approved == True
        response = client.post('/api/programs/1/contacts/approve-many/',
                              data=json.dumps(payload),
                              headers=headers)
        assert response.status_code == 404
        message = json.loads(response.data)['message']
        assert message == "Payload contained contacts that couldn't be found"

@pytest.mark.parametrize(
    "delete_url,query",
    [('/api/contacts/123',
      lambda: Contact.query.get(123))
    ,('/api/experiences/512/', lambda: Experience.query.get(512))
    ,('/api/contacts/123/skills/n1N02ypni69EZg0SggRIIg==',
      lambda: ContactSkill.query.filter_by(
          skill_id='n1N02ypni69EZg0SggRIIg==', contact_id=123, deleted=False).first())
    ,('/api/contacts/123/capabilities/cap:it/suggestion/QUEVjv1tcq6uLmzCku6ikg==',
      lambda: CapabilitySkillSuggestion.query.get(
          (123, 'cap:it', 'QUEVjv1tcq6uLmzCku6ikg=='))
      )
    ]

)
def test_delete(app, delete_url, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to delete should exist"

        response = client.delete(delete_url, headers=headers)
        assert response.status_code == 200
        assert query() is None, "Deleted item should not exist"


def test_delete_contact_skill_saved(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    delete_url = '/api/contacts/123/skills/n1N02ypni69EZg0SggRIIg=='
    with app.test_client() as client:
        response = client.delete(delete_url, headers=headers)
        assert response.status_code == 200
        contact_skill = ContactSkill.query.filter_by(
            skill_id='n1N02ypni69EZg0SggRIIg==', contact_id=123).first()
        assert contact_skill is not None
        assert contact_skill.deleted


@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/123/', CONTACTS['billy'])
    ,('/api/contacts/124/', CONTACTS['obama'])
    ,('/api/experiences/512/', EXPERIENCES['goucher'])
    ,('/api/experiences/513/', EXPERIENCES['baltimore'])
    ,('/api/contacts/123/skills', SKILLS['billy'])
    ,('/api/contacts/123/programs/1', PROGRAM_CONTACTS['billy_pfp'])
    ,('/api/opportunity/123abc', OPPORTUNITIES['test_opp1'])
    ,('/api/contacts/123/app/123abc', APPLICATIONS['app_billy'])
    ,('/api/org/opportunities/123abc', OPPORTUNITIES_INTERNAL['test_opp1'])
    ,('/api/contacts/123/about-me', CONTACT_PROFILE['billy_profile'])
    ,('/api/contacts/123/program-apps', PROGRAM_APPS['billy'])
    ]
)
def test_get(app, url, expected):
    #the expected data comes from the EXPERIENCES constant above
    #the actual data come from the populate_db.py script
    #in the common directory
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        pprint(data)
        pprint(expected)
        assert len(data) > 0
        assert data == expected


def test_get_autocomplete(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    query = {
        'q': 'Pyt',
    }
    with app.test_client() as client:
        response = client.get('/api/skills/autocomplete/',
                              query_string=query, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert 'matches' in data
        assert 'got_exact' in data
        assert 'Python' in data['matches']

def test_get_capability_recommendations(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    expected = {
        'Advocacy and Public Policy': [
            'Community Organizing',
            'Canvassing',
            'Advocacy',
            'Policy Writing',
            'Volunteer Mobilization',
        ],
        'Community Engagement and Outreach': [
            'Community Engagement',
            'Client Recruitment',
            'Partnership Building',
            'Event Planning',
            'Community Organizing',
        ],
        'Information Technology': [],
    }
    with app.test_client() as client:
        response = client.get('/api/capabilities/',
                              headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        pprint(data)
        for capability in data:
            assert capability['name'] in expected
            for i, skill in enumerate(capability['recommended_skills']):
                skill['skill']['name'] == expected[capability['name']][i]

@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/', [CONTACTS['billy'], CONTACTS['obama']])
    ,('/api/contacts/123/experiences/', [EXPERIENCES['goucher'],
                                         EXPERIENCES['baltimore']])
    ,('/api/contacts/124/experiences/', [EXPERIENCES['columbia']])
    ,('/api/contacts/123/achievements/', ACHIEVEMENTS.values())
    ,('/api/contacts/123/programs/', [PROGRAM_CONTACTS['billy_pfp'], PROGRAM_CONTACTS['billy_mayoral']])
    ,('/api/opportunity/', OPPORTUNITIES.values())
    ,('/api/contacts/123/app/', [APPLICATIONS['app_billy']])
    ,('/api/internal/opportunities/', OPPORTUNITIES_INTERNAL.values())
    ,('/api/contacts/short/', CONTACTS_SHORT.values())
    ,('/api/internal/applications/',
      [APPLICATIONS_INTERNAL['billy_pfp']])
    ,('/api/internal/applications/?program_id=1',
      [APPLICATIONS_INTERNAL['billy_pfp']])
    ,('/api/contacts/programs/', CONTACT_PROGRAMS.values())
    ,('/api/contacts/programs/?is_approved=true', [CONTACT_PROGRAMS['billy']])
    ,('/api/contacts/programs/?is_approved=false', [CONTACT_PROGRAMS['obama']])
    ,('/api/programs', PROGRAMS.values())
    ]
)
def test_get_many_unordered(app, url, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        # Test that the data and expected contain the same items, but not
        # necessarily in the same order
        pprint(list(expected))
        pprint(data)
        assert len(data) == len(expected)
        for item in data:
            pprint(item)
            assert item in expected

def test_get_contact_capabilities(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url, expected = ('/api/contacts/123/capabilities/', CAPABILITIES['billy'])
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        pprint(expected)
        pprint(data)
        assert data == expected

@pytest.mark.skip
def test_get_contact_without_apps(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url, expected = ('/api/contacts/124/app/', [])
    with app.test_client() as client:

        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        pprint(expected)
        pprint(data)
        assert data == expected

@pytest.mark.skip
@pytest.mark.parametrize(
    "url,input,output",
    [('/api/contacts/123/generate-resume/',POSTS['resume'],RESUME_OUTPUT)]
)
def test_generate_resume(app, url, input, output):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.post(url, data=json.dumps(input),
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data == output


def make_session(contact_id, permissions=[]):
    return UserSession(
        id="fake_session_id",
        auth_id="fake_auth_id",
        contact_id=contact_id,
        jwt=json.dumps({'permissions': permissions}),
        expiration=(dt.datetime.utcnow() + dt.timedelta(days=1)),
    )

@pytest.mark.parametrize(
    "method,url,data,successes,failures",
    [pytest.param(
        'POST',
        '/api/opportunity/',
      POSTS['opportunity'],
      [make_session(1, ['write:opportunity'])],
      [make_session(1)],
      marks=pytest.mark.skip)
    ]
)
def test_authz(app, method, url, data, successes, failures):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'X-Test-Authz': '1',
    }

    for success in successes:
        with app.test_client() as client:
            g.test_user = success
            client_method = getattr(client, method.lower())
            response = client_method(url, data=json.dumps(data), headers=headers)
            assert response.status_code != 401

    for failure in failures:
        with app.test_client() as client:
            g.test_user = failure
            client_method = getattr(client, method.lower())
            response = client_method(url, data=json.dumps(data), headers=headers)
            assert response.status_code == 401
