from flask import request, redirect, url_for, session,g
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from src import admin, db
from src.models import User,Product
from src import constants


class Admin_panel(sqla.ModelView):
    def is_accessible(self):
        return g.user and User.query.filter_by(id=g.user.id).first().permission >= constants.ADMIN_PANEL_PERMISSION_LEVEL
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index', next=request.url))

Users = admin.add_view(Admin_panel(User, db.session))
Products = admin.add_view(Admin_panel(Product, db.session))
