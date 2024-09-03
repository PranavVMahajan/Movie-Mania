import secrets
import os
from flask import Flask, render_template, redirect, request, session, url_for, flash,jsonify
from pymongo import MongoClient
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin,current_user
from bson import ObjectId

app = Flask(__name__)

#sdfshh
# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key securely from environment variable or fallback to a default value
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secret_key)

client = MongoClient('mongodb://localhost:27017/')
db = client['MovieMania']
movies = db['movies']
users = db['users']

login_manager = LoginManager()
login_manager.init_app(app)
db = client['MyHealth_Hero']
users_collection = db['users']
users_community = db['users_community']
appointments_collection = db['appointments_collection']
goals_collection = db['goals']
users_mental_data = db['users_mental_data']
mental_question_collection = db['mental_question']
goals_done = db['goals_done']

username = 'prath123'
user_data = None
user = username
questions = mental_question_collection.find()
user = username
questions = mental_question_collection.find()
print('hello')
print(username)
user_answers = users_mental_data.find({'user_data':username}) 
# if user_answers != None:
    # explanation = user_answers['explanation']
    # stressed = predictor(user_answers['explanation'])
    # user_answers = user_answers['08042024'] 
    # user_data1 = {
    # 'questions' : questions,
    # 'answers': user_answers,
    # # 'explanation': explanation,
    # 'user_data' : user
    # }
temp = None
for i in user_answers:
    temp = i
print(temp)
print(temp['explanation'])

for i in range(0,20):
    print(temp['08042024'].pop(0))