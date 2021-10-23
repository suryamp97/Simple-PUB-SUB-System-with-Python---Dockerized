#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import mysql.connector
import tweepy
import smtplib
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
        cur.execute('SELECT email FROM subscriptions WHERE topic = %s',(topic,))
        emailids = cur.fetchall()
        print(type(emailids))
        print(emailids)
        connection.commit()
        cur.close()

        # send mail (notify) to all the topic's subscribers
        for email in set(emailids):
            msg = Message('New update published by '+topic,sender = 'cse586DS@gmail.com', recipients = list(email))
            msg.body = topic + " has posted a new update: "+ "\n " + str(data[0])
            mail.send(msg)
        return render_template('publish_posts.html', data = data)


""" Method to select which publisher wishes to publish"""
@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        return render_template('publish.html')
    return render_template('index.html')

""" Method to select which publisher a new user wants to subscribe"""
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        return render_template('subscribe.html')

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

        # query to retrieve email-ids of current non-subscribers of the publisher's topic
        cur.execute('SELECT email from subscriptions where email NOT IN (SELECT email FROM subscriptions WHERE topic = %s) ',(topic,))
        emailids = cur.fetchall()
        print(type(emailids))
        print(emailids)
        connection.commit()
        cur.close()

        # send advertising/de-advertising mails to retrieved email-ids from above query
        for email in set(emailids):
            msg = Message(sub,sender = 'cse586DS@gmail.com', recipients = list(email))
            msg.body = topic + " has posted a new update: "+ "\n " + mes
            mail.send(msg)
        return render_template('errorpage.html', data ="Notifications successfully sent")

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
            cur.execute('INSERT INTO subscriptions(subid, sname, email, topic) VALUES (%s, %s,%s,%s)',
                    (x, name, email, topic))
        if sub == 'UnSubscribe': # atleast email is required to unsubscribe and the email should be valid or redirected to error page
            if email is None or email =='':
                return render_template('errorpage.html',data = "Error: Enter email to unsubscribe")
            cur.execute('SELECT * FROM subscriptions WHERE email= %s AND topic=%s',(email,topic))
            isExist = cur.fetchall()
            if not isExist:
                return render_template('errorpage.html',data = "Error: email address does not exist in database or is not subscribed for the selected topic")
            else:
                cur.execute('DELETE FROM subscriptions WHERE email =%s AND topic=%s',(email,topic))
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
    app.run(host='0.0.0.0')
