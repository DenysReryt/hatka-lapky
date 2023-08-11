import time
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import join_room, leave_room, send, SocketIO

from models import db, migrate
from wtform import *
from config import settings
import crud

# Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# Set up the SQLAlchemy connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)

# Configure flask login
login = LoginManager(app)
login.init_app(app)   

@login.user_loader
def load_admin(id):    
    return crud.AdminModel.query.get(id)

# Initialize Flask-SocketIO
socketio = SocketIO(app, manage_session=False)  

def update_rooms_list():
    global ROOMS
    ROOMS = []
    for user in crud.get_all_users():
        if user.active is True:
            ROOMS.append(f'{user.first_name} (@{user.username})')
        elif user.active is False and f'{user.first_name} (@{user.username})' in ROOMS:
                ROOMS.remove(f'{user.first_name} (@{user.username})')


@app.route('/registration', methods=['GET', 'POST'])
def index():
    
    reg_form = RegistrationForm()
    
    # Updated database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        
        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)
        
        # Add admin`s username & hashed password to DB
        admin = crud.create_admin(username=username, password=hashed_pswd)
        if admin is False:
            return render_template('404.html')
        
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
        
    
    return render_template('index.html', form=reg_form)


@app.route('/', methods=['GET', 'POST'])
def login():
    
    login_form = LoginForm()
    
    # Allow login if validation success
    if login_form.validate_on_submit():
        admin_obj = crud.get_admin(username=login_form.username.data)
        login_user(admin_obj)
        return redirect(url_for('chat'))
    
    return render_template('login.html', form=login_form)


@app.route('/logout', methods=['GET'])
def logout():
    
    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    
    update_rooms_list()
    
    return render_template("chat.html", username=current_user.username, rooms=ROOMS)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


last_message = None

@socketio.on('incoming-msg')
def on_message(data):
    """ Broadcast messages """
    global last_message
    msg = data['msg']
    username = data['username']
    room = data['room']
    
    # Set timestamp
    time_stamp = time.strftime('%b-%d %H:%M', time.localtime())
    
    send({'username': username, 'msg': msg, 'time_stamp': time_stamp}, room=room)

    if msg:
        last_message = msg
        

@socketio.on('join')
def on_join(data):
    """ User joins a room """
    
    username = data["username"]
    room = data["room"]
    join_room(room)
    
    # Broadcast that new user has joined
    send({'msg': f'{username} has joined the {room} room.'}, room=room)


@socketio.on('leave')
def on_leave(data):
    """ User leaves a room """
    
    username = data['username']
    room = data['room']    
    leave_room(room)
    
    # Broadcast that user has left the room
    send({'msg': f'{username} has left the room'}, room=room)


if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', debug=True)
    