import logging
from flask import Flask, g
from flask_appbuilder import SQLA
from flask_appbuilder import AppBuilder
from flask_appbuilder.menu import Menu
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask import (flash, redirect, send_file, jsonify, make_response, url_for, session, abort)
from flask_appbuilder.baseviews import BaseView, BaseCRUDView, BaseFormView, expose, expose_api
from flask_appbuilder import IndexView
from flask_bootstrap import Bootstrap

from app.security import MySecurityManager


# logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
weasyprint_logger = logging.getLogger("weasyprint")
weasyprint_logger.addHandler(logging.NullHandler())
weasyprint_logger.setLevel(logging.ERROR)


class CustomIndexView(IndexView):
    default_view = 'index'
    index_template = 'appbuilder/index.html'

    @expose('/')
    def index(self):
        self.update_redirect()
        user = g.user

        if user.is_anonymous:
            return redirect(url_for('AuthDBView.login'))
        else:
            return redirect(url_for('AppointmentCalendarView.calendar'))


app = Flask(__name__)
app.config.from_object('config')
app.logger
Bootstrap(app)
db = SQLA(app)

appbuilder = AppBuilder(app, db.session,
                        indexview=CustomIndexView,
                        menu=Menu(reverse=False, extra_classes='navbar-default navbar-fixed-top'),
                        security_manager_class=MySecurityManager,
                        base_template='appbuilder/baselayout.html')


from app.utils import get_month_name, get_week_name
from app import models, views


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)

    def format_week(week):
        return get_week_name(week)

    def format_month(month):
        return get_month_name(month)

    return dict(format_price=format_price, format_week=format_week, format_month=format_month)



