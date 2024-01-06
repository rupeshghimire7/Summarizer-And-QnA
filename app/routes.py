from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from app import app, db, bcrypt, login_manager
from app.models import User, Context

# ... (previous routes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated and current_user.username == 'admin':
        users = User.query.all()
        contexts = Context.query.all()
        return render_template('admin.html', users=users, contexts=contexts)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))