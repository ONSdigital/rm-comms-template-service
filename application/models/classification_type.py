from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Column

Base = declarative_base()

class ClassificationType(Base):
    __tablename__ = 'classificationtype'

    name = Column(Text, unique=True, primary_key=True)

    def to_dict(self):
        return self.name
