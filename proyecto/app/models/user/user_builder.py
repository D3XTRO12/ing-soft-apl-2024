from .user_model import User
class UserBuilder:
    def __init__(self, username):
        self.user = User()
        self.user.username = username


    def build(self):
        return self.user