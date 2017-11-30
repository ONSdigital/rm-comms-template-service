import enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.json import JSONB
from application.utils.database import db


class CommunicationType(enum.Enum):
    EMAIL = "EMAIL"
    LETTER = "LETTER"
    SMS = "SMS"


class ClassificationType(enum.Enum):
    LEGAL_STATUS = "LEGAL_STATUS"
    INDUSTRY = "INDUSTRY"
    GEOGRAPHY = "GEOGRAPHY"
    COLLECTION_EXERCISE = "COLLECTION_EXERCISE"
    RU_REF = "RU_REF"
    SURVEY_REF = "SURVEY_REF"
    ENROLMENT_STATUS = "ENROLMENT_STATUS"


class CommunicationTemplate(db.Model):
    __tableargs__ = {"schema": "templatesvc"}
    __tablename__ = 'template'

    id = db.Column(UUID, unique=True, primary_key=True)
    label = db.Column(db.Text)
    type = db.Column(db.Enum(CommunicationType))
    uri = db.Column(db.Text)
    classification = db.Column(JSONB)
    params = db.Column(JSONB)
