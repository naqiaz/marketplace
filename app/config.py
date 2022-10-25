import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0215@localhost/app'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOADED_PHOTOS_DEST = os.path.join(basedir,'static/uploads')
    UPLOADED_PROMOS_DEST = os.path.join(basedir,'static/promotions')
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cause.base.marketplace@gmail.com']
    
    COMPANIES_PER_PAGE = 3
    PROMOTIONS_PER_PAGE = 3