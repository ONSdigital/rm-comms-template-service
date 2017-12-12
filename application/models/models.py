from enum import IntEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.json import JSONB
from application.utils.database import db


class CommunicationType(IntEnum):
    EMAIL = 0
    LETTER = 1
    SMS = 2


class CommunicationTemplate(db.Model):
    __tablename__ = 'template'

    id = db.Column(UUID, unique=True, primary_key=True)
    label = db.Column(db.Text)
    type = db.Column(db.Enum(CommunicationType))
    uri = db.Column(db.Text)
    classification = db.Column(JSONB)
    params = db.Column(JSONB)

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": CommunicationType(self.type).name,
            "uri": self.uri,
            "classification": self.classification,
            "params": self.params
        }
