from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class DinerUser(UserMixin):
    def __init__(self, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password, is_admin=False):
        self.numDocument = numDocument
        self.firstName = firstName
        self.secondName = secondName
        self.firstLastName = firstLastName
        self.secondLastName = secondLastName
        self.address = address
        self.telephone = telephone
        self.payMethod = payMethod
        self.email = email
        self.userName = userName
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)

##### PROVISIONAL
users = []
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None