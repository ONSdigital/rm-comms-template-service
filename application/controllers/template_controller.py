from application.models.models import CommunicationTemplate
from application.utils.session_wrapper import with_db_session
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from application.models.schema import template_schema
from jsonschema import validate, ValidationError
from structlog import get_logger


logger = get_logger()

UPLOAD_SUCCESSFUL = 'The upload was successful'


def get_template_by_id(template_id, session):
    return session.query(CommunicationTemplate).filter(CommunicationTemplate.id == template_id).first()


def validate_template(template):
    try:
        validate(template, template_schema)
    except ValidationError as exception:
        logger.exception("Attempted to upload invalid template")
        raise InvalidTemplateException('Template is invalid', status_code=400)


class TemplateController(object):

    @staticmethod
    @with_db_session
    def upload_comms_template(template_id, template_object, session=None):
        logger.info('Uploading comms template with id {}.'.format(template_id))

        validate_template(template_object)

        existing_template = get_template_by_id(template_id, session)

        if existing_template:
            logger.info("Attempted to upload already existing template, id {}".format(template_id))
            raise InvalidTemplateException('Id already exists', status_code=400)

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
    @with_db_session
    def get_comms_template_by_id(template_id, session=None):
        template = get_template_by_id(template_id, session)
        if not template:
            raise DatabaseError("Template with id {} doesn't exist".format(template_id), status_code=404)
        return template.to_dict()
