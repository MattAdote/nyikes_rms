# system imports
import datetime

# local imports
from app import db

class BaseModel(db.Model):
    """Contains properties shared across all the models"""

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    createdOn = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    createdBy = db.Column(db.String(75))
    lastModifiedOn = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    lastModifiedBy = db.Column(db.String(75))
    # date_modified = db.Column(
    #     db.DateTime, default=db.func.current_timestamp(),
    #     onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserModel(db.Model):
    """
        Base class for "User" objects of the RMS
        Contains properties applicable to all User objects
    """

    __abstract__ = True

    public_id = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150), nullable=True)
    lastLoggedIn = db.Column(db.DateTime, default="2000-Jan-01 01:01:01", nullable=False)
    lastLoggedOut = db.Column(db.DateTime, default="2000-Jan-01 01:01:01", nullable=False)