from crypt import methods
from flask import Flask, render_template, request, redirect,url_for, session, flash
import mysql.connector
from service.authentication import Authentication
from service.category import CategoryService
from service.product import ProductService
from service.usres import UserService
import hashlib


db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password='12345',
    database="store"
)

mycursor = db_connection.cursor()
product_service = ProductService(mycursor)
category_service = CategoryService(mycursor)
users_service = UserService(mycursor)
auth = Authentication(session)

app = Flask(__name__)
app.secret_key = 'secretkey'



#login
@app.route('/')
def index():
    username = ''
    if 'user' in session:
        username = session['user'][1]
    return render_template('/login/index.html', username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = users_service.list_users()

    if request.method == 'POST' and request.form['email'] != '':
        email = request.form['email']
        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        for user in users:
            if email in user and encrypted_password in user:
                session['user'] = user
                return redirect(url_for('index'))
        flash('email or password invalid')
    return render_template('/login/login.html')


@app.route('/logout')
def logout():
    print(session.items())
    session.pop('user', None)
    return redirect(url_for('index'))


#PRODUCT PAGE

@app.route("/products/list")
def list_products_page():
    products = product_service.list_products()
    if auth.is_logged():
        return render_template('products/list_products.html', products=products)
    return redirect(url_for('login'))

@app.route("/products/new")
def new_products_page():
    categories = category_service.list_categories()
    if auth.is_logged():
        return render_template('products/new_product.html', categories=categories)
    return redirect(url_for('login'))


@app.route("/products/create",methods=['POST'])
def create_products():
    product_service.create(request.form["name"],request.form["price"],db_connection,request.form["category"])
    return redirect(url_for('list_products_page'))


@app.route("/products/edit/<product_id>")
def edit_products_page(product_id):
    product = product_service.get_product_by_id(product_id)
    categories = category_service.list_categories()
    if auth.is_logged():
        return render_template('products/edit_product.html',product=product, categories=categories)
    return redirect(url_for('login'))

@app.route("/products/update/<product_id>",methods=['POST'])
def update_products(product_id):
    product_service.update_product(request.form["name"],request.form["price"],product_id, db_connection)
    return redirect(url_for('list_products_page'))

@app.route("/products/delete/<product_id>")
def delete_products(product_id):
    product_service.del_product(product_id,db_connection)
    return redirect(url_for('list_products_page'))

#CATEGORY PAGE


@app.route("/categories/list")
def categories_list():
    categories = category_service.list_categories()
    if auth.is_logged():
        return render_template("/categories/list_categories.html", categories = categories)
    return redirect(url_for('login'))

@app.route("/categories/new")
def new_category_page():
    if auth.is_logged():
        return render_template("/categories/new_category.html")
    return redirect(url_for('login'))


@app.route("/categories/create", methods=['POST'])
def create_category():
    category_service.create(request.form["name"], db_connection)
    return redirect(url_for('categories_list'))


@app.route("/categories/edit/<category_id>")
def edit_category_page(category_id):
    category = category_service.get_category_by_id(category_id)
    if auth.is_logged():
        return render_template("/categories/edit_category.html", category = category)
    return redirect(url_for('login'))


@app.route("/categories/update/<category_id>", methods=["POST"])
def uptade_category(category_id):
    category_service.update_category(db_connection, request.form["name"], category_id)
    return redirect(url_for('categories_list'))


@app.route("/categories/delete/<category_id>")
def delete_category(category_id):
    category_service.delete_category(db_connection, category_id)
    return redirect(url_for('categories_list'))

#USERS PAGE

@app.route("/users/new")
def new_user_page():
    if auth.is_logged():
        return render_template("/users/new_user.html")
    return redirect(url_for('login'))


@app.route("/users/create", methods=["POST"])
def create_user():
    form_password = request.form['password']
    new_password = hashlib.sha256(form_password.encode()).hexdigest()
    print(new_password)
    print(type(new_password))
    users_service.create(request.form["name"], request.form["email"],
           new_password, request.form["datetime"], db_connection)
    if auth.is_logged():
        return redirect(url_for("users_list"))
    return redirect(url_for('login'))

@app.route("/users/list")
def users_list():
    users = users_service.list_users()
    if auth.is_logged():
        return render_template("/users/list_users.html", users=users)
    return redirect(url_for('login'))


@app.route("/users/edit/<user_id>")
def edit_user_page(user_id):
    user = users_service.get_user_by_id(user_id)
    if auth.is_logged():
        return render_template("/users/edit_user.html", user=user)
    return redirect(url_for('login'))


@app.route("/user/update/<user_id>", methods=["POST"])
def update_user(user_id):
    pass_form = request.form['password']
    if len(pass_form) == 0: 
        new_pass_form = 0
        print('cima')
    else:
        new_pass_form = hashlib.sha256(pass_form.encode()).hexdigest()
        print('baixo')
    print(f'aqui1: {new_pass_form}')
    users_service.update_user(request.form['name'], request.form['email'], user_id, db_connection, new_pass_form)
    return redirect(url_for("users_list"))


@app.route("/user/delete/<user_id>")
def delete_user(user_id):
    users_service.delete_user(user_id, db_connection)
    return redirect(url_for("users_list"))


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)


mycursor.close()
db_connection.close()
