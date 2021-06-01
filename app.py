# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Dragon
# CreatDate: 2020/12/29 14:27
import string
import urllib
import hashlib
import time
import urllib.request
from importlib import reload
from urllib.parse import quote
import math
from flask import Flask, render_template, request, flash, session, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from common.request_yapi import Request_Yapi
import requests, re, sys
import pymysql
pymysql.install_as_MySQLdb()
reload(sys)
import pytest


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Test@1234@10.39.39.13:3306/nx_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config["SQLALCHEMY_ECHO"] = False
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = 'longlong'
url_for = '127.0.0.1:5000'

'''
users表模型
'''
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.INTEGER,primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String())
    phone = db.Column(db.String())
    adress = db.Column(db.String())
    sex = db.Column(db.String())
    status = db.Column(db.INTEGER)
    is_delete = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME())
    email = db.Column(db.String())
'''
apicase表模型
'''
class Apicase(db.Model):
    __tablename__ = 'api_case'
    api_id = db.Column(db.INTEGER,primary_key=True)
    api_name = db.Column(db.String())
    api_url = db.Column(db.String())
    api_url_json = db.Column(db.String())
    api_user_name = db.Column(db.String())
    api_status = db.Column(db.INTEGER())
    api_is_delete = db.Column(db.String())
    introduce = db.Column(db.String())
    scenic = db.Column(db.String())
    edition = db.Column(db.String())

'''
scenic表模型
'''

class Scenic(db.Model):
    __tablename__ = 'scenic'
    scenic_id = db.Column(db.INTEGER,primary_key=True)
    scenic_name = db.Column(db.String(16))

'''
session 检测，判断登陆
'''
@app.route('/auth',methods=['POST','GET'])
def auth(func):
    def inner(*args,**kwargs):
        if not session.get('user'):
            return redirect("/loginning")
        return func(*args,**kwargs)
    return inner

'''
首页
'''
@app.route('/',methods=['POST','GET'])
@auth
def index():
    return render_template('index.html',username = session.get('user'))

'''
登出
'''
@app.route('/loginout',methods=['POST','GET'])
def loginout():
    session.get('user')
    session.pop('user')
    return redirect('/')

'''
处理登陆
'''
@app.route('/loginning',methods=['POST','GET'])
def loginning():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        print(password_md5)
        username_test = User.query.filter_by(username=username,password=password_md5).all()
        if username_test:
            for x in username_test:
                login_name = x.username
                login_id = x.user_id
                session['user']=login_name
                session['id'] = login_id
                return redirect('/')
        else:
            flash('密码错误')
            return render_template('login.html')
    else:
        return render_template('login.html')


'''
会员列表
'''
@app.route('/member_list',methods=['POST','GET'])
def member_list():
    user_datas = User.query.filter_by(is_delete=0).all()
    user_data = User.query.filter_by(is_delete=0).offset(0).limit(10).all()
    count_datas = len(user_datas)
    data_counts = len(user_datas) / 10
    data_count = int(math.ceil(data_counts))
    return render_template('member-list.html',user_data=user_data,data_count=data_count,count_datas=count_datas)

@app.route('/member_page',methods=['POST','GET'])
def member_page():
    page_start = request.args.get("id")
    num = int(page_start) * 10
    user_data = User.query.filter_by(is_delete=0).offset(int(num)).limit(10).all()
    user_datas = User.query.filter_by(is_delete=0).all()
    data_counts = len(user_datas)/10
    data_count = int(math.ceil(data_counts))
    return render_template('member-list.html',user_data=user_data,data_count=data_count)
'''
会员添加
'''
@app.route('/member_list_add',methods=['POST','GET'])
def member_list_add():
    print(request.method)
    if request.method == "POST":
        user_email = request.form.get('email')
        L_username = request.form.get('username')
        user_password = request.form.get('pass')
        password_md5 = hashlib.md5(user_password.encode(encoding='UTF-8')).hexdigest()
        user_insert = User(username = L_username,email = user_email,password = password_md5,adress='',sex='',status=1,phone='',is_delete=0,create_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        db.session.add(user_insert)
        db.session.commit()
        return redirect('/member_list')
    return render_template('member-list.html')
@app.route('/member_add',methods=['POST','GET'])
def member_add():
    return render_template('member-add.html')

'''
会员删除
'''
@app.route('/member_del',methods=['POST','GET'])
def member_del():
    ids = request.form.get('id')
    User.query.filter_by(user_id = ids).update({'is_delete':1})
    db.session.commit()
    return redirect('member_list')
'''
编辑页面，数据显示
'''
@app.route('/member_edit',methods=['POST','GET'])
def member_edit():
    id = request.form.get('id')
    if id:
        user_data = User.query.filter_by(user_id=id).all()
        for user_data in user_data:
            user_email = user_data.email
            user_name = user_data.username
            user_id = user_data.user_id
        dates = {'useremail':user_email,'username':user_name,'user_id':user_id}
        return dates
        return render_template('member-edit.html')
    else:

        return render_template('member-edit.html')

'''
用户修改
'''
@app.route('/member_update',methods=['POST','GET'])
def member_update():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('pass')
    id = request.form.get('idd')
    password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    user_update = User.query.filter_by(user_id=id).update({'email': email,'username':username,'password':password_md5,'phone':'','status':1,'create_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'sex':'男','adress':'','is_delete':0})
    db.session.commit()
    return render_template('member-list.html')


'''
自动化管理
'''
@app.route('/api_list',methods=['POST','GET'])
def api_list():
    api_data = Apicase.query.filter_by(api_is_delete=0).all()

    return render_template('api-list.html',api_data=api_data)

'''
add case
'''
@app.route('/api_add',methods=['POST','GET'])
def api_add():
    scenic_data = Scenic.query.all()
    return render_template('api-add.html',scenic_data=scenic_data)

@app.route('/api_add_do',methods=['POST','GET'])
def api_add_do():
    print(session['id'])
    api_name = request.form.get('username')
    api_url = request.form.get('url_name')
    url_json_name = request.form.get('url_json_name')
    api_introduce = request.form.get('api_introduce')
    api_scenic = request.form.get('api_scenic')
    api_edition = request.form.get('api_edition')
    api_user_id = session['id']
    api_datas = User.query.filter_by(user_id=api_user_id).all()
    for data in api_datas:
        username = data.username
    insert_api = Apicase(api_name = api_name,api_url=api_url,url_json_name=url_json_name,api_user_name=username,api_status=0,api_is_delete=0,introduce=api_introduce,scenic=api_scenic,edition=api_edition)
    db.session.add(insert_api)
    db.session.commit()
    return render_template('api-list.html')


@app.route('/api_del',methods=['POST','GET'])
def  api_del():
    id = request.form.get('id')
    Apicase.query.filter_by(api_id=id).update({'api_is_delete': 1})
    db.session.commit()
    return redirect('api_list')




@app.route('/test_report',methods=['POST','GET'])
def test_report():

    render_template('test-report.html')

'''
导出
'''
@app.route('/export_report',methods=['POST','GET'])
def export_report():
    url = request.form.get('url')
    name = request.form.get('name')
    url_q = quote(url, safe=string.printable)
    request_url = urllib.request.Request(url_q)
    response_data = urllib.request.urlopen(request_url)
    html = response_data.read()
    with open('./report'+ name + ".html","wb") as f:
        f.write(html)
    return render_template('api-list.html')
'''
全部执行
'''
@app.route('/full_implement',methods=['POST','GET'])
def full_implement():
    api_datas = Apicase.query.with_entities(Apicase.api_url,Apicase.api_name,Apicase.api_url_json).all()
    for x in api_datas:
        url_q = quote(x.api_url, safe=string.printable)
        request_url = urllib.request.Request(url_q)
        response_data = urllib.request.urlopen(request_url)
        html = response_data.read()
        with open('./report' + x.api_name + ".html", "wb") as f:
            f.write(html)
    return redirect('api_list')


'''
通过率计算
'''
@app.route('/pass_rate',methods=['POST','GET'])
def pass_rate():
    id =  request.args.get("id")
    if id:
        json_data = Apicase.query.filter_by(api_id = id).all()
        for ds in json_data:
            api_name = ds.api_name
        yapi_data = Request_Yapi.request_url_data(json_data)
        return render_template('api-report.html',yapi_data = yapi_data,api_name = api_name)
    else:
        return render_template('api-report.html')


'''
消息发送
'''
@app.route('/send_message',methods=['POST','GET'])
def send_message():

    return render_template('admin-cate.html')


@app.route('/admin_cate',methods=['POST','GET'])
def admin_cate():
    return render_template('admin-cate.html')



@app.route('/welcome',methods=['POST','GET'])
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':

    app.run(debug=True)
