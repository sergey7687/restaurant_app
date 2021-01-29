from flask import render_template, flash, redirect, url_for, session, request
from restapp.restaurant_data import Employee, Register, Guests, Orders
from passlib.hash import sha256_crypt
from functools import wraps
from restapp.stock import Stock
from restapp import app
from restapp import mysql

stock = Stock()
stock_item = Stock()

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('вы не зарегистрированы', 'danger')
            return redirect(url_for('login'))

    return wrap


# home page
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('home.html')


# add employee data page
@app.route('/add_employee', methods=['POST', 'GET'])
@is_logged_in
def add_employee():
    form = Employee(request.form)

    return render_template('add_emp.html', form=form)


# edit employee data page
@app.route('/edit_employee', methods=['POST', 'GET'])
@is_logged_in
def edit_employee():
    form = Employee(request.form)

    return render_template('edit_emp.html', form=form)


# add guest data page
@app.route('/add_guest', methods=['POST', 'GET'])
@is_logged_in
def add_guest():
    form = Guests(request.form)
    if request.method == 'POST' and form.validate():
        g_name = form.guest_f_name.data
        g_l_name = form.guest_l_name.data
        g_phone = form.guest_phone.data
        g_email = form.guest_email.data
        g_address = form.guest_address.data
        g_note = form.guest_note.data
        cur = mysql.connection.cursor()
        result = cur.execute(
            'INSERT INTO guests(guest_f_name, guest_l_name, guest_phone, guest_email, guest_address, guest_note)'
            'VALUES(%s, %s, %s, %s, %s, %s)', (g_name, g_l_name, g_phone, g_email, g_address, g_note))
        mysql.connection.commit()
        cur.close()
        flash('гость добавлен', 'success')
        return redirect(url_for('guest_table'))

    return render_template('add_guest.html', form=form)


# edit guest data page
@app.route('/edit_guest/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def edit_guest(id):
    form = Guests(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM guests WHERE guest_id = %s', [id])
    guest = cur.fetchone()
    form.guest_f_name.data = guest['guest_f_name']
    form.guest_l_name.data = guest['guest_l_name']
    form.guest_phone.data = guest['guest_phone']
    form.guest_email.data = guest['guest_email']
    form.guest_address.data = guest['guest_address']
    form.guest_note.data = guest['guest_note']

    return render_template('edit_guest.html', form=form, guest=guest)


# guest card
@app.route('/guest_card/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def guest_card(id):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM guests WHERE guest_id = %s', [id])
    guest = cur.fetchone()

    # print(guest['guest_id'])
    if result > 0:
        return render_template('guest_card.html', guest=guest)


# table guest data
@app.route('/guests', methods=['POST', 'GET'])
@is_logged_in
def guest_table():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM guests')
    guest = cur.fetchall()
    if result > 0:
        return render_template('guest_table.html', guests=guest)

    else:
        msg = 'Гость не найден'
        return render_template('guest_table.html', msg=msg)


# menu

@app.route('/menu', methods=['POST', 'GET'])
@is_logged_in
def menu():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM menu')
    menu = cur.fetchall()
    if result > 0:
        return render_template('menu.html', menu=menu)


# customer orders
@app.route('/orders', methods=['POST', 'GET'])
@is_logged_in
def orders():
    form = Orders(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute(
        'SELECT o.book_id, o.menu_pos, g.guest_f_name, g.guest_address, u.user_f_name, u.user_l_name FROM orders o INNER JOIN guests g ON g.guest_id = o.guest_id INNER JOIN users u ON u.user_id = o.executor_emp')
    orders = cur.fetchall()
    if result > 0:
        return render_template('orders.html', orders=orders)
    else:
        return render_template('orders.html')


@app.route('/item/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def add_item(id):
    if session['order'] == 1:
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM menu WHERE pos_id = %s', [id])
        menu = cur.fetchone()
        if result > 0:
            stock.add_pos(menu['pos_name'])
            s = stock.get_stock()
            menu_pos = ', '.join(s)
            return render_template('items.html', stock=menu_pos)


@app.route('/items', methods=['POST', 'GET'])
@is_logged_in
def items():
    if session['order'] == 1:
        s = stock.get_stock()
        menu_pos = ', '.join(s)
        flash(session['username'] + ' завершите заказ', 'danger')
        return render_template('items.html', stock=menu_pos)
    else:
        s = stock.get_stock()
        menu_pos = ', '.join(s)
        session['order'] = 1
        return render_template('items.html', stock=menu_pos)


@app.route('/add_order', methods=['POST', 'GET'])
@is_logged_in
def add_order():
    form = Orders(request.form)
    session['order'] = 1
    s = stock.get_stock()
    menu_pos = ', '.join(s)
    if request.method == 'POST' and form.validate():
        guest_name = form.order_name.data
        guest_address = form.order_address.data
        executor = session['username']
        cur = mysql.connection.cursor()
        result = cur.execute(
            'INSERT INTO orders(guest_id, menu_pos, executor_emp) VALUES ((SELECT guest_id FROM guests WHERE guest_f_name = %s and guest_address = %s), %s, (SELECT user_id FROM users WHERE username = %s))',
            (guest_name, guest_address, menu_pos, executor))
        mysql.connection.commit()
        cur.close()
        session['order'] = 0
        flash('заказ создан', 'success')
        stock.get_stock().clear()
        return redirect(url_for('orders'))
    return render_template('add_order.html', form=form, stock=menu_pos)


# register page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Register(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.user_f_name.data
        last_name = form.user_l_name.data
        username = form.username.data
        phone = form.user_phone.data
        email = form.user_email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO users(user_f_name, user_l_name, username, user_phone, user_email, password) VALUES(%s, %s, %s, %s, %s, %s)',
            (first_name, last_name, username, phone, email, password))
        mysql.connection.commit()
        cur.close()

        flash('вы зарегистрированы', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


# login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Register(request.form)
    if request.method == 'POST':
        username = form.username.data
        password_candidate = form.password.data
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM users WHERE username = %s', [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['order'] = 0
                flash(username + ' вы вошли в личный кабинет', 'success')
                return redirect(url_for('index', username=username))
            else:
                error = 'неверное имя пользователя'
                return render_template('login.html', error=error)
        else:
            error = 'пользователь не найден'
            return render_template('login.html', error=error)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('вы вышли из личного кабинета', 'success')
    return redirect(url_for('login'))


@app.route('/delete_guest/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def delete_guest(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM guests WHERE guest_id = %s', [id])
    mysql.connection.commit()
    cur.close()

    flash('Гость удален', 'success')
    return redirect(url_for('guest_table'))


@app.route('/delete_order/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def delete_order(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM orders WHERE book_id = %s', [id])
    mysql.connection.commit()
    cur.close()

    flash('Заказ удален', 'success')
    return redirect(url_for('orders'))


