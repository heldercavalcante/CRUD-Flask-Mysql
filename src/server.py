from crypt import methods
from flask import Flask, render_template, request, redirect,url_for
import mysql.connector
from service.category import CategoryService
from service.product import ProductService
from service.category import CategoryService


db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password='12345',
    database="store"
)

mycursor = db_connection.cursor()
product_service = ProductService(mycursor)
category_service = CategoryService(mycursor)

app = Flask(__name__)

#HOME PAGE
@app.route("/")
def home_page():
    return render_template("products/home_page.html")

#PRODUCT PAGE
@app.route("/products")
def product_page():
    return render_template("products/product_page.html")

@app.route("/products/list")
def list_products_page():
    products = product_service.list_products()
    return render_template('products/list_products.html', products=products)

@app.route("/products/new")
def new_products_page():
    categories = category_service.list_categories()
    return render_template('products/new_product.html', categories=categories)

@app.route("/products/create",methods=['POST'])
def create_products():
    product_service.create(request.form["name"],request.form["price"],db_connection,request.form["category"])
    return redirect(url_for('list_products_page'))

@app.route("/products/edit/<product_id>")
def edit_products_page(product_id):
    product = product_service.get_product_by_id(product_id)
    categories = category_service.list_categories()
    return render_template('products/edit_product.html',product=product, categories=categories)

@app.route("/products/update/<product_id>",methods=['POST'])
def update_products(product_id):
    product_service.update_product(request.form["name"],request.form["price"],product_id, db_connection)
    return redirect(url_for('list_products_page'))

@app.route("/products/delete/<product_id>")
def delete_products(product_id):
    product_service.del_product(product_id,db_connection)
    return redirect(url_for('list_products_page'))

#CATEGORY PAGE
@app.route("/categories")
def categories_page():
    return render_template('/categories/category_page.html')

@app.route("/categories/list")
def categories_list():
    categories = category_service.list_categories()
    return render_template("/categories/list_categories.html", categories = categories)

@app.route("/categories/new")
def new_category_page():
    return render_template("/categories/new_category.html")

@app.route("/categories/create", methods=['POST'])
def create_category():
    category_service.create(request.form["name"],db_connection)
    return redirect(url_for('categories_list'))

@app.route("/categories/edit/<category_id>")
def edit_category_page(category_id):
    category = category_service.get_category_by_id(category_id)
    return render_template("/categories/edit_category.html", category = category)

@app.route("/categories/update/<category_id>", methods=["POST"])
def uptade_category(category_id):
    category_service.update_category(db_connection, request.form["name"], category_id)
    return redirect(url_for('categories_list'))

@app.route("/categories/delete/<category_id>")
def delete_category(category_id):
    category_service.delete_category(db_connection, category_id)
    return redirect(url_for('categories_list'))

app.run(host='localhost', port=8080, debug=True)


mycursor.close()
db_connection.close()