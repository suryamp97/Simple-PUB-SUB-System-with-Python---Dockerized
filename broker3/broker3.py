#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import mysql.connector
import requests

app = Flask(__name__)

@app.route('/send_ads')
def send_ads():
    topic = request.args.get('topic')
    print("from broker1 topic name: ",topic)
    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
    connection = mysql.connector.connect(**config)
    cur = connection.cursor()
    cur.execute('SELECT email from subscriptions where email NOT IN (SELECT email FROM subscriptions WHERE topic = %s AND port = %s) ',(topic,'6003'))
    emailids_from_6003 = cur.fetchall()

    _6001 = requests.get('http://broker1:6001/send_ads_broker', params={'topic':topic})
    emailids_from_6001 = _6001.json()['eid']
    _6002 = requests.get('http://broker2:6002/send_ads_broker', params={'topic':topic})
    emailids_from_6002 = _6002.json()['eid']

    emailids = emailids_from_6001 + emailids_from_6002 + emailids_from_6003
    print(type(emailids))
    connection.commit()
    cur.close()
    return jsonify({'ids':emailids} )

@app.route('/send_ads_broker')
def send_ads_broker():
    topic = request.args.get('topic')
    print("from broker topic name: ",topic)
    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
    connection = mysql.connector.connect(**config)
    cur = connection.cursor()
    cur.execute('SELECT email from subscriptions where email NOT IN (SELECT email FROM subscriptions WHERE topic = %s AND port = %s) ',(topic,'6003'))
    emailids_from_6003 = cur.fetchall()

    emailids = emailids_from_6003
    print(type(emailids))

    connection.commit()
    cur.close()
    return jsonify({'eid':emailids})


@app.route('/get_subs')
def get_subs():
    topic = request.args.get('topic')
    print("from broker3 topic name: ",topic)
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
    cur.execute('SELECT email FROM subscriptions WHERE topic = %s AND port = %s',(topic,'6003'))
    emailids_from_6003 = cur.fetchall()

    _6001 = requests.get('http://broker1:6001/get_eid', params={'topic':topic})
    emailids_from_6001 = _6001.json()['eid']
    _6002 = requests.get('http://broker2:6002/get_eid', params={'topic':topic})
    emailids_from_6002 = _6002.json()['eid']

    emailids = emailids_from_6001 + emailids_from_6002 + emailids_from_6003
    print(type(emailids))
    connection.commit()
    cur.close()
    return jsonify({'ids':emailids} )

@app.route('/get_eid')
def get_eid():
    topic = request.args.get('topic')
    print("from broker topic name: ",topic)
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
    cur.execute('SELECT email FROM subscriptions WHERE topic = %s AND port = %s',(topic,'6003'))
    emailids_from_6003 = cur.fetchall()

    emailids = emailids_from_6003 
    print(type(emailids))

    connection.commit()
    cur.close()
    return jsonify({'eid':emailids})

@app.route('/subber')
def subber():
    name = request.args.get('name')
    email = request.args.get('email')
    topic = request.args.get('topic')
    port_number = request.args.get('port_number')

    if (str(topic) == "Rainbow6Game" or str(topic) == "watchdogsgame" or str(topic) == "GhostRecon"):
        return requests.get('http://broker1:6001/sub', params={'name':name,'email':email,'topic':topic,'port_number':port_number})
    if (str(topic) == "ForHonorGame" or str(topic) == "justdancegame" or str(topic) == "TheDivisionGame"):
        return requests.get('http://broker2:6002/sub', params={'name':name,'email':email,'topic':topic,'port_number':port_number})

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
    cur.execute('INSERT INTO subscriptions(subid, sname, email, topic, port) VALUES (%s, %s,%s,%s,%s)',
                    (0, name, email, topic, port_number))

    connection.commit()
    cur.close()
    return jsonify({'dummy':0})

@app.route('/sub')
def sub():
    name = request.args.get('name')
    email = request.args.get('email')
    topic = request.args.get('topic')
    port_number = request.args.get('port_number')

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
    cur.execute('INSERT INTO subscriptions(subid, sname, email, topic, port) VALUES (%s, %s,%s,%s,%s)',
                    (0, name, email, topic, port_number))

    connection.commit()
    cur.close()
    return jsonify({'dummy':0})

@app.route('/unsub')
def unsub():
    email = request.args.get('email')
    topic = request.args.get('topic')

    if (str(topic) == "Rainbow6Game" or str(topic) == "watchdogsgame" or str(topic) == "GhostRecon"):
        return requests.get('http://broker1:6001/unsubber', params={'email':email,'topic':topic})
    if (str(topic) == "ForHonorGame" or str(topic) == "justdancegame" or str(topic) == "TheDivisionGame"):
        return requests.get('http://broker2:6002/unsubber', params={'email':email,'topic':topic})

    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
    connection = mysql.connector.connect(**config)
    cur = connection.cursor()
    cur.execute('DELETE FROM subscriptions WHERE email =%s AND topic=%s',(email,topic))
    connection.commit()
    cur.close()
    return jsonify({'dummy':0})

@app.route('/unsubber')
def unsubber():
    email = request.args.get('email')
    topic = request.args.get('topic')


    config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'database': 'test',
            'port':'3306'
            }
    connection = mysql.connector.connect(**config)
    cur = connection.cursor()
    cur.execute('DELETE FROM subscriptions WHERE email =%s AND topic=%s',(email,topic))
    connection.commit()
    cur.close()
    return jsonify({'dummy':0})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 6003, debug = True)
