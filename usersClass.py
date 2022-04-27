from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class user(UserMixin):          #heredamos de la clase UserMixin, perteneciente a Flask-login

    def __init__(self, name, password, permisosAdmin):
        self.name = name
        self.password = generate_password_hash(password)
        self.permisosAdmin = permisosAdmin

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)
