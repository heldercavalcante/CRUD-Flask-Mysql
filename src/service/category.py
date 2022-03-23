class CategoryService:

    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def create(self, name, conection):
        self.dbcursor.execute(f"INSERT INTO categories (cat_name) VALUES ('{name}');")
        conection.commit()

    def list_categories(self):
        self.dbcursor.execute("SELECT * FROM categories;")
        return self.dbcursor.fetchall()

    def get_category_by_id(self, category_id):
        self.dbcursor.execute(f"SELECT * FROM categories WHERE cat_id = {category_id}")
        return self.dbcursor.fetchall()[0]

    def update_category(self, conection, name, category_id):
        self.dbcursor.execute(f"UPDATE categories SET cat_name = '{name}' WHERE categories.cat_id = {category_id};")
        conection.commit()

    def delete_category(self, conection, category_id):
        self.dbcursor.execute(f"DELETE FROM categories WHERE categories.cat_id = {category_id}")
        conection.commit()