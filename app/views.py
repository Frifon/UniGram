# -*- coding: utf-8 -*-
from app import app

from flask import render_template, redirect, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy

import os
import uuid

from PIL import Image
from copy import deepcopy
from random import randint


def get_price(images):
    cnt = 0
    for image in images:
        cnt += image.cnt
    if cnt == 0:
        return 0
    elif cnt <= 4:
        return 100
    elif cnt <= 8:
        return 150
    elif cnt <= 20:
        return 350
    else:
        return cnt * 17


def get_ost(images):
    cnt = 0
    for image in images:
        cnt += image.cnt
    if cnt == 0:
        return 0
    elif cnt <= 4:
        return 4 - cnt
    elif cnt <= 8:
        return 8 - cnt
    elif cnt <= 20:
        return 20 - cnt
    else:
        return 0


def get_cnt(images):
    cnt = 0
    for image in images:
        cnt += image.cnt
    return cnt

class Img:
    def __init__(self, filename, count, text, cnt):
        self.filename = filename
        self.count = count
        self.text = text
        self.cnt = cnt

@app.route("/")
def landing():
    return render_template('index.html')

@app.route("/order")
def order():
    print (Base)
    sessionid = request.cookies.get('SSID')
    if sessionid is None or sessionid not in Base:
        print (sessionid)
        resp = make_response(render_template('order.html', price=0, ost=0, cnt=0))
        sessionid = str(uuid.uuid1())
        resp.set_cookie('SSID', sessionid)
        Base[sessionid] = []
        return resp
    else:
        resp = make_response(render_template('order.html', images=Base[sessionid][::-1], price=get_price(Base[sessionid]), ost=get_ost(Base[sessionid]), cnt=get_cnt(Base[sessionid])))
        resp.set_cookie('SSID', sessionid)
        return resp
    


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpeg', 'jpg', 'png']

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    sessionid = request.cookies.get('SSID')
    if request.method == 'POST' and not(sessionid is None or sessionid not in Base):
        file = request.files['image']
        if file and allowed_file(file.filename):
            print ('ok')
            
            text = request.form['desc'].encode('utf-8')
            x = int(float(request.form['x']))
            y = int(float(request.form['y']))
            w = int(float(request.form['w']))
            h = int(float(request.form['h']))
            width = int(float(request.form['coolwidth']))
            cnt = int(request.form['cnt'])
            print (cnt)
            cnt = max(0, cnt)
            print (cnt)
            if not text:
                text = '';
            
            print (width)

            file.filename = file.filename.encode('utf-8')

            filename = sessionid + str(uuid.uuid1()) + file.filename
            filename = filename.encode('utf-8')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            x = int(1. * x / width * im.size[0])
            w = int(1. * w / width * im.size[0])
            y = int(1. * y / (1. * width / im.size[0] * im.size[1]) * im.size[1])
            h = int(1. * h / (1. * width / im.size[0] * im.size[1]) * im.size[1])
            im = im.crop((x, y, x + w, y + h))
            print(x, y, w, h)
            im = im.resize((640, 640), Image.ANTIALIAS)
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Base[sessionid].append(Img(filename, 1, text, cnt))
            return redirect('/order')
        else:
            return redirect('/order')
    else:
        return redirect('/order')

@app.route('/getportfolio')
def getportfolio():
    sessionid = request.cookies.get('SSID')
    if sessionid is None or sessionid not in Base:
        return ''
    
    response =  '''
            <section id="portfolio" class="portfolio">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-10 col-lg-offset-1 text-center">
                '''
    if len(Base[sessionid]):
        response += '''
                            <a href="#makeorder" class="btn btn-lg btn-light">Оформить заказ</a>
                            <hr class="small">
                    '''
    response += '''
                            <div class="row">
                '''
    for im in Base[sessionid][::-1]:
        response += '''
                    <div class="col-md-4">
                        <div class="portfolio-item">
                            <div style="width:100%">
                            <div style="display: inline-block;">
                                <div class="photo">
                                    <div class="topBlock">
                                        <div class="photoBlock">
                                            <div class="photoQuantity">{0}</div>
                                            <img id="modalPhoto" name="{1}" src="/static/images/{1}">
                                        </div>
                                    </div>
                                    <div class="bottomBlock">
                                        <div class="textBlock">
                                            <div id="{1}" class="userBlock">{2}</div>
                                            <div class="labelBlock">PhotoCrossing.ru</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
                    '''.format(str(im.cnt), im.filename, im.text)
    response += '</div>'
    if len(Base[sessionid]):
        response += '''<p style="text-align:right">
                                    <a href="/deleteall" class="btn btn-sm btn-danger" target="hidden-del">Удалить все фотографии</a>
                                </p><IFRAME style="display:none" name="hidden-del" id="hidden-del"></IFRAME>  '''
    response += '''
                        </div>
                    </div>
                </div>
            </section>
        '''
    return response

@app.route("/getprice")
def getprice():
    sessionid = request.cookies.get('SSID')
    if sessionid is None or sessionid not in Base:
        return ''
    if not len(Base[sessionid]):
        return ''
    response = '''
            <h3>
                <div id="Price">
                    {0} руб.'''.format(str(get_price(Base[sessionid])))
    if len(Base[sessionid]):
        response += ' / ' + str(get_cnt(Base[sessionid])) + ''' фото
                </div>
            </h3>'''
    if get_ost(Base[sessionid]):
        response += '''
                <h6>
                    Мы можете заказать еще {0} фото по той же цене.
                </h6>
                    '''.format(str(get_ost(Base[sessionid])))
    return response

@app.route('/getminiportfolio')
def getminiportfolio():
    sessionid = request.cookies.get('SSID')
    if sessionid is None or sessionid not in Base:
        return ''
    response = '<br><br>'
    for im in Base[sessionid][::-1]:
        for i in range(im.cnt):
            response += '''
                <div class="col-md-4">
                <div class="portfolio-item">
                    <div class="photo_small">
                        <div class="topBlock">
                            <div class="photoBlock">
                                <img style="width:64px;height:auto;" src="static/images/{0}">
                            </div>
                        </div>
                        <div class="bottomBlock">
                            <div class="textBlock">
                                <div id="{0}" class="userBlock" style="color:black">{1}</div>
                                <div class="labelBlock">PhotoCrossing.ru</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            '''.format(im.filename, im.text)
    return response

@app.route("/makeorder", methods=['GET', 'POST'])
def makeorder():
    global ID
    sessionid = request.cookies.get('SSID')
    if request.method == 'POST' and sessionid is not None and sessionid in Base and len(Base[sessionid]):
        Name = request.form['OrderName'].encode('utf-8')
        Phone = request.form['OrderPhone'].encode('utf-8')
        Address = request.form['OrderAddress'].encode('utf-8')
        Comment = request.form['OrderComment'].encode('utf-8')
        print(Name, Phone, Address, Comment)
        ID += 1
        os.system('mkdir orders/' + str(ID - 1))
        f = open('orders/' + str(ID - 1) + '/description.txt', 'w')
        f.write(Name + '\n===\n')
        f.write(Phone + '\n===\n')
        f.write(Address + '\n===\n')
        f.write(Comment + '\n===\n')
        f.close()
        for image in Base[sessionid]:
            os.system('echo ' + str(image.cnt) + ' > orders/' + str(ID - 1) + '/' + image.filename + ".txt")
            os.system('echo "<' + str(image.text.encode('utf-8')) + '>" >> orders/' + str(ID - 1) + '/' + image.filename + ".txt")
            os.system('cp static/images/' + image.filename + ' orders/' + str(ID - 1) + '/')
        f = open('ID', 'w')
        f.write(str(ID))
        f.close()
        return redirect('/order')
    else:
        return redirect('/order')

@app.route("/deleteall")
def deleteall():
    sessionid = request.cookies.get('SSID')
    if not(sessionid is None or sessionid not in Base or len(Base[sessionid]) == 0):
        Base[sessionid] = []
        return redirect('/order')
    else:
        return redirect('/order')

@app.errorhandler(500)
def pageShit(error):
    return app.make_response(redirect('/'))

@app.errorhandler(404)
def pageNotFound(error):
    return app.make_response(redirect('/'))

@app.errorhandler(443)
def pageSomeAnotherShit(error):
    return app.make_response(redirect('/'))

