from jsonschema import validate, ValidationError
from structlog import get_logger

from sqlalchemy.exc import SQLAlchemyError
from flask import current_app

from application.models.models import CommunicationTemplate
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from application.models.schema import template_schema


logger = get_logger()

UPLOAD_SUCCESSFUL = 'The upload was successful'
PREEXISTING_TEMPLATE = 'ID already exists'


def get_template_by_id(template_id, session):
    try:
        template = session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id).first()
    except SQLAlchemyError:
        logger.exception("Unable to retrieve template with id: {}".format(template_id))
        raise DatabaseError("Unable to retrieve template with id: {}".format(template_id), status_code=500)
    return template


def validate_template(template):
    try:
        validate(template, template_schema)
    except ValidationError as exception:
        logger.exception("Attempted to upload invalid template")
        raise InvalidTemplateException(exception.message, status_code=400)


class TemplateController(object):

    @staticmethod
    def upload_comms_template(template_id, template_object):
        session = current_app.db.session()

        logger.info('Uploading comms template with id {}.'.format(template_id))

        validate_template(template_object)

        existing_template = get_template_by_id(template_id, session)

        if existing_template:
            logger.info("Attempted to upload already existing template, id {}".format(template_id))
            raise InvalidTemplateException(PREEXISTING_TEMPLATE, status_code=400)

        label = template_object.get('label')
        type = template_object.get('type')
        uri = template_object.get('uri')
        classification = template_object.get('classification')
        params = template_object.get('params')

        template = CommunicationTemplate(id=template_id, label=label, type=type, uri=uri, classification=classification,
                                         params=params)

        session.add(template)

        logger.info("Uploaded template with id {}".format(template_id))

        return UPLOAD_SUCCESSFUL

    @staticmethod
    def get_comms_template_by_id(template_id):
        session = current_app.db.session()

        template = get_template_by_id(template_id, session)

        if not template:
            logger.info("Tried to GET non-existent template with id {}".format(template_id))

        return template.to_dict() if template else template
