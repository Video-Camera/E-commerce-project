from flask import Flask, request, redirect, url_for, render_template, make_response

from DB_Controller import connect_to_db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('user_auth.html')


@app.route('/user_controller/', methods=['GET'])
def user_controller():
    return render_template('user_controller.html')


@app.route("/user_controller/create_new_user/", methods=['GET'])
def create_new_user_get():
    return render_template('create_new_user.html')


@app.route("/user_controller/create_new_user/", methods=['POST'])
def create_new_user_post():
    conn = connect_to_db()
    curr = conn.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    password_conformation = request.form.get('password_conformation')
    if password == password_conformation:
        sql = """INSERT INTO user (username, password) VALUES (?, ?)"""
        curr.execute(sql, (username, password))
        conn.commit()
        sql_to_redirect = """SELECT * FROM user WHERE username = ? AND password = ?"""
        curr.execute(sql_to_redirect, (username, password))
        conn.close()
        return redirect(url_for("log_in"))
    else:
        error_response = make_response(f'Invalid credentials')
        return error_response


@app.route("/user_controller/user_page/", methods=['GET'])
def show_user_page():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """SELECT * FROM user WHERE id = ?"""
    curr.execute(sql, (user_id,))
    found_user = curr.fetchone()
    return render_template('user_page.html', content=found_user)


@app.route('/user_controller/update_user/', methods=['GET'])
def edit_user_page_get():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """SELECT * FROM user WHERE id = ?"""
    curr.execute(sql, (user_id,))
    found_user = curr.fetchone()
    return render_template('edit_user.html', content=found_user)


@app.route('/user_controller/update_user/', methods=['POST'])
def edit_user_page_post():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    balance = request.form.get('balance')
    sql = """UPDATE user SET first_name = ?, last_name = ?, balance = ? WHERE id = ?"""
    curr.execute(sql, (first_name, last_name, balance, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_user_page', user_id=user_id))


@app.route('/user_controller/delete_user/', methods=['GET', 'POST'])
def delete_user_get():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """DELETE FROM user WHERE id = ?"""
    curr.execute(sql, (user_id,))
    conn.commit()
    return redirect(url_for('homepage'))


@app.route('/user_controller/view_all_users/', methods=['GET'])
def view_all_users():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT id, first_name, last_name FROM user"""
    curr.execute(sql)
    list_of_users = curr.fetchall()
    return render_template('view_all_users.html', content=list_of_users)


@app.route('/product_controller/', methods=['GET'])
def product_controller():
    return render_template('product_controller.html')


@app.route('/product_controller/create_category/', methods=['GET'])
def create_category_get():
    return render_template('create_category.html')


@app.route('/product_controller/create_category/', methods=['POST'])
def create_category_post():
    conn = connect_to_db()
    curr = conn.cursor()
    category_name = request.form.get('category_name')
    category_description = request.form.get('category_description')
    sql = """INSERT INTO category (name, description) VALUES (?, ?)"""
    curr.execute(sql, (category_name, category_description))
    conn.commit()
    conn.close()
    return render_template('product_controller.html')


@app.route('/product_controller/create_product/', methods=['GET'])
def create_product_get():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM category"""
    curr.execute(sql)
    list_of_categories = curr.fetchall()
    return render_template('create_product.html', content=list_of_categories)


@app.route('/product_controller/create_product/', methods=['POST'])
def create_product_post():
    conn = connect_to_db()
    curr = conn.cursor()
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    product_price = request.form.get('product_price')
    product_category = request.form.get('category_name')
    sql = """INSERT INTO product (name, description, price, category_id) VALUES (?, ?, ?, ?)"""
    curr.execute(sql, (product_name, product_description, product_price, product_category))
    conn.commit()
    conn.close()
    return render_template('product_controller.html')


@app.route('/product_controller/show_product/<int:product_id>', methods=['GET'])
def product_page_get(product_id):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM product WHERE id = ?"""
    curr.execute(sql, (product_id,))
    found_product = curr.fetchone()
    return render_template('product_page.html', content=found_product)


@app.route('/product_controller/show_all_products/', methods=["GET"])
def show_all_products():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM product"""
    curr.execute(sql)
    list_of_products = curr.fetchall()
    return render_template('show_all_products.html', content=list_of_products)


@app.route('/product_controller/update_product/<int:product_id>', methods=["GET"])
def update_product_get(product_id):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM product WHERE id = ?"""
    curr.execute(sql, (product_id,))
    found_product = curr.fetchone()
    return render_template('edit_product.html', content=found_product)


@app.route('/product_controller/update_product/<int:product_id>', methods=["POST"])
def update_product_post(product_id):
    conn = connect_to_db()
    curr = conn.cursor()
    updated_name = request.form.get('edit_name')
    updated_price = request.form.get('edit_price')
    updated_description = request.form.get('edit_description')
    sql = """UPDATE product SET name = ?, price = ?, description = ? WHERE id = ?"""
    curr.execute(sql, (updated_name, updated_price, updated_description, product_id))
    conn.commit()
    conn.close()
    return redirect(url_for('product_controller'))


@app.route('/product_controller/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """DELETE FROM product WHERE id = ?"""
    curr.execute(sql, (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('product_controller'))


@app.route('/product_controller/show_all_categories/', methods=['GET'])
def show_all_categories():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM category"""
    curr.execute(sql)
    list_of_categories = curr.fetchall()
    return render_template('show_all_categories.html', content=list_of_categories)


@app.route('/product_controller/show_category/<int:category_id>/', methods=['GET'])
def show_category(category_id):
    conn = connect_to_db()
    curr = conn.cursor()
    sql_query_products_category = """SELECT * FROM product WHERE category_id = ?"""
    curr.execute(sql_query_products_category, (category_id,))
    list_of_products_to_category = curr.fetchall()
    sql_query_found_category = """SELECT * FROM category WHERE id = ?"""
    curr.execute(sql_query_found_category, (category_id,))
    found_category = curr.fetchone()
    return render_template('show_category.html', content=found_category, list_of_products=list_of_products_to_category)


@app.route('/shop_user_select/', methods=['GET'])
def shop_user_select_get():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM user"""
    curr.execute(sql)
    list_of_users = curr.fetchall()
    return render_template('shop_user_select.html', content=list_of_users)


@app.route('/shop_user_select/', methods=['POST'])
def shop_user_select_post():
    conn = connect_to_db()
    curr = conn.cursor()
    selected_user = request.form.get('user_select')
    sql = """SELECT * FROM user WHERE id = ?"""
    curr.execute(sql, (selected_user,))
    found_user = curr.fetchone()
    resp = make_response(render_template('shop_main.html', content=found_user))
    resp.set_cookie('userid', f'{found_user[0]}')
    return resp


@app.route('/product_controller/shop_all_products/', methods=['GET'])
def shop_all_products_get():
    conn = connect_to_db()
    curr = conn.cursor()
    sql = """SELECT * FROM product"""
    curr.execute(sql)
    list_of_products = curr.fetchall()
    return render_template('shop_all_products.html', content=list_of_products)


@app.route('/product_controller/shop_all_products/add_product/<int:product_id>', methods=['POST'])
# Adding a product from shop_all_products_get endpoint
def add_product_to_cart(product_id):
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql_product_query = """SELECT * FROM product WHERE id = ?"""
    curr.execute(sql_product_query, (product_id, ))
    found_product = curr.fetchone()
    sql_add_to_cart = """INSERT INTO cart (cart_user_id, cart_product_id, total_value) VALUES (?, ?, ?)"""
    curr.execute(sql_add_to_cart, (user_id, found_product[0], found_product[3]))
    conn.commit()
    conn.close()
    return render_template('shop_main.html')


@app.route('/user_controller/update_current_user/', methods=['GET'])
def update_current_user():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """SELECT * FROM user WHERE id = ?"""
    curr.execute(sql, (user_id, ))
    found_user = curr.fetchone()
    return render_template('user_page.html', content=found_user)


@app.route('/product_controller/view_cart/', methods=['GET'])
def view_cart():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """SELECT product.id, product.name, product.price FROM cart
            INNER JOIN product ON cart.cart_product_id = product.id
             WHERE cart.cart_user_id = ?"""
    curr.execute(sql, (user_id, ))
    cart_data = curr.fetchall()
    total_price_of_a_cart = 0
    for product in cart_data:
        total_price_of_a_cart += product[2]
    return render_template('view_cart.html', content=cart_data, total_value=total_price_of_a_cart)


@app.route('/product_controller/view_cart/', methods=['POST'])
def check_out():
    conn = connect_to_db()
    curr = conn.cursor()
    user_id = request.cookies.get('userid')
    sql = """SELECT product.id, product.name, product.price FROM cart
            INNER JOIN product ON cart.cart_product_id = product.id
             WHERE cart.cart_user_id = ?"""
    curr.execute(sql, (user_id, ))
    list_of_products_in_cart = curr.fetchall()
    total_price_of_a_cart = 0
    for product in list_of_products_in_cart:
        total_price_of_a_cart += product[2]
    sql_user_search = """SELECT * FROM user WHERE id = ?"""
    curr.execute(sql_user_search, (user_id, ))
    found_user = curr.fetchone()
    error_resp = make_response(f"Your balance is less than required!")
    if found_user[3] is None or found_user[3] < total_price_of_a_cart:
        return error_resp
    elif found_user[3] > total_price_of_a_cart:
        balance_after_cart = found_user[3] - total_price_of_a_cart
        update_user_balance = """UPDATE user SET balance = ? WHERE id = ?"""
        curr.execute(update_user_balance, (balance_after_cart, user_id))
        for item in list_of_products_in_cart:
            sql = """INSERT INTO orders (order_user_id, order_product_id, total_value) VALUES (?, ?, ?)"""
            curr.execute(sql, (user_id, item[0], item[2]))
            sql_to_delete_item_from_cart = """DELETE FROM cart WHERE cart_product_id = ?"""
            curr.execute(sql_to_delete_item_from_cart, (item[0], ))

        conn.commit()
        conn.close()
    return render_template('shop_main.html')


@app.route('/product_controller/delete_item_from_cart/<int:item_id>', methods=['POST'])
def delete_item_from_cart(item_id):
    conn = connect_to_db()
    curr = conn.cursor()
    sql_query = """DELETE FROM cart WHERE cart_product_id = ?"""
    curr.execute(sql_query, (item_id, ))
    conn.commit()
    return redirect(url_for('check_out'))


@app.route('/login/', methods=["GET"])
def log_in_get():
    return render_template('user_auth.html')


@app.route('/login/', methods=['POST'])
def log_in():
    conn = connect_to_db()
    curr = conn.cursor()
    requested_username = request.form.get('username')
    requested_password = request.form.get('password')
    sql_query_search_user = """SELECT * FROM user WHERE username = ? AND password = ?"""
    curr.execute(sql_query_search_user, (requested_username, requested_password))
    found_user = curr.fetchone()
    if found_user:
        resp = make_response(render_template('shop_main.html'))
        resp.set_cookie('userid', f'{found_user[0]}')
        return resp
    else:
        resp = make_response("User credentials don't match")
        return resp


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    # app.run()  # run app
