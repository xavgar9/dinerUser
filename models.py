from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class DinerUser(UserMixin):
    def __init__(self, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password, is_admin=False):
        self.id = numDocument
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
    def __str__(self):
        tmp=str(self.id)+","+str(self.firstName)+","+str(self.userName)+","+str(self.email)+","+str(self.password)
        return tmp
    def data(self):
        tmp=str(self.id)+","+str(self.firstName)+","+str(self.userName)+","+str(self.email)+","+str(self.password)
        return tmp
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return True
    def __repr__(self):
        return '<User {}>'.format(self.email)
    def get_id(self):
        tmp=self.id
        tmp=tmp.decode("utf-8")
        return tmp
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def is_active(self):
        return True




##### PROVISIONAL
users = []
def getUser(firstName, secondName, lastName, telephone, email,password):
    """
    buscar la password en base de datos
    password=SQL
    """
    user=DinerUser("45454", firstName, secondName, lastName, 0, 0, telephone, 0, email, 0, password, False)
    """
    for user in users:
        if user.email == email:
            return user
    """
    return user