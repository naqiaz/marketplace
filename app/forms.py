import secrets, os
from app import app, photos, promos
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import MultipleFileField, SelectField, SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import URL, Optional, Length, ValidationError, Email, EqualTo, DataRequired
from flask_wtf.file import FileField,FileRequired, FileAllowed
from flask_login import current_user
from app.models import Person, User,Tag,Company
from PIL import Image

class LoginForm(FlaskForm):
    type = SelectField('Select Account Type',choices=[('User','User'),('Company','Company')],validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    zipcode = StringField('5 Digit Zipcode',validators=[DataRequired(),Length(min=5,max=5)])
    password = PasswordField('Password',validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    tags = SelectMultipleField('Select Causes You Support', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    email_me = BooleanField('Receive Weekly Promotion Newsletters',default="checked")
                                                                                                                                       
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already registered')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered')

class CompanyRegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    name = StringField('Company Name',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = URLField('Website URL',validators=[Optional(), URL()])
    zipcode = StringField('5 Digit Zipcode',validators=[DataRequired(),Length(min=5,max=5)])
    password = PasswordField('Password',validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    tags = SelectMultipleField('Select Company Descriptors', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    submit = SubmitField('Register')
    
    def validate_username(self,username):
        user = Company.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already registered')
    
    def validate_email(self,email):
        user = Company.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered')
    
    def validate_website(self,website):
        user = Company.query.filter_by(website=website.data).first()
        if user is not None:
            raise ValidationError('This website is already registered')

class Profile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(),Email()])
    photo = FileField('Upload a Profile Picture',validators=[FileAllowed(photos,'Images Only!')])
    tags = SelectMultipleField('Select Causes You Support', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    submit = SubmitField('Submit')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('This username is already registered')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('This email is already registered')
    
    def save_picture(self, form_picture):
        random_hex = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_picture.filename)
        fn = random_hex + f_ext
        path = os.path.join(app.root_path,'static/uploads',fn)

        output_size = (125,125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(path)

        return fn

class CompanyProfile(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    website = URLField('Website', validators=[Optional(), URL()])
    photo = FileField('Upload a Profile Picture',validators=[FileAllowed(photos,'Images Only!')])
    tags = SelectMultipleField('Select Causes You Support', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    submit = SubmitField('Submit')

    def validate_name(self,name):
        if name.data != current_user.name:
            user = Company.query.filter_by(name=name.data).first()
            if user is not None:
                raise ValidationError('This name is already registered')
    
    def validate_website(self,website):
        if website.data != current_user.website:
            user = Company.query.filter_by(website=website.data).first()
            if user is not None:
                raise ValidationError('This website is already registered')
    
    def save_picture(self, form_picture):
        random_hex = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_picture.filename)
        fn = random_hex + f_ext
        path = os.path.join(app.root_path,'static/uploads',fn)

        output_size = (125,125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(path)

        return fn

class Adv_Profile(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    zipcode = StringField('5 Digit Zipcode',validators=[DataRequired(),Length(min=5,max=5)])
    tags = SelectMultipleField('Select Causes You Support', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    email_me = BooleanField('Receive Weekly Promotion Newsletters',default="checked")                                                                                                                                  
    submit = SubmitField('Save Changes')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('This username is already registered')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('This email is already registered')

class Adv_CompanyProfile(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    name = StringField('Company Name',validators=[DataRequired()])
    website = URLField('Website URL',validators=[Optional(), URL()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    zipcode = StringField('5 Digit Zipcode',validators=[DataRequired(),Length(min=5,max=5)])
    tags = SelectMultipleField('Select Company Descriptors', choices=[(t.name, t.name) for t in Tag.query.order_by('name')])
    submit = SubmitField('Save Changes')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = Company.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('This username is already registered')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = Company.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('This email is already registered')
    
    def validate_website(self,website):
        if website.data != current_user.website:
            user = Company.query.filter_by(website=website.data).first()
            if user is not None:
                raise ValidationError('This website is already registered')

class PromotionUpload(FlaskForm):
    photo = MultipleFileField('Upload a Promotion',validators=[FileAllowed(photos,'Images Only!')])
    submit = SubmitField('Upload')
    
    def save_picture(self,form_picture):
        random_hex = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_picture.filename)
        fn = random_hex + f_ext
        path = os.path.join(app.root_path,'static/promotions',fn)

        output_size = (250,250)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(path)

        return fn

class ResetPassword(FlaskForm):
    type = SelectField('Select Account Type',choices=[('User','User'),('Company','Company')],validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')
    





    

    


