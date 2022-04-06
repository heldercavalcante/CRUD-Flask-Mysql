class Authentication:
    def __init__(self, session):
        self.session = session

    def is_logged(self):
        return 'user' in self.session
