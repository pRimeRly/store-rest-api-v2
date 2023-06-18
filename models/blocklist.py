"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported
by the app and the logout resource so that tokens can be added to the blocklist when the
users log out.
"""

from db import db


class BlocklistModel(db.Model):
    __tablename__ = 'blocklist'

    id = db.Column(db.Integer, primary_key=True)
    blocklist = db.Column(db.String(255), nullable=False, unique=True)
