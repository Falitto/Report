from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from hashlib import md5
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orgnization = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    subdivision = db.Column(db.Integer, db.ForeignKey('subdivisions.id'))
    first_name = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    performer = db.Column(db.Boolean)
    appraiser = db.Column(db.Boolean)
    signer = db.Column(db.Boolean)  
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    controler = db.Column(db.Boolean)
    can_see_all_documents = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Field_type(db.Model):
    __tablename__='field_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Appraiser(db.Model):
    __tablename__='appraisers'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey('documents.id'))
    employee = db.Column(db.Integer, db.ForeignKey('users.id'))

class Signer(db.Model):
    __tablename__='signers'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey('documents.id'))
    employee = db.Column(db.Integer, db.ForeignKey('users.id'))

class Performer(db.Model):
    __tablename__='performers'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey('documents.id'))
    employee = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_info = db.relationship('User', backref='user_info')

class Controler(db.Model):
    __tablename__='controlers'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey('documents.id'))
    employee = db.Column(db.Integer, db.ForeignKey('users.id'))

class Document(db.Model):
    __tablename__='documents'
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    number = db.Column(db.String(25))
    customer = db.Column(db.String(150))
    the_total_cost = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    performers = db.relationship('Performer',  backref='performers')

class Document_field(db.Model):
    __tablename__='document_fields'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer, db.ForeignKey('documents.id'))
    name = db.Column(db.String(255))
    value = db.Column(db.Text)
    index = db.Column(db.Integer)
    alias = db.Column(db.String(255))
    template_field = db.Column(db.Integer, db.ForeignKey('template_fields.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    comment = db.Column(db.Text)
    field_type = db.Column(db.Integer, db.ForeignKey('field_types.id'))

class Organization(db.Model):
    __tablename__='organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    inn = db.Column(db.String(20))
    ogrn = db.Column(db.String(20))
    kpp = db.Column(db.String(20))

class Subdivision(db.Model):
    __tablename__='subdivisions'
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    name = db.Column(db.String(255))
    inn = db.Column(db.String(20))
    ogrn = db.Column(db.String(20))
    kpp = db.Column(db.String(20))
    address = db.Column(db.String(255))
    telephone = db.Column(db.String(255))
    show_telephones_together = db.Column(db.Boolean)
    email = db.Column(db.String(255))
    show_emails_together = db.Column(db.Boolean)
    site = db.Column(db.String(255))


class Template(db.Model):
    __tablename__='templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))

    def getStatus(self):
          return Status.query.filter(self.status == Status.id)

class Template_field(db.Model):
    __tablename__='template_fields'
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.Integer, db.ForeignKey('templates.id'))
    name = db.Column(db.String(255))
    value = db.Column(db.Text)
    alias = db.Column(db.String(255))
    index = db.Column(db.Integer)
    comment = db.Column(db.Text)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    field_type = db.Column(db.Integer, db.ForeignKey('field_types.id'))

class Group(db.Model):
    __tablename__='groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    comment = db.Column(db.Text)
    index = db.Column(db.Integer)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))

class Status(db.Model):
    __tablename__='statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    activate = db.Column(db.Boolean)
    

    def __repr__(self):
        return '<Status {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Docs(db.Model):
    __tablename__='docs'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    result = db.Column(db.Boolean)
