import json
from jsonschema import validate, ValidationError
from structlog import get_logger

from sqlalchemy.exc import SQLAlchemyError

from application.models.models import CommunicationTemplate
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from application.models.schema import template_schema
from application.utils.database import db


logger = get_logger()

PREEXISTING_TEMPLATE = 'ID already exists'


def get_template_by_id(template_id):
    try:
        template = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id).first()
    except SQLAlchemyError:
        logger.exception("Unable to retrieve template with id", id=template_id)
        raise DatabaseError("Unable to retrieve template with id: {}".format(template_id), status_code=500)
    return template


def get_templates_by_classifiers(classifiers):
    try:
        templates = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.classification == classifiers)\
            .all()
    except SQLAlchemyError:
        logger.exception('Unable to retrieve template with classifiers', classifiers=classifiers)
        classifiers_json = json.dumps(classifiers)
        raise DatabaseError('Unable to retrieve template with classifiers: {}'.format(classifiers_json), status_code=500)
    return templates


def validate_template(template):
    try:
        validate(template, template_schema)
    except ValidationError as exception:
        logger.exception("Attempted to upload invalid template")
        raise InvalidTemplateException(exception.message, status_code=400)


def upload_comms_template(template_id, template_object):

    logger.info("Uploading comms template with id", id=template_id)

    validate_template(template_object)

    existing_template = get_template_by_id(template_id)

    if existing_template:
        logger.info("Attempted to upload already existing template", id=template_id)
        raise InvalidTemplateException(PREEXISTING_TEMPLATE, status_code=400)

    label = template_object.get('label')
    type = template_object.get('type')
    uri = template_object.get('uri')
    classification = template_object.get('classification')
    params = template_object.get('params')

    template = CommunicationTemplate(id=template_id, label=label, type=type, uri=uri, classification=classification,
                                     params=params)

    db.session.add(template)

    logger.info("Uploaded template", id=template_id)


def get_comms_template_by_id(template_id):
    template = get_template_by_id(template_id)
    if not template:
        logger.info("Tried to GET non-existent template with id", id=template_id)
    return template.to_dict() if template else template


def get_comms_templates_by_classifiers(classifiers):
    templates = get_templates_by_classifiers(classifiers)
    if templates:
        template_list = [template.to_dict() for template in templates]
    else:
        logger.info("Couldn't find template with classifiers", classifiers=classifiers)
        template_list = None

    return template_list
