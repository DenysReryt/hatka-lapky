from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256
import crud


def invalid_credentials(form, field):
    """ Username and password checker """
    
    username_entered = form.username.data
    password_entered = field.data
    
    # Check credentials is valid    
    admin_obj = crud.get_admin(username=username_entered)
    if admin_obj is None:
        raise ValidationError('Username or password is incorrect')
    
    # Check password in invalid
    elif not pbkdf2_sha256.verify(password_entered, admin_obj.password):
        raise ValidationError('Username or password is incorrect')


class RegistrationForm(FlaskForm):
    """ Registration form """
    
    username = StringField('username', 
                           validators=[InputRequired(message='Username requiered'), 
                           Length(min=4, max=25, message='Username must be between 4 and 25 characters')])
    
    password = PasswordField('password', 
                             validators=[InputRequired(message='Password requiered'), 
                             Length(min=4, max=25, message='Password must be between 4 and 25 characters')])
    
    confirm_pswd = PasswordField('confirm_pswd', 
                                 validators=[InputRequired(message='Password requiered'), 
                                 EqualTo('password', message='Password must match')])
    

class LoginForm(FlaskForm):
    """ Login form """
    
    username = StringField('username', validators=[InputRequired(message="Username required")])
    password = PasswordField('password', validators=[InputRequired(message='Password required'), invalid_credentials])        
