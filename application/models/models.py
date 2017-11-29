import enum

from ras_common_utils.ras_database.base import Base
from ras_common_utils.ras_database.guid import GUID
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql.json import JSONB


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


class CommunicationTemplate(Base):
    __tablename__ = 'template'

    id = Column(GUID, unique=True, primary_key=True)
    label = Column(Text)
    type = Column(Enum(CommunicationType))
    uri = Column(Text)
    classification = Column(JSONB)
    params = Column(JSONB)

