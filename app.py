import secrets
import os
from flask import Flask, render_template, redirect, request, session, url_for, flash,jsonify
from pymongo import MongoClient
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin,current_user
from bson import ObjectId
import cgi



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
adminl = db['admin']
booking = db['bookings']

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username):
        self.username = username
    def get_id(self):
        return str(self.username)    

# Load user from database
@login_manager.user_loader
def load_user(username):
    a = adminl.find_one({'username': username})
    if a:
        return User(a['username'])
    
    user_data = users.find_one({'username': username})
    if user_data:
        return User(user_data['username'])
    else:
        return None
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        

        if users.find_one({'username': username}):
            flash('Username already taken. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        new_user = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': password,
            'mobile': mobile
        }
        users.insert_one(new_user)
        flash('Signup successful. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        a = adminl.find_one({'username':username,
                             'password':password
                             })
        
        if a:
            print('login successful')
            user = User(a['username'])
            login_user(user)
            print(user)
            return redirect(url_for('admin'))
        
        user_data = users.find_one({'username': username, 'password': password})

        if user_data:
            user = User(user_data['username'])
            
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/',methods=['GET','POST'])
def first():
    return render_template('login.html')

@app.route('/index',methods=['GET','POST'])
def home():
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})

        movie_record = movies.find()
        print(movie_record)
        return render_template('index.html', movie_record=movie_record)

    return render_template('index.html')

@app.route('/seatbooking',methods=['GET','POST'])
def seatbooking():
    if current_user.is_authenticated:  # Check if the user is authenticated
        form = cgi.FieldStorage()
        movie_id = request.form['movie_id']
        print(movie_id)
        movie_details = movies.find_one({'movie_id':movie_id})
        
        print(movie_details)
        return render_template('seatbooking.html', movie_details=movie_details)

    return render_template('seatbooking.html')


@app.route('/bookings',methods=['GET','POST'])
def bookings():
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})

        selected_seats = request.form['selected_seats']
        movie_id = request.form['movie_id']
        
        bs1 = movies.find_one({'movie_id':movie_id})
        bs = bs1['booked_seats']
        ss = selected_seats.split(',')
        
        
        query = {'movie_id': movie_id}
        new_values = {'$set': {'booked_seats': ss+bs}}
        print(selected_seats.split(','))
        print(movie_id)
        movies.update_one(query, new_values)
                
        print(selected_seats,movie_id)
        
        movie_details = movies.find_one({'movie_id':movie_id})
        
        book = {
            'username':current_user.username,
            'movie_id':movie_id,
            'booked_seats':ss,
            'payment':'online',
            'total':len(ss)*bs1['ticket_price'],
            'show_date':movie_details['show_date'],
            'show_time':movie_details['show_time'],
            'screen':movie_details['screen'],
            'movie_name':movie_details['movie_name']
        }
        booking.insert_one(book)
        
        cus_bookings = booking.find({'username':current_user.username})
        cb = []
        for i in cus_bookings:
            cb.append(i)
        cb.reverse()
        return render_template('bookings.html',cb=cb)

    return render_template('bookings.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})

        user_details = users.find_one({'username':current_user.username})
        
        return render_template('profile.html', user_details=user_details)

    return render_template('profile.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})
        
        return render_template('admin.html')

    return render_template('admin.html')

@app.route('/addmovie',methods=['GET','POST'])
def addmovie():
    # print(current_user.username)
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})
        print('adminl')
        return render_template('addmovie.html')

    return render_template('addmovie.html')

@app.route('/successful',methods=['GET','POST'])
def successful():
    
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})
        movieId = request.form['movieId']
        movieName = request.form['movieName']
        movieDescription = request.form['movieDescription']
        screen = request.form['screen']
        showDate = request.form['showDate']
        showTime = request.form['showTime']
        ticketPrice = int(request.form['ticketPrice'])
        bookedSeats = []
        
        movie = {
            'movie_id':movieId,
            'movie_name':movieName,
            'movie_decription':movieDescription,
            'screen':screen,
            'show_date':showDate,
            'show_time':showTime,
            'ticket_price':ticketPrice,
            'booked_seats':bookedSeats
        }
        
        exist = movies.find_one({'movie_id':movieId})
        
        print(movie)
        
        if exist:
            flash('Movie id already exists.', 'error')
        else:
            movies.insert_one(movie)
            
        return render_template('successful.html')

    return render_template('successful.html')

@app.route('/searchmovie',methods=['GET','POST'])
def searchmovie():
    
    if current_user.is_authenticated:  # Check if the user is authenticated
        
        return render_template('searchmovie.html')

    return render_template('searchmovie.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if current_user.is_authenticated:  # Check if the user is authenticated
        movieId = request.form['movieId']
        movie_details = movies.find_one({'movie_id':movieId})
        if movie_details:
            
            return render_template('result.html',movie_details=movie_details)

    return render_template('nodata.html')

@app.route('/update',methods=['GET','POST'])
def update():
    
    if current_user.is_authenticated:  # Check if the user is authenticated
        
        return render_template('update.html')

    return render_template('update.html')

@app.route('/deletemovie',methods=['GET','POST'])
def deletemovie():
    
    if current_user.is_authenticated:  # Check if the user is authenticated
        movieId = request.form['movie_id']
        exist = movies.find_one({'movie_id':movieId})
        if exist:
            movies.delete_one({'movie_id':movieId})
            return render_template('deletemovie.html')

    return render_template('deletemovie.html')

@app.route('/successful2',methods=['GET','POST'])
def successful2():
    
    if current_user.is_authenticated:  # Check if the user is authenticated
        # user_data = users.find_one({'username': current_user.username})
        movieId = request.form['movieId']
        movieName = request.form['movieName']
        movieDescription = request.form['movieDescription']
        screen = request.form['screen']
        showDate = request.form['showDate']
        showTime = request.form['showTime']
        ticketPrice = int(request.form['ticketPrice'])
        bookedSeats = []
        
        movie = {
            'movie_id':movieId,
            'movie_name':movieName,
            'movie_decription':movieDescription,
            'screen':screen,
            'show_date':showDate,
            'show_time':showTime,
            'ticket_price':ticketPrice,
            'booked_seats':bookedSeats
        }
        
        exist = movies.find_one({'movie_id':movieId})
        
        print(movie)
        
        if exist:
            movies.update_one({'movie_id': movieId}, {"$set": movie})
            return render_template('successful2.html')
        else:
            return render_template('nodata.html')
            
        

    return render_template('nodata.html')


if __name__ =='__main__':
    app.run(debug=True,port=5001)