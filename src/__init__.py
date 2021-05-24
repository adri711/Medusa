from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin import Admin,AdminIndexView,helpers, expose
from os.path import join, dirname, realpath

application = Flask(__name__)

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user and g.user.permission >= 1):
            return redirect(url_for('signin'))
        return super(MyAdminIndexView, self).index()

application.config['SECRET_KEY'] = b'\xf8\xb24,\x0e\xef\x0c!\ndj\\Y\xb1\x99\xab\xbdF\x8b\x99\xf8\xc0a\xad'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config["TEMPLATES_AUTO_RELOAD"] = True
application.config['FILE_UPLOADS'] = join(dirname(realpath(__file__)), 'static/images/uploads/users_avatars')
application.config['flouci_public'] = "40196cd9-6a5a-4498-973b-088810638508"
application.config['flouci_private'] = "b9ad995c-8696-4acd-8e31-d9c75a1fbd95"

db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
Migrate(application, db)
# Admin panel
admin = Admin(application, name='Espace administrateur', index_view=MyAdminIndexView(), template_mode='bootstrap3')

# App modules
from src.routes import *
from src.models import *
from src.admin_panel import *