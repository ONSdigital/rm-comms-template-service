from enum import IntEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Text, Column, Enum

Base = declarative_base()


class CommunicationType(IntEnum):
    EMAIL = 0
    LETTER = 1
    SMS = 2


class CommunicationTemplate(Base):
    __tablename__ = 'template'

    id = Column(UUID, unique=True, primary_key=True)
    label = Column(Text)
    type = Column(Enum(CommunicationType))
    uri = Column(Text)
    classification = Column(JSONB)
    params = Column(JSONB)

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": CommunicationType(self.type).name,
            "uri": self.uri,
            "classification": self.classification,
            "params": self.params
        }
