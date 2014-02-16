import datetime
from flask import url_for
from LeagueMgr import db

class League(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    participants = db.ListField(db.EmbeddedDocumentField('Participant'))

class Participant(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    slug = db.StringField(max_length=255, required=True)
    name = db.StringField(max_length=255, required=True)
