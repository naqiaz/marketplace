import os
import secrets
from app import app, db, photos,promos
from app.forms import Adv_Profile, Adv_CompanyProfile, ResetPassword, ResetPasswordForm, LoginForm, RegistrationForm, CompanyProfile, CompanyRegistrationForm, Profile, PromotionUpload
from app.models import Person, User, Tag, Company,Promotion
from app.email import send_reset_email
from flask import render_template,request, url_for, redirect, flash, session
from werkzeug.urls import url_parse
from flask_login import login_required,logout_user,current_user,login_user

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])

def index():
    page = request.args.get('page',1,type=int)
    promotions = Promotion.query.order_by(Promotion.timestamp.desc()).paginate(
        page,app.config['PROMOTIONS_PER_PAGE'],False)
    if promotions.has_next:
        next_url = url_for('index',page=promotions.next_num)
    else:
        next_url = None
    if promotions.has_prev:
        prev_url = url_for('index',page=promotions.prev_num)
    else:
        prev_url = None

    return render_template('index.html',title='Home',promos=promos, 
                           next_url = next_url, prev_url=prev_url, promotions=promotions.items)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        account_type = ''
        if (form.type.data =='User'):
             user = User.query.filter_by(username=form.username.data).first()
             account_type = 'User'
        else:
             user = Company.query.filter_by(username=form.username.data).first() 
             account_type = 'Company'
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['account_type'] = account_type
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Login',form=form)

@app.route('/loguout')
def logout():
    session.pop('account_type',None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(type='User', email_me=form.email_me.data, username=form.username.data, email = form.email.data, zipcode=form.zipcode.data)
        user.set_password(form.password.data)
        
        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                user.set_tags(t)

        db.session.add(user)
        db.session.commit()
        flash(user.username + ' has successfully registered!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Registration',form=form)

@app.route('/company_register',methods=['GET','POST'])
def company_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company = Company(type='Company',username=form.username.data, name=form.name.data, email = form.email.data, website=form.website.data, zipcode=form.zipcode.data)
        company.set_password(form.password.data)

        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                company.set_tags(t)

        db.session.add(company)
        db.session.commit()
        flash(company.username + ' has successfully registered!')
        return redirect(url_for('login'))
    return render_template('company_register.html',title='Company Registration',form=form)

@app.route('/profile/<username>',methods=['GET','POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile', user=user, photos=photos)


@app.route('/promotions')
@login_required
def promotions():
    page = request.args.get('page',1,type=int)
    companies = current_user.companies().paginate(page,app.config['COMPANIES_PER_PAGE'],False)
    if companies.has_prev:
        prev_url = url_for('promotions',page=companies.prev_num)
    else:
        prev_url = None
    if companies.has_next:
        next_url = url_for('promotions',page=companies.next_num)
    else:
        next_url = None
    return render_template('promotions.html',title='Promotions', promos=promos,companies=companies.items,prev_url=prev_url, next_url=next_url)


@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = Profile()
    if form.validate_on_submit():
        if form.photo.data:
            pic_fn = form.save_picture(form.photo.data)
            current_user.image_file = pic_fn
        current_user.username = form.username.data
        current_user.tags = []
        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                current_user.set_tags(t)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.tags.data = current_user.tags
    return render_template('edit_profile.html',title='Edit Profile', photos=photos, form=form)

@app.route('/adv_profile',methods=['GET','POST'])
@login_required
def adv_profile():
    form = Adv_Profile()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.email_me = form.email_me.data
        current_user.zipcode = form.zipcode.data
        current_user.tags = []
        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                current_user.set_tags(t)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.email_me.data = current_user.email_me
        form.zipcode.data = current_user.zipcode
        form.tags.data = current_user.tags
    return render_template('adv_profile.html',title='Manage Account', form=form)

@app.route('/adv_comp_profile',methods=['GET','POST'])
@login_required
def adv_comp_profile():
    form = Adv_CompanyProfile()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.website = form.website.data
        current_user.email = form.email.data
        current_user.zipcode = form.zipcode.data
        current_user.tags = []
        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                current_user.set_tags(t)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('account',name=current_user.name))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.website.data = current_user.website
        form.email.data = current_user.email
        form.zipcode.data = current_user.zipcode
        form.tags.data = current_user.tags
    return render_template('adv_comp_profile.html',title='Manage Account', form=form)

@app.route('/account/<name>',methods=['GET','POST'])
@login_required
def account(name):
    form = PromotionUpload()
    user = Company.query.filter_by(name=name).first_or_404()
    if form.validate_on_submit():
        if form.photo.data:
            for p in form.photo.data:
                pic_fn = form.save_picture(p)
                pic = Promotion(image=pic_fn)
                current_user.promotions.append(pic)
            db.session.commit() 
            flash('Your promotions have been uploaded')
            return redirect(url_for('account',name=current_user.name))
    return render_template('company_account.html',title='Company Account', promos=promos, photos=photos, form=form, user=user)


@app.route('/edit_comp_profile',methods=['GET','POST'])
@login_required
def edit_comp_profile():
    form = CompanyProfile()
    if form.validate_on_submit():
        if form.photo.data:
            pic_fn = form.save_picture(form.photo.data)
            current_user.image_file = pic_fn
        current_user.name = form.name.data
        current_user.website = form.website.data
        current_user.tags = []
        for item in form.tags.data:
            t = Tag.query.filter_by(name=item).first()
            if t is not None:
                current_user.set_tags(t)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('account',name=current_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.website.data = current_user.website
        form.tags.data = current_user.tags
    return render_template('edit_comp_profile.html',title='Edit Profile', photos=photos, form=form)

@app.route('/reset_password',methods = ['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPassword()
    if form.validate_on_submit():
       if (form.type.data == 'User'):
        user = User.query.filter_by(email=form.email.data).first()
       if (form.type.data == 'Company'):
        user = Company.query.filter_by(email=form.email.data).first()
       if user:
        send_reset_email(user)
        flash('Check your inbox for the link to reset your password!')
       else:
        flash('This email has not been registered')
       return redirect(url_for('login'))
    return render_template('reset_password.html',title='Reset Password',form=form)

@app.route('/password_reset/<token>',methods = ['GET','POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = Person.verify_token(token)
    form = ResetPasswordForm()
    if user:
        if form.validate_on_submit():
           user.set_password(form.password.data)
           flash('Password Reset Successfully!')
           db.session.commit()
           return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))
    return render_template('password_reset.html',title='Password Reset',form=form)

@app.route('/delete_promo/<int:id>',methods=['POST'])
def delete_promo(id):
    p = Promotion.query.get_or_404(id)
    current_user.promotions.remove(p)
    db.session.delete(p)
    db.session.commit()
    flash('Your promotion has been deleted.')
    return redirect(url_for('account',name=current_user.name))

@app.route('/delete_comp/<int:id>',methods=['POST'])
def delete_comp(id):
    c = Company.query.get_or_404(id)
    session.pop('account_type',None)
    logout_user()
    c.tags.clear()
    db.session.delete(c)
    db.session.commit()
    flash('Your account has been deleted.')
    return redirect(url_for('login'))


@app.route('/delete_user/<int:id>',methods=['POST'])
def delete_user(id):
    u = User.query.get_or_404(id)
    session.pop('account_type',None)
    logout_user()
    u.tags.clear()
    db.session.delete(u)
    db.session.commit()
    flash('Your account has been deleted.')
    return redirect(url_for('login'))