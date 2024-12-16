import math

from flask import render_template, request, redirect, jsonify, session
import dao, utils
from app import app, login
from flask_login import login_user, logout_user
from app.models import UserRole


@app.route("/")
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)

    prods = dao.load_products(cate_id=cate_id, kw=kw, page=int(page))

    total = dao.count_products()
    page_size = app.config['PAGE_SIZE']
    return render_template("index.html", products=prods, pages=math.ceil(total/page_size), UserRole=UserRole)


@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            if(user.user_role != UserRole.ADMIN):
                return redirect('/')
            elif(user.user_role == UserRole.ADMIN):
                return redirect('/admin')

    return render_template('login.html',UserRole=UserRole)


@app.route('/login-admin', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user)

    return redirect('/admin')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def register_process():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']

            dao.add_user(avatar=request.files.get('avatar'), **data)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/carts', methods=['post'])
def add_to_cart():

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart


    return jsonify(utils.stats_cart(cart))

@app.route('/api/carts', methods=['delete'])
def remove_from_cart():
    data = request.json
    id = str(data.get('id'))

    cart = session.get('cart', {})

    if id in cart:
        del cart[id]
        session['cart'] = cart
        # total_quantity = sum(item['quantity'] for item in cart.values())
    return jsonify(utils.stats_cart(cart))

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    id = str(data.get('id'))

    cart = session.get('cart')


    cart[id]["quantity"] = data.get("quantity")
    session['cart'] = cart
    return jsonify(utils.stats_cart(cart))

@app.route('/cart')
def cart():
    return render_template('cart.html',UserRole = UserRole)

@app.route('/house',methods=['post','get'])
def house():
    return render_template('user_role/house.html',UserRole = UserRole)

@app.route('/seller',methods=['post','get'])
def seller():
    return render_template('user_role/seller.html',UserRole = UserRole)


@app.context_processor
def common_response():
    cart = session.get('cart')
    if cart is None:
        cart = {}
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.stats_cart(cart)
    }


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        from app import admin
        app.run(debug=True)

