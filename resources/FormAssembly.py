from flask_restful import Resource, request
from models.base_model import db
from models.program_contact_model import ProgramContact, ProgramContactSchema
from models.program_model import Program
from models.review_model import Review
from .Trello_Intake_Talent import get_intake_talent_board_id
from .ProgramContacts import query_one_program_contact
from .trello_utils import (
    query_board_data,
    update_card,
    Board,
    Card,
    BoardList
)

program_contact_schema = ProgramContactSchema()

def get_review_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.review_talent_board_id

class TalentProgramApp(Resource):

    def post(self):
        form_data = request.form
        contact_id = int(form_data['contact_id'])
        program_id = int(form_data['program_id'])
        if not (contact_id or program_id):
            return {'message': 'No contact_id or program_id provided'}, 400
        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'No program_contact record found'}, 400

        intake_board_id = get_intake_talent_board_id(program_id)
        review_board_id = get_review_talent_board_id(program_id)
        intake_card_id = program_contact.card_id
        intake_board_data = query_board_data(intake_board_id)
        review_board_data = query_board_data(review_board_id)
        intake_board = Board(intake_board_data)
        review_board = Board(review_board_data)
        intake_card = intake_board.cards.get(intake_card_id)
        if not intake_card:
            return {'message': 'No intake card found'}, 400

        # sets the data to create or update the review card
        card_data = {
            'name': f'Applicant {contact_id}',
            'desc': (
                '**Racial Equity & Baltimore: '
                'Why is racial equity work in Baltimore '
                'important to you?**\n\n'
                f"{form_data['equity']}\n\n---\n\n"
                '**Sector Effectiveness: How has your background'
                ' and experiences prepared you for today’s work'
                ' in Baltimore’s social impact sector?**\n\n'
                f"{form_data['effectiveness']}\n\n"
            )
        }

        # checks to see if a review already exists
        # updates the associated card if one does
        # creates a new card and record if one doesn't
        review_card = None
        if program_contact.reviews:
            print(program_contact.reviews[0].card_id)
            review = program_contact.reviews[0]
            review_card = review_board.cards.get(review.card_id)
        if review_card:
            update_card(review_card.id, **card_data)
        else:
            del program_contact.reviews[:]
            to_review_list = review_board.lists['stage'][1]
            review_card = to_review_list.add_card_from_template(**card_data)
            if not review_card:
                return {'message': 'Issue creating review card'}, 400
            review = Review(card_id=review_card.id, stage=1)
            program_contact.reviews.append(review)
            db.session.add(review)
            db.session.commit()
        review_card.set_custom_field_values(**{'Review ID': str(review.id)})

        # moves intake card and updates program_contact to stage 2
        # sets Review ID custom field on review_card
        program_contact.update(**{'stage': 2})
        submitted_list = intake_board.lists['stage'][2]
        intake_card.move_card(submitted_list)
        result = program_contact_schema.dump(program_contact)
        return {'status': 'success', 'data': result}, 201
