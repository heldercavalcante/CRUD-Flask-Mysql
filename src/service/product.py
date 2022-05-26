class ProductService:

    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def create(self, name, price, conection, category):
        sql = f"INSERT INTO `products` (`pro_category_id`, `pro_name`, `pro_price`) VALUES ('{category}', '{name}', '{price}');"
        self.dbcursor.execute(sql)
        conection.commit()

    def list_products(self):
        self.dbcursor.execute("SELECT pro_id, cat_id, cat_name, pro_name, pro_price FROM `products` JOIN categories ON categories.cat_id = products.pro_category_id;")
        #self.dbcursor.execute("SELECT * FROM `products`")
        return self.dbcursor.fetchall()

    def get_product_by_id(self, product_id):
        self.dbcursor.execute(f"SELECT * FROM `products` WHERE pro_id = {product_id}")
        return self.dbcursor.fetchall()[0]

    def update_product(self, name, price, product_id, conection):
        self.dbcursor.execute(f"UPDATE `products` SET `pro_name` = '{name}', `pro_price` = '{price}' WHERE `products`.`pro_id` = {product_id};")
        conection.commit()

    def del_product(self, product_id, conection):
        self.dbcursor.execute(f"DELETE FROM `products` WHERE `products`.`pro_id` = {product_id}")
        conection.commit()
