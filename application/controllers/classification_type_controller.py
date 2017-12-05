from flask import current_app
from application.utils.session_wrapper import with_db_session
from application.models.classification_type import ClassificationType
from application.utils.exceptions import InvalidClassificationType
from application.controllers.template_controller import UPLOAD_SUCCESSFUL
from structlog import get_logger

logger = get_logger()


def get_classification(classification_type, session):
    return session.query(ClassificationType).filter(ClassificationType.name == classification_type).first()


class ClassificationTypeController(object):

    @staticmethod
    def upload_classification_type(classification_type):
        session = current_app.db.session()
        logger.info('Uploading classification type: {}'.format(classification_type))

        existing_classification_type = get_classification(classification_type, session)

        if existing_classification_type:
            logger.info("Attempted to upload an already existing classification type: {}"
                        .format(classification_type))
            raise InvalidClassificationType("Attempted to upload an already existing classification type: {}"
                                            .format(classification_type), 400)

        classification = ClassificationType(name=classification_type)

        session.add(classification)

        logger.info("Uploaded new classification type : {}".format(classification_type))

        return UPLOAD_SUCCESSFUL

    @staticmethod
    def get_classification_types():
        session = current_app.db.session()
        classification = get_classification(classification_type, session)
        if not classification:
            logger.info("Attempted to retrieve a non existent classification type: {}".format(classification_type))
            raise InvalidClassificationType("Attempted to retrieve a non existent classification type: {}"
                                            .format(classification_type), status_code=404)
        return classification.to_dict()

    @staticmethod
    def get_classification_types():
        session = current_app.db.session()
        classification_types = session.query(ClassificationType).all()
        if not classification_types:
            logger.info("Attempted to retrieve classification types when none in database")
            raise InvalidClassificationType("Attempted to retrieve classification types when none in database",
                                            status_code=404)
        classification_types_dict = [classification.to_dict() for classification in classification_types]
        return classification_types_dict
