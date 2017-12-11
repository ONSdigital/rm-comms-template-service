from structlog import get_logger

from sqlalchemy.exc import SQLAlchemyError
from jsonschema import validate, ValidationError

from application.models.models import CommunicationTemplate
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from application.models.schema import template_schema
from application.utils.database import db


logger = get_logger()

PREEXISTING_TEMPLATE = 'ID already exists'


def _get_template_by_id(template_id):
    try:
        template = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id).first()
    except SQLAlchemyError:
        logger.exception("Unable to retrieve template", id=template_id)
        raise DatabaseError("Unable to retrieve template with id: {}".format(template_id), status_code=500)
    return template


def _validate_template(template):
    try:
        validate(template, template_schema)
    except ValidationError as exception:
        logger.exception("Attempted to upload invalid template")
        raise InvalidTemplateException(exception.message, status_code=400)


def _create_or_update_template(template_id, template_object):
    label = template_object.get('label')
    type = template_object.get('type')
    uri = template_object.get('uri')
    classification = template_object.get('classification')
    params = template_object.get('params')

    template = CommunicationTemplate(id=template_id, label=label, type=type, uri=uri, classification=classification,
                                     params=params)

    db.session.merge(template)
    logger.info("Uploaded template", id=template_id)


def create_comms_template(template_id, template=None):
    logger.info('Creating template', id=template_id)

    _validate_template(template)
    existing_template = _get_template_by_id(template_id)

    if existing_template:
        logger.info("Attempted to create an already existing template", id=template_id)
        raise InvalidTemplateException(PREEXISTING_TEMPLATE, status_code=409)

    _create_or_update_template(template_id, template)


def update_comms_template(template_id, template=None):
    logger.info('Updating template', id=template_id)
    is_created = True

    _validate_template(template)
    existing_template = _get_template_by_id(template_id)

    if existing_template:
        is_created = False

    _create_or_update_template(template_id, template)
    return is_created


def get_comms_template_by_id(template_id):
    template = _get_template_by_id(template_id)

    if not template:
        logger.info("Tried to GET non-existent template", id=template_id)

    return template.to_dict() if template else template
