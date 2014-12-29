#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: harmoN
# @Date:   2014-12-21 23:07:24
# @Last Modified by:   harmoN
# @Last Modified time: 2014-12-29 18:36:23
from datetime import datetime
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import config
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(128))
    create_date = db.Column(db.DateTime)
    colour = db.Column(db.String(10))
    is_activeactive = db.Column(db.Boolean, default=True, unique=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


import base_flask.views
