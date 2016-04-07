from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, Email, ValidationError, EqualTo
from app.models import User

class Unique(object):

    '''
    Custom validator to check an object's attribute
    is unique. For example users should not be able
    to create an account if the account's email
    address is already in the database. This class
    supposes you are using SQLAlchemy to query the
    database.
    '''

    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class SignUp(Form):

    ''' User sign up form. '''

    payout_address = TextField(validators=[Required()],
                     description='Payout Address')
    email = TextField(validators=[Required(), Email(),
                                  Unique(User, User.email,
                                         'This email address is ' +
                                         'already linked to an account.')],
                      description='Email')
    password = PasswordField(validators=[
        Required(), Length(min=6),
        EqualTo('confirm', message='Passwords must match.')
    ], description='Password')
    confirm = PasswordField(description='Confirm password')

class Login(Form):

    ''' User login form. '''

    email = TextField(validators=[Required(), Email()],
                      description='Email')
    password = PasswordField(validators=[Required()],
                             description='Password')
