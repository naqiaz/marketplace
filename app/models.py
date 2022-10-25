import jwt
from datetime import datetime
from app import db, login_manager
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func
from time import time
from app import app

@login_manager.user_loader
def load_user(id):
    if 'account_type' in session:
        if session['account_type'] == 'User':
            return User.query.get(int(id))
        if session['account_type'] == 'Company':
            return Company.query.get(int(id))
        else:
            return None
    else:
        return None

class Person(db.Model):
   __abstract__ = True
   username = db.Column(db.String(64),index=True,unique=True)
   email = db.Column(db.String(120),index=True,unique=True)
   zipcode = db.Column(db.String(64),index=True)
   password_hash = db.Column(db.String(128))
   image_file = db.Column(db.String(20),nullable=False,default='default.jpg')

   def set_password(self, password):
       self.password_hash = generate_password_hash(password)
    
   def check_password(self, password):
       return check_password_hash(self.password_hash, password)

   @staticmethod
   def verify_token(token): 
        try:
            id = jwt.decode(token,app.config['SECRET_KEY'],
                algorithms=['HS256'])['id']
            type = jwt.decode(token,app.config['SECRET_KEY'],
                algorithms=['HS256'])['type']
        except:
            return
        if type == 'User':
            return User.query.filter_by(id=id).first()
        else:
            return Company.query.filter_by(id=id).first()
   
class User(Person, UserMixin):
   __tablename__ = 'user'
   id = db.Column(db.Integer,primary_key=True)
   type = db.Column(db.String(64), nullable=False, default='User')
   email_me = db.Column(db.Boolean,unique=False,default=True)
   tags = db.relationship('Tag',secondary='user_tag')

   def __repr__(self):
       return '<Username: {}>'.format(self.username)
   
   def set_tags(self,tag):
       self.tags.append(tag)

   def companies(self):
       CompTags = CompanyTag.query.join(UserTag,(CompanyTag.tag_id == UserTag.tag_id)).filter(UserTag.user_id == self.id).subquery()
       return Company.query.join(CompTags,(Company.id == CompTags.c.company_id)).order_by('name')
   
   def get_token(self, expires_in=600):
       return jwt.encode({'id':self.id, 'exp':time()+expires_in, 'type':self.type},
                         app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')

class Company(Person, UserMixin):
    __tablename__ = 'company'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(64), nullable=False, default='Company')
    name = db.Column(db.String(64),index=True, unique=True)
    website = db.Column(db.String(100),unique=True)
    tags = db.relationship('Tag',secondary='company_tag')
    promotions = db.relationship('Promotion',backref='company_promos',lazy=True,uselist=True, cascade='all,delete-orphan')
   
    def __repr__(self):
        return '<Company Name: {}>'.format(self.name)
    
    def set_tags(self,tag):
       self.tags.append(tag)

    def get_token(self, expires_in=600):
       return jwt.encode({'id':self.id, 'exp':time()+expires_in, 'type':self.type},
                         app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')

class Promotion(db.Model):
    __tablename__ = 'promotion'
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(120),nullable=False)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'))
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)

    def __repr__(self):
        return '<Promo: {}>'.format(self.id)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),index=True,unique=True)
    users = db.relationship('User',secondary='user_tag')
    companies = db.relationship('Company',secondary='company_tag')
    
    def __repr__(self):
       return '<Tag: {}>'.format(self.name)

class UserTag(db.Model):
    __tablename__ = 'user_tag'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key = True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'),primary_key = True)
    
    def __repr__(self):
        return '<User_Id: {}> <Tag_Id: {}>'.format(self.user_id,self.tag_id)

class CompanyTag(db.Model):
    __tablename__ = 'company_tag'
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'),primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'),primary_key = True)
    
    def __repr__(self):
        return '<Company_Id: {}> <Tag_Id: {}>'.format(self.company_id, self.tag_id)

causes =  ['Women-Owned','Black-Owned']

db.create_all()
for cause in causes:
    t = Tag.query.filter_by(name=cause).first()
    if t is None:
        t = Tag(name=cause)
        db.session.add(t)
db.session.commit






    
    
  
   


