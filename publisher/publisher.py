#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import mysql.connector
import tweepy
import smtplib
import requests
from flask_mail import Mail, Message
import json


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

"""
This method is used to notify subscribers of their subscribed topics by emailing the latest tweet on those topics
once the publisher chooses to publish
"""
@app.route('/notfiy', methods=['GET', 'POST'])
def notfiy():
    if request.method == 'POST':
        topic = request.form.get('publish') # the publisher of the topic who wish to publish

        tweets = []
        c = 0
        tws = api.user_timeline(screen_name = topic, count =1 ) # twitter API that retrieves the latest tweet by the publisher
        data = []
        for t in tws:
            data.append(t.text)
        
        print(str(topic))
        if (str(topic) == "Rainbow6Game" or str(topic) == "watchdogsgame" or str(topic) == "GhostRecon"):
            eids = requests.get('http://broker1:6001/get_subs', params={'topic':topic})
        if (str(topic) == "ForHonorGame" or str(topic) == "justdancegame" or str(topic) == "TheDivisionGame"):
            eids = requests.get('http://broker2:6002/get_subs', params={'topic':topic})
        if (str(topic) == "TheCrewGame" or str(topic) == "FarCrygame" or str(topic) == "assassinscreed"):
            eids = requests.get('http://broker3:6003/get_subs', params={'topic':topic})

        elids = eids.json()['ids']
        emailids = []
        for i in elids:
            emailids.append(i[0])
        # send mail (notify) to all the topic's subscribers
        for email in set(emailids):
            tmp=[]
            tmp.append(email)
            msg = Message('New update published by '+topic,sender = 'cse586DS@gmail.com', recipients = tmp)
            msg.body = topic + " has posted a new update: "+ "\n " + str(data[0])
            mail.send(msg)
        return render_template('publish_posts.html', data = data)


""" Method to select which publisher wishes to publish"""
@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        return render_template('publish.html')
    return render_template('index.html')



""" Method for publishers to select their topic to advertise or de-advertise their topic"""
@app.route('/ads', methods=['GET', 'POST'])
def ads():
    if request.method == 'POST':
        return render_template('ads.html')

""" 
Method that sends advertisement and de-advertisement mails to current non-subscribers
in the database who are subscribed to other topics except the advertising publisher's topic
"""
@app.route('/mail_success', methods=['GET', 'POST'])
def mail_success():
    if request.method == 'POST':
        topic = request.form.get('subscribe') # publisher who wish to advertise their topic
        addeadd = request.form.get('addead') # select whether the publisher chose to advertise or de-advertise
        mes = ''
        sub=''
        if addeadd== 'ad':
            mes = 'Subscribe to '+ topic + ' for more Amazing offers and updates!!! '
            sub = 'Offers by '+topic + ' only for you'
        if addeadd == 'deadd':
            mes = 'Deeply regret to inform you that the offers on '+topic+ ' Subscriptions has ended'
            sub = 'Sorry to let you down -' +topic +' and Team' 

        # query to retrieve email-ids of current non-subscribers of the publisher's topic
        if (str(topic) == "Rainbow6Game" or str(topic) == "watchdogsgame" or str(topic) == "GhostRecon"):
            eids = requests.get('http://broker1:6001/send_ads', params={'topic':topic})
        if (str(topic) == "ForHonorGame" or str(topic) == "justdancegame" or str(topic) == "TheDivisionGame"):
            eids = requests.get('http://broker2:6002/send_ads', params={'topic':topic})
        if (str(topic) == "TheCrewGame" or str(topic) == "FarCrygame" or str(topic) == "assassinscreed"):
            eids = requests.get('http://broker3:6003/send_ads', params={'topic':topic})

        elids = eids.json()['ids']
        emailids = []
        for i in elids:
            emailids.append(i[0])

        # send advertising/de-advertising mails to retrieved email-ids from above query
        for email in set(emailids):
            tmp=[]
            tmp.append(email)
            msg = Message(sub,sender = 'cse586DS@gmail.com', recipients = tmp)
            msg.body = topic + " has posted a new update: "+ "\n " + mes
            mail.send(msg)
        return render_template('errorpage.html', data ="Notifications successfully sent")


"""
Index.html - Main Page
"""
@app.route('/')
def index():
    # config = {'user': 'root','password': 'root','host': 'db','port': '3306','database': 'htest'}
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000, debug = True)
