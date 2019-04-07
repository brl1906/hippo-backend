from flask_restful import Resource, request
from models.tag_model import Tag, TagSchema, TagItem, TagItemSchema, TagStatusType, TagType, ContactTagSchema
from models.contact_model import Contact, ContactAllSchema
from models.base_model import db


contacts_schema = ContactAllSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
tagitem_schema = TagItemSchema()
contacttag_schema = ContactTagSchema(many=True)


# Returns a list of all tags
class TagAll(Resource):

	def get(self):
		tags = Tag.query.with_entities(Tag.id, Tag.name, Tag.type)
		tags_list = tags_schema.dump(tags).data

		return {'status': 'success', 'data': tags_list}, 200


# Returns a specific tag
class TagOne(Resource):

	def get(self, tag_id):
		tags_list = Tag.query.with_entities(Tag.id, Tag.name, Tag.type)\
						.filter_by(id=tag_id)
		
		if not tags_list.first():
			return {'message': 'Tag does not exist'}, 400

		tag = tag_schema.dump(tags_list.first()).data

		return {'status': 'success', 'data': tag}, 200


	def post(self, tag_id):
		json_data = request.get_json(force=True)

		if not json_data:
			return {'message': 'No input data provided'}, 400

		# Validate and deserialize input
		data, errors = tag_schema.load(json_data)
		if errors:
			return errors, 422

		tag = Tag(**data)

		db.session.add(tag)
		db.session.commit()
		result = tag_schema.dump(tag).data

		return {"status": 'success', 'data': result}, 201


	def delete(self, tag_id):
		tag = Tag.query.with_entities(Tag.id, Tag.name, Tag.type, Tag.status)\
						.filter_by(id=tag_id)
		if not tag.first():
			return {'message': 'Tag does not exist'}, 400
		tag.delete()
		db.session.commit()
		return {"status": 'success'}, 201


	def put(self, tag_id):
		tag = Tag.query.with_entities(Tag.id, Tag.name, Tag.type, Tag.status)\
						.filter_by(id=tag_id)
		if not tag.first():
			return {'message': 'Tag does not exist'}, 400
		json_data = request.get_json(force=True)
		data, errors = tag_schema.load(json_data)
		if not data:
			return {'message': 'No data provided to update'}, 400
		tag.update(data)
		db.session.commit()
		return {"status": 'success'}, 201


class TagItemQuery(Resource):
	# returns a list of tags associated with a given contact
	def get(self, contact_id):
		tags = db.session.query(Tag, Contact, TagItem)\
						.with_entities(TagItem.contact_id, TagItem.tag_id, Tag.name, Tag.type)\
						.filter(TagItem.contact_id==contact_id)\
						.filter(TagItem.contact_id==Contact.id)\
						.filter(TagItem.tag_id==Tag.id).all()

		tags_list = contacttag_schema.dump(tags).data		
		return {'status': 'success', 'data': tags_list}, 200
		

