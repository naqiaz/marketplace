import os, logging
from flask_mail import Mail
from logging.handlers import SMTPHandler, RotatingFileHandler
from app.config import Config
from flask import Flask
from flask_uploads import UploadSet,configure_uploads,DOCUMENTS,IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
photos = UploadSet('photos',IMAGES)
promos = UploadSet('promos',IMAGES)
configure_uploads(app,photos)
configure_uploads(app,promos)
patch_request_class(app)
mail = Mail(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        # mail handler
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
                                   fromaddr='no-reply@'+app.config['MAIL_SERVER'],toaddrs=app.config['ADMINS'],subject='Marketplace Error',
                                   credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        
        # log of errors & other warning info
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/marketplace.log',maxBytes=10240,
                                          backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Marketplace startup')


                 
from app import routes, models, errors 