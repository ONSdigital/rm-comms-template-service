import enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql.json import JSONB
from application.utils.database import db


class CommunicationType(enum.Enum):
    EMAIL: 0
    LETTER: 1
    SMS: 2


class ClassificationType(enum.Enum):
    LEGAL_STATUS: 0
    INDUSTRY: 1
    GEOGRAPH: 2
    COLLECTION_EXERCISE: 3
    RU_REF: 4
    SURVEY_REF: 5
    ENROLMENT_STATUS: 6


class CommunicationTemplate(db.Model):
    __tableargs__ = {"schema": "templatesvc"}
    __tablename__ = 'template'

    id = db.Column(UUID, unique=True, primary_key=True)
    label = db.Column(db.Text)
    type = db.Column(db.Enum(CommunicationType))
    uri = db.Column(db.Text)
    classification = db.Column(JSONB)
    params = db.Column(JSONB)
