# -*- coding: utf-8 -*-

from app import db, models

def addPhoto(filename, text='', copies=0):
    u = models.Photo(filename=filename, text=text, copies=copies)
    db.session.add(u)
    db.session.commit()

def getPhotos():
    return models.Photo.query.all()

def deletePhotos():
    for u in getPhotos():
        db.session.delete(u)
    db.session.commit()



def addOrder(UserName='', UserPhone='', UserAddress='', UserComment=''):
    u = models.Order(UserName=UserName, UserPhone=UserPhone, UserAddress=UserAddress, UserComment=UserComment)
    db.session.add(u)
    db.session.commit()

def getOrders():
    return models.Order.query.all()

def deleteOrders():
    for u in getOrders():
        db.session.delete(u)
    db.session.commit()


def addPair(order_id, photo_id):
    u = models.Pair(order_id=order_id, photo_id=photo_id)
    db.session.add(u)
    db.session.commit()

def getPairs():
    return models.Pair.query.all()

def deletePairs():
    for u in getPairs():
        db.session.delete(u)
    db.session.commit()


def deleteAll():
    deletePairs()
    deleteOrders()
    deletePhotos()

addPhoto(u'1.jpg', u'красотка', 3)
addPhoto(u'2.jpg', u'КРАСОТКА', 1)

addOrder(u'Аня', u'+79262100590', u'Дом', u'лооол')
addOrder(u'Глаша', u'+', u'Дофолвтам', u'ЫЫЫЫлооол')

addPair(1, 1)
addPair(2, 1)
addPair(2, 2)


print getPhotos()
print
print getOrders()
print

for pair in getPairs():
    print pair.order, pair.photo

for order in getOrders():
    print order.pairs.all()

for photo in getPhotos():
    print photo.pairs.all()


deleteAll()