import os
import uuid

from flask_restful import Resource, request
from flask_login import login_required
from marshmallow import ValidationError

from models.base_model import db

from auth import (
    is_authorized_view,
    is_authorized_write,
    unauthorized,
    refresh_session,
    is_authorized_with_permission
)
from models.opportunity_app_model import OpportunityApp, ApplicationStage
from models.opportunity_model import OpportunityAppSchema
from models.resume_model import ResumeSnapshot

opportunity_app_schema = OpportunityAppSchema()
opportunity_app_schema_many = OpportunityAppSchema(many=True)

# TODO: Change this so it returns all applications instead of just submitted ones
class OpportunityAppAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session]
    }

    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()
        opportunity_apps = (OpportunityApp.query
            .filter(OpportunityApp.contact_id==contact_id,
                    OpportunityApp.stage>=ApplicationStage.submitted.value)
            .all())
        data = opportunity_app_schema_many.dump(opportunity_apps)
        return {'status': 'success', 'data': data}, 200

class OpportunityAppOne(Resource):
    method_decorators = {
        'get': [], #this used to be [login_required, refresh_session]
        'post': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }

    def get(self, contact_id, opportunity_id):

        # TODO: Create permission for employers so we can restore AuthZ
        #if not is_authorized_view(contact_id):
        #    return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404


        data = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': data}, 200

    def post(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if opportunity_app:
            return {'message': 'Application already exists!'}, 400

        opportunity_app = OpportunityApp(
            id=str(uuid.uuid4()),
            contact_id=contact_id,
            opportunity_id=opportunity_id,
            interest_statement=''
        )
        db.session.add(opportunity_app)
        db.session.commit()

        data = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': data}, 201

    def put(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = opportunity_app_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404

        if data.get('resume') is not None:
            if opportunity_app.resume is None:
                opportunity_app.resume = ResumeSnapshot(
                    **data['resume']
                )
            else:
                opportunity_app.resume.resume = data['resume']['resume']
            del data['resume']

        opportunity_app.update(**data)

        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200

class OpportunityAppReopen(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, contact_id, opportunity_id):
        if not is_authorized_with_permission("write:app"):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        if opportunity_app.stage == ApplicationStage.draft.value:
            return {'message': 'Application is already open for editing'}, 400

        opportunity_app.stage = ApplicationStage.draft.value
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200


class OpportunityAppSubmit(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        if opportunity_app.stage >= ApplicationStage.submitted.value:
            return {'message': 'Application is already submitted'}, 400

        opportunity_app.stage = ApplicationStage.submitted.value
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200

class OpportunityAppRecommend(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, contact_id, opportunity_id):

        if not is_authorized_with_permission('write:app'):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        if opportunity_app.stage >= ApplicationStage.recommended.value:
            return {'message': 'Application is already recommended'}, 400

        opportunity_app.stage = ApplicationStage.recommended.value
        opportunity_app.is_active = True
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200

class OpportunityAppReject(Resource):

    def post(self, contact_id, opportunity_id):

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        if opportunity_app.is_active == False:
            return {'message': 'Application is already marked "Not a Fit"'}, 400

        opportunity_app.is_active = False
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200

class OpportunityAppInterview(Resource):

    def post(self, contact_id, opportunity_id):

        json_data = request.get_json(force=True)
        try:
            data = opportunity_app_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())
        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404

        opportunity_app.stage = ApplicationStage.interviewed.value
        opportunity_app.is_active = True
        opportunity_app.update(**data)
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200

class OpportunityAppConsider(Resource):

    def post(self, contact_id, opportunity_id):
        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())
        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404

        opportunity_app.stage = ApplicationStage.considered_for_role.value
        opportunity_app.is_active = True
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200
