import json
from structlog import get_logger

from sqlalchemy.exc import SQLAlchemyError
from jsonschema import validate, ValidationError

from application.models.models import CommunicationTemplate
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from application.models.schema import template_schema
from application.utils.database import db
from application.controllers.classification_type_controller import get_classification_types


logger = get_logger()

PREEXISTING_TEMPLATE = 'ID already exists'


def _get_template_by_id(template_id):
    try:
        template = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id).first()
    except SQLAlchemyError:
        logger.exception('Unable to retrieve template', id=template_id)
        raise DatabaseError(f'Unable to retrieve template with id: {template_id}', status_code=500)
    return template


def get_templates_by_classifiers(classifiers):
    try:
        templates = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.classification == classifiers)\
            .all()
    except SQLAlchemyError:
        logger.exception('Unable to retrieve template with classifiers', classifiers=classifiers)
        raise DatabaseError(f'Unable to retrieve template with classifiers: {json.dumps(classifiers)}', status_code=500)
    return templates


def _validate_template_schema(template):
    try:
        validate(template, template_schema)
    except ValidationError as exception:
        logger.exception('Attempted to upload invalid template')
        raise InvalidTemplateException(exception.message, status_code=400)


def _validate_classification_types_exist(template_classifications):
    existing_classification_types = get_classification_types()

    if not existing_classification_types:
        raise InvalidTemplateException('There are no classification types available to create a template', 500)

    for classification_type in template_classifications:
        if classification_type not in existing_classification_types:
            raise InvalidTemplateException(
                f'Classification type {classification_type} is not a valid classification type', status_code=400)


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

    _validate_template_schema(template)

    _validate_classification_types_exist(template.get('classification'))

    existing_template = _get_template_by_id(template_id)

    if existing_template:
        logger.info('Attempted to create an already existing template', id=template_id)
        raise InvalidTemplateException(PREEXISTING_TEMPLATE, status_code=409)

    _create_or_update_template(template_id, template)


def update_comms_template(template_id, template=None):
    logger.info('Updating template', id=template_id)
    is_created = True

    _validate_template_schema(template)
    existing_template = _get_template_by_id(template_id)

    if existing_template:
        is_created = False

    _create_or_update_template(template_id, template)
    return is_created


def get_comms_template_by_id(template_id):
    template = _get_template_by_id(template_id)

    if not template:
        logger.info('Tried to GET non-existent template', id=template_id)

    return template.to_dict() if template else template


def get_comms_templates_by_classifiers(classifiers=None):
    templates = get_templates_by_classifiers(classifiers)

    if templates:
        return [template.to_dict() for template in templates]

    logger.info('Could not find template with classifiers', classifiers=classifiers)


def delete_comms_template(template_id):
    deleted_templates = _delete_template(template_id)
    if deleted_templates >= 1:
        is_deleted = True
        logger.info('Deleted template with id', id=template_id)
    else:
        is_deleted = False
        logger.info('Attempted to delete non-existent template', id=template_id)

    return is_deleted


def _delete_template(template_id):
    try:
        deleted_templates = db.session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id)\
            .delete()
    except SQLAlchemyError:
        logger.exception('Unable to delete template', id=template_id)
        raise DatabaseError(f'Exception thrown while trying to delete template with id {template_id}', status_code=500)
    return deleted_templates
