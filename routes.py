from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, BookForm, BorrowForm
from app.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data)
        db.session.add(book)
        db.session.commit()
        flash('Your book has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('book.html', title='New Book', form=form)

@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow_book():
    form = BorrowForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if book and not book.user_id:
            book.user_id = current_user.id
            db.session.commit()
            flash('You have borrowed the book!', 'success')
        else:
            flash('Book not available or invalid ID', 'danger')
    return render_template('borrow.html', title='Borrow Book', form=form)
