from flask import Blueprint, render_template, redirect, url_for, abort, flash, session, g
from flask.ext.login import login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from app import app, models, db
from app.forms import user as user_forms
from app.toolbox import email

# Serializer for generating random tokens
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Create a user blueprint
userbp = Blueprint('userbp', __name__, url_prefix='/user')

@userbp.route('/all', methods=['GET'])
def all_users():
    users = models.User.query.all()
    return render_template('user/profile.html', users=users, title="Users")

@userbp.route('/signup', methods=['GET', 'POST'])
def signup():
    # See if user is already logged in
    if 'email' in session:
        return redirect('/')

    form = user_forms.SignUp()
    if form.validate_on_submit():
        print("Creating user...")
        # Create a user who hasn't validated his email address
        user = models.User(
            email=form.email.data,
            payout_address=form.payout_address.data,
            wallet_seed=form.wallet_seed.data,
            password=form.password.data,
        )

        # Insert the user in the database
        db.session.add(user)
        db.session.commit()

        # Subject of the confirmation email
        # subject = 'Welcome to ZeroHouseEdge'
        # Generate a random token
        # token = ts.dumps(user.email, salt='email-confirm-key')
        # Render an HTML template to send by email
        # html = render_template('email/welcome.html')
        # Send the email to user
        # email.send(user.email, subject, html)
        # Log in user
        login_user(user)

        session['email'] = form.email.data
        return redirect(url_for('lobby'))
    return render_template('user/signup.html', form=form, title='Register')

@userbp.route('/signin', methods=['GET', 'POST'])
def signin():
    # See if user is already logged in
    if 'email' in session:
        return redirect('/')

    form = user_forms.Login()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        # Check the user exists
        if user is not None:
            # Check if the password is correct
            if user.check_password(form.password.data):
                # Log the user in and send them to the lobby
                login_user(user)
                session['email'] = form.email.data

                return redirect(url_for('lobby'))
            else:
                return redirect(url_for('userbp.signin'))
        else:
            return redirect(url_for('userbp.signin'))
    return render_template('user/signin.html', form=form, title='Sign in')

@userbp.route('/signout')
def signout():
    session.pop('email', None)
    logout_user()
    return redirect(url_for('lobby'))

@userbp.route('/profile')
def profile():
    if 'email' not in session:
        return redirect('/')
    user = models.User.query.filter_by(email=session['email']).first()
    return render_template('user/profile.html', wallet_seed=user.wallet_seed)
