import hashlib
from datetime import datetime



class UserService:

    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def create(self, name, email, password, connection):
        created_at = datetime.today()
        self.dbcursor.execute(f"INSERT INTO `users`(`usr_name`, `usr_email`, `usr_encrypted_password`, `usr_created_at`) VALUES ('{name}','{email}','{password}','{created_at}')")
        connection.commit()

    def list_users(self):
        self.dbcursor.execute("SELECT usr_id,usr_name, usr_email, usr_created_at FROM `users`;")
        return self.dbcursor.fetchall()

    def get_user_by_id(self,usr_id):
        self.dbcursor.execute(f"SELECT * FROM users WHERE usr_id = {usr_id}")
        return self.dbcursor.fetchall()[0]

    def update_user(self, name, email, user_id, connection, password_form):
        if password_form == 0:
            self.dbcursor.execute(f"UPDATE `users` SET `usr_name` = '{name}', `usr_email` = '{email}' WHERE `users`.`usr_id` = {user_id};")
            connection.commit()
        else:
            self.dbcursor.execute(f"UPDATE `users` SET `usr_name` = '{name}',`usr_email` = '{email}' ,`usr_encrypted_password` = '{password_form}' WHERE `users`.`usr_id` = {user_id};")
            connection.commit()

    def delete_user(self, user_id, connection):
        self.dbcursor.execute(f"DELETE FROM users WHERE users.usr_id = {user_id}")
        connection.commit()

    def user_exist(self, email, password):
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        self.dbcursor.execute(f"SELECT usr_id,usr_name, usr_email, usr_created_at, usr_encrypted_password FROM users WHERE usr_email = '{email}' AND (usr_encrypted_password = '{password}' OR usr_encrypted_password = '{encrypted_password}')")
        try:
            user = self.dbcursor.fetchall()[0]
            return user
        except Exception:
            return False


