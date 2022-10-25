from app import app, db
from app.models import User, Company, Tag, UserTag, CompanyTag

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User': User, 'Company':Company,'Tag':Tag, 'UserTag':UserTag,'CompanyTag':CompanyTag }

