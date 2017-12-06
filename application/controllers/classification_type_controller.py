from flask import current_app

from structlog import get_logger
from sqlalchemy.exc import SQLAlchemyError

from application.models.classification_type import ClassificationType
from application.utils.exceptions import InvalidClassificationType, DatabaseError
from application.controllers.template_controller import UPLOAD_SUCCESSFUL

logger = get_logger()


def get_classification(classification_type, session):
    try:
        classification = session.query(ClassificationType)\
            .filter(ClassificationType.name == classification_type).first()
    except SQLAlchemyError:
        logger.exception("Unable to retrieve template with id: {}".format(classification_type))
        raise DatabaseError("Unable to retrieve template with id: {}".format(classification_type), status_code=500)
    return classification


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

        return classification.to_dict() if classification else classification

    @staticmethod
    def get_classification_types():
        session = current_app.db.session()
        classification_types = session.query(ClassificationType).all()

        if classification_types:
            classification_types_dict = [classification.to_dict() for classification in classification_types]
        else:
            logger.info("Attempted to retrieve classification types when none in database")
            classification_types_dict = None

        return classification_types_dict
