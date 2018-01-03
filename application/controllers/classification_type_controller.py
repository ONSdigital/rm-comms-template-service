from structlog import get_logger
from sqlalchemy.exc import SQLAlchemyError

from application.models.classification_type import ClassificationType
from application.utils.exceptions import InvalidClassificationType, DatabaseError
from application.utils.database import db
logger = get_logger()


def _get_classification(classification_type):
    try:
        classification = db.session.query(ClassificationType)\
            .filter(ClassificationType.name == classification_type).first()
    except SQLAlchemyError:
        logger.exception("Unable to retrieve classification type", classification_type=classification_type)
        raise DatabaseError(f'Unable to retrieve classification type: {classification_type}', status_code=500)
    return classification


def create_classification_type(classification_type):
    logger.info(f'Uploading classification type: {classification_type}')

    existing_classification_type = _get_classification(classification_type)

    if existing_classification_type:
        logger.info("Attempted to upload an already existing classification type",
                    classification_type=classification_type)
        raise InvalidClassificationType(
            f'Attempted to upload an already existing classification type: {classification_type}', 409)

    classification = ClassificationType(name=classification_type)

    db.session.add(classification)

    logger.info("Uploaded new classification type", classification_type=classification_type)


def get_classification_type(classification_type):
    classification = _get_classification(classification_type)

    if classification:
        return classification.to_dict()

    logger.info("Attempted to retrieve a non existent classification type",
                classification_type=classification_type)


def get_classification_types():
    try:
        classification_types = db.session.query(ClassificationType).all()
    except SQLAlchemyError:
        logger.exception("Unable to get classification types")
        raise DatabaseError('Exception thrown while trying to get all classification types', status_code=500)

    if classification_types:
        return [classification.to_dict() for classification in classification_types]

    logger.info("Attempted to retrieve classification types when none in database")


def _delete_classification_query(classification_type):
    try:
        deleted_classification_types_count = db.session.query(ClassificationType).filter(ClassificationType.name ==
                                                                                         classification_type).delete()
    except SQLAlchemyError:
        logger.exception("Unable to delete classification type", classification_type=classification_type)
        raise DatabaseError(f'Exception thrown while trying to delete classification type {classification_type}',
                            status_code=500)
    return deleted_classification_types_count


def delete_classification_type(classification_type):
    records_deleted = _delete_classification_query(classification_type)

    if records_deleted >= 1:
        logger.info("Deleted classification type", classification_type=classification_type)
        return True

    logger.info("Attempted to delete non-existent classification type", classification_type=classification_type)
    return False
