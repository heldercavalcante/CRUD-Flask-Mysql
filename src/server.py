from crypt import methods
from flask import Flask, render_template, request, redirect,url_for
import mysql.connector
from service.product import ProductService


db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password='12345',
    database="store"
)

mycursor = db_connection.cursor()
product_service = ProductService(mycursor)

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("products/home_page.html")

@app.route("/products")
def list_products_page():
    products = product_service.list_products()
    return render_template('products/list_products.html', products=products)

@app.route("/products/new")
def new_products_page():
    return render_template('products/new_product.html')

@app.route("/products/create",methods=['POST'])
def create_products():
    product_service.create(request.form["name"],request.form["price"],db_connection)
    return redirect(url_for('list_products_page'))

@app.route("/products/edit/<product_id>")
def edit_products_page(product_id):
    product = product_service.get_product_by_id(product_id)
    return render_template('products/edit_product.html',product=product)

@app.route("/products/update/<product_id>",methods=['POST'])
def update_products(product_id):
    product_service.update_product(request.form["name"],request.form["price"],product_id, db_connection)
    return redirect(url_for('list_products_page'))

@app.route("/products/delete/<product_id>")
def delete_products(product_id):
    product_service.del_product(product_id,db_connection)
    return "<p>Product deleted</p> <a href='/products'>Product List</a>"


app.run(host='localhost', port=8080, debug=True)


mycursor.close()
db_connection.close()