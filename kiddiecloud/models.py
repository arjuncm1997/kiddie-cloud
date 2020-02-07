from kiddiecloud import db, app, login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):

    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(80), nullable=False)
    image= db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Login('{self.username}', '{self.password}','{self.usertype}','{self.email}', '{self.image}')"

class Gallery(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    desc = db.Column(db.String(120), nullable=False)
    image= db.Column(db.String(20), nullable=True, default='default.jpg')


class AddChildRight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    crimesection = db.Column(db.String(200), nullable=False)
    childright = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class AddVaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    age = db.Column(db.String(200), nullable=False)
    vaccination = db.Column(db.String(200), nullable=False)
    

class AddHealthyDiet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    age = db.Column(db.String(200), nullable=False)
    food = db.Column(db.String(200), nullable=False)

class AddSchool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    school = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)

class AddBabyCare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    product = db.Column(db.String(200), nullable=False)
    usage = db.Column(db.String(200), nullable=False)
    location=db.Column(db.String(200), nullable=False)

class BookDoctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    doctorname = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200),nullable = False)

class AddTalent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(200), nullable=False)
    talent = db.Column(db.String(200), nullable=False)

class BookAdmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    school = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    std = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200))


class AddComplaints(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    complaint=db.Column(db.String(200),nullable=False)

class AddQuestions(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    question=db.Column(db.String(200),nullable=False)
    doctor = db.Column(db.String(200))
    replay = db.Column(db.String(200))
    status = db.Column(db.String(200))

class AddParenting(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    parentingtips=db.Column(db.String(200),nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    subject = db.Column(db.String(200))
    message = db.Column(db.String(230))
    usertype = db.Column(db.String(200))