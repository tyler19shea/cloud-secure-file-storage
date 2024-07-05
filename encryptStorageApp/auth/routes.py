from flask import request, jsonify, redirect, url_for, render_template, flash
from . import auth_blueprint, db, bcrypt
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from encryptStorageApp.utils.logging import log_error

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        user = User.query.filter_by(username=username).first()
        if user:
            log_error('Registration failed due to Invalid Username.')
            flash(f'Username {username} already exists')
            return render_template('register.html')
        elif password1 != password2:
            log_error('Registration failed due to Invalid Passwords')
            flash('Passwords do not match')
            return render_template('register.html')
        elif len(password1) < 7:
            log_error('Registration failed due to Invalid Passwords')
            flash('Password is not long enough (must be longer than 7 characters)')
            return render_template('register.html')
        hashed_password = bcrypt.generate_password_hash(password1)
        try: 
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!')
            return render_template('/login.html', user=current_user)
        except Exception as e:
            log_error(f'Registration failed: {e}')
            flash('Registration failed. Please try again.')
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        #Check the password and log in the user
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Login successful!')
            log_error(f'Login successsful by user: {username}')
            return redirect(url_for('app.index'))
        else: 
            flash('Invalid credentials!')
            log_error(f'Login in failed by user: {username}')
            return render_template('login.html')
            # return redirect(url_for('auth.login'))
    return render_template('login.html', user=current_user)
    
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 
