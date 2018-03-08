#!/usr/bin/env bash

set -x # Echo everything
set -e # Exit on error

cat >> flask_app.py << flask_app
import os
import random


from flask import Flask
from flask import request, Response

app = Flask(__name__)
password_one = 'helloworld'
password_two = 'worldhello'
current_password = password_one
number_of_calls = 0

companies = ['EmailSpanner', 'Brandwatch', 'GoogleAnalytics', 'HootSuite', 'Radian6', 'HelloCustomer', 'MoneyMoney']

companies_pending_anonymization = {}

dates = [str(x) for x in list(range(20180201,20180228)) + list(range(20180301,20180309))]

for date in dates:
    companies_to_be_anonymized_today = ",".join(random.sample(companies,random.randint(0,len(companies))))
    companies_pending_anonymization[date] = {
      'companies_pending_anonymization' : f"[{companies_to_be_anonymized_today}]"
    }


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'etl_user' and password == current_password

@app.route('/pending_anonymization/<day>')
def companies_to_anonymize(day):
    global password_one
    global password_two
    global current_password
    global number_of_calls

    print(f'Current number of calls {number_of_calls} ')
    number_of_calls += 1
    auth = request.authorization
    if not auth or not check_auth(auth.username,auth.password):
      return Response("Not Authenticated!",401)
    if number_of_calls % 20 == 0:
      to_password_two()
    print(companies_pending_anonymization)
    print(day in companies_pending_anonymization)
    if day in companies_pending_anonymization:
      return str(companies_pending_anonymization[day])
    return str({'companies_pending_anonymization':[]})

@app.route('/password_one')
def to_password_one():
  global password_one
  global password_two
  global current_password
  global number_of_calls
  number_of_calls = 0
  current_password = password_one
  return 'Ok'

@app.route('/password_two')
def to_password_two():
  global password_one
  global password_two
  global current_password
  global number_of_calls
  number_of_calls = 0
  current_password = password_two
  return 'Ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

flask_app

exec python flask_app.py