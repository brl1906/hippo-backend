from flask import Blueprint
from flask_restful import Api
from resources.Contacts import ContactAll, ContactOne, Profile
from resources.Experience import ExperienceAll, ExperienceOne
from resources.Tag import TagAll, TagOne, ContactWithThisTagSearch


api_bp = Blueprint('api',__name__)
api = Api(api_bp)

# Route
api.add_resource(ContactAll, '/contacts')
api.add_resource(ContactOne, '/contacts/<int:contact_id>', '/contacts')
api.add_resource(Profile, '/contacts/<int:contact_id>/profile')
api.add_resource(ExperienceAll, '/contacts/<int:contact_id>/experiences/')
api.add_resource(ExperienceOne, '/contacts/<int:contact_id>/experiences/',
                 '/contacts/<int:contact_id>/experiences/<int:experience_id>')
api.add_resource(TagAll, '/tags')
api.add_resource(TagOne, '/tags/<int:tag_id>')
api.add_resource(ContactWithThisTagSearch, '/contacts/tag-search/<int:tag_id>')