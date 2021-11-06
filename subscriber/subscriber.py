#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import mysql.connector
import tweepy
import smtplib
import requests
import random
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cse586DS@gmail.com'
app.config['MAIL_PASSWORD'] = 'cse586Distributed'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

auth = tweepy.OAuthHandler('AC7WkBbTptQM1F9vPvaWMnPu0',
                           '6Kv4MuuLHX3FvB0PxNLZaa1ajyIIrnGqVQriBvmYzGD8u2fD3O'
                           )
auth.set_access_token('1433835629763338242-SMviK8BJ5FcBnrrYBj9CMWIoDRX8Uu'
                      , '8hcho5OJ03WadpgMjfEgvUhzX3sOJ3DNWoIvOAyqc0sdc')
api = tweepy.API(auth, wait_on_rate_limit=True)

global_sub_count=1
broker_list = [6001,6002,6003]



""" Method to select which publisher a new user wants to subscribe"""
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        return render_template('subscribe.html')



""" Get method displays the current subscribers and their subscribed topic which is redirected from the main page (index.html)
Post method is called when a subscriber subscribes or unsubscribes to a topic and in order to display the success message, we redirect 
it to the subscriber details page that is the same page retrieved by the Get method.
"""
@app.route('/subscriptions', methods = ['GET', 'POST'])
def subscriptions():
    if request.method == 'GET': # Subscriber details page
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
        connection = mysql.connector.connect(**config)
        cur = connection.cursor()
        cur.execute('Select * from subscriptions')
        data = cur.fetchall()
        ll = []
        for i in data:
            dt={}
            dt['name']= i[1]
            dt['email']= i[2]
            dt['topic']= i[3]
            dt['broker_port'] = i[4]
            ll.append(dt)
        connection.commit()

        cur.close()

        return render_template('subscriptions.html',data = ll)

    if request.method == 'POST': # called when a subscriber successfully subscribes or unsubscribes to a topic
        sub = request.form.get('subunsub')
        name = request.form.get('name')
        email = request.form.get('email')
        topic = request.form.get('subscribe')
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
        connection = mysql.connector.connect(**config)
        cur = connection.cursor()
        x = 0
        if sub == 'Subscribe': # name or email both are checked for subscribing or redirected to an error page
            if name is None or email is None or email =='' or name=='':
                return render_template('errorpage.html',data = "Error: Enter both email and name to subscribe")

            random.shuffle(broker_list)
            port_number = broker_list[0]

            if port_number == 6001:
                res = requests.get('http://broker1:6001/subber', params={'name':name,'email':email,'topic':topic,'port_number':port_number})
            if port_number == 6002:
                res = requests.get('http://broker2:6002/subber', params={'name':name,'email':email,'topic':topic,'port_number':port_number})
            if port_number == 6003:
                res = requests.get('http://broker3:6003/subber', params={'name':name,'email':email,'topic':topic,'port_number':port_number})


        if sub == 'UnSubscribe': # atleast email is required to unsubscribe and the email should be valid or redirected to error page
            if email is None or email =='':
                return render_template('errorpage.html',data = "Error: Enter email to unsubscribe")
            cur.execute('SELECT * FROM subscriptions WHERE email= %s AND topic=%s',(email,topic))
            isExist = cur.fetchall()
            if not isExist:
                return render_template('errorpage.html',data = "Error: email address does not exist in database or is not subscribed for the selected topic")
            else:
                for i in isExist:
                    port_ = i[4]
                if port_ == 6001:
                    res = requests.get('http://broker1:6001/unsub', params={'email':email,'topic':topic})
                if port_ == 6002:
                    res = requests.get('http://broker2:6002/unsub', params={'email':email,'topic':topic})
                if port_ == 6003:
                    res = requests.get('http://broker3:6003/unsub', params={'email':email,'topic':topic})

        connection.commit()

        cur.close()

        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
        connection = mysql.connector.connect(**config)
        cur = connection.cursor()
        cur.execute('Select * from subscriptions')
        data = cur.fetchall()
        ll = []
        for i in data:
            dt={}
            dt['name']= i[1]
            dt['email']= i[2]
            dt['topic']= i[3]
            dt['broker_port'] = i[4]
            ll.append(dt)
        connection.commit()

        cur.close()

        return render_template('subscriptions.html',data = ll)

"""
Index.html - Main Page
"""
@app.route('/')
def index():
    # config = {'user': 'root','password': 'root','host': 'db','port': '3306','database': 'htest'}
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5050, debug = True)
