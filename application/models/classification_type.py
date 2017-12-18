from application.utils.database import db


class ClassificationType(db.Model):
    __tablename__ = 'classificationtype'

    name = db.Column(db.Text, unique=True, primary_key=True)

    def to_dict(self):
        return self.name
