# -*- coding: utf-8 -*-
from app import db
import datetime

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(36))
    text = db.Column(db.String(36), default = '')
    copies = db.Column(db.Integer, default = 1)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    pairs = db.relationship('Pair', backref = 'photo', lazy = 'dynamic')

    def __repr__(self):
        return '<Photo id = {0}, \
user_id = {1}, \
filename = {2}, \
text = {3}, \
copies = {4}, \
timestamp = {5}>'.format(self.id, self.user_id, self.filename.encode('utf-8'), self.text.encode('utf-8'), str(self.copies), str(self.timestamp))

class Pair(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    def __repr__(self):
        return '<Pair order_id = {0}, photo_id = {1}>'.format(str(self.order_id), str(self.photo_id))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(50))
    UserPhone = db.Column(db.String(36))
    UserAddress = db.Column(db.String(500))
    UserComment = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    pairs = db.relationship('Pair', backref = 'order', lazy = 'dynamic')

    def __repr__(self):
        return '<Order id = {0}, \
UserName = {1}, \
UserPhone = {2}, \
UserAddress = {3}, \
UserComment = {4}, \
timestamp = {5}>'.format(str(self.id), self.UserName.encode('utf-8'), self.UserPhone.encode('utf-8'), self.UserAddress.encode('utf-8'), self.UserComment.encode('utf-8'), str(self.timestamp))
