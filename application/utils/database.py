from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(schema="templatesvc")
db = SQLAlchemy(metadata=metadata)
