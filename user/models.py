from mongoengine import signals

from application import db
from utilities.common import uts_now_ts as now


class User(db.Document):
    '''
    Adding User model on top of
    MongoDb.
    The Definition of fields are as follows:
    '''
    username = db.StringField(db_field='u', required=True, unique=True)
    password = db.StringField(db_field='p', required=True)
    email = db.StringField(db_field='e', required=True, unique=True)
    first_name = db.StringField(db_field='fn', max_length=50)
    last_name = db.StringField(db_field='ln', max_length=50)
    created = db.IntField(db_field='c', default=now)
    bio = db.StringField(db_field='b', max_length=160)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.username = document.username.lower()
        document.email = document.email.lower()

    '''
    Creating Index for the User Model.
    the minus(-) in front of created index
    means the created index is sorted descending. 
    '''
    meta = {
        'indexes': ['username', 'email', '-created']
    }

signals.pre_save.connect(User.pre_save, sender=User)