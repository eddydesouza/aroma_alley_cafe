from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import json

# App and DB setup
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Login manager setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models (imported after db is initialized)
from models import User, MenuItem, Order

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class CheckoutForm(FlaskForm):
    submit = SubmitField('Place Order')

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    items = MenuItem.query.all()
    return render_template('menu.html', items=items)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        cart_data = request.form.get('cart')
        session['cart'] = json.loads(cart_data) if cart_data else []
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    cart = session.get('cart', [])
    if form.validate_on_submit():
        total = sum(item['price'] * item['quantity'] for item in cart)
        order = Order(user_id=current_user.id, total=total, status='Pending')
        db.session.add(order)
        db.session.commit()
        session['cart'] = []
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('checkout.html', form=form, cart=cart)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists', 'error')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    orders = Order.query.all()
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        status = request.form.get('status')
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            flash('Order status updated', 'success')
    return render_template('admin.html', orders=orders)

@app.route('/api/menu', methods=['GET'])
def api_menu():
    items = MenuItem.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'price': float(item.price)} for item in items])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='Page not found'), 404

if __name__ == '__main__':
    app.run(debug=True)
