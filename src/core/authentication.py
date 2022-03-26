class Authentication:
    
    def __init__(self,session) -> None:
        self.session = session
    
    def is_logged(self):
         return 'user' in self.session
     
    def get_user(self):
        self._check_user_logged(self)
        return self.session["user"]
    
    def get_user_name(self):
        self._check_user_logged(self)
        return self.session["user"]["name"]
    
    def get_user_email(self):
        self._check_user_logged(self)
        return self.session["user"]["email"]
    
    def _check_user_logged(self):
        if not self.is_logged:
            raise Exception("user not logged")