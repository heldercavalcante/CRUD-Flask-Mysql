from itertools import product


class ProductService:

    def __init__(self,dbcursor):
        self.dbcursor = dbcursor


    def create(self,name,price,conection):
        sql = f"INSERT INTO `products` (`id`, `name`, `price`) VALUES (NULL, '{name}', '{price}');"
        self.dbcursor.execute(sql)
        conection.commit()

    def list_products(self):
        self.dbcursor.execute("SELECT * FROM `products`")
        return self.dbcursor.fetchall()

    def get_product_by_id(self, product_id):
        self.dbcursor.execute(f"SELECT * FROM `products` WHERE id = {product_id}")
        return self.dbcursor.fetchall()[0]

    def update_product(self, name, price, product_id, conection):
        self.dbcursor.execute(f"UPDATE `products` SET `name` = '{name}', `price` = '{price}' WHERE `products`.`id` = {product_id};")
        conection.commit()

    def del_product(self, product_id, conection):
        self.dbcursor.execute(f"DELETE FROM `products` WHERE `products`.`id` = {product_id}")
        conection.commit()