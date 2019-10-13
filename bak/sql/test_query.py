from app import db
from flask import Flask
from flask_appbuilder import SQLA
from app.models import Teacher, Student, StudentHistory, InvoiceLesson, Instrument, Grade, LessonSchedule, LessonActual
import random
from datetime import datetime
from flask_appbuilder.security.sqla.models import User, Role
from random import randrange
from datetime import timedelta
from flask_appbuilder.models.sqla.interface import SQLAInterface

from contextlib import contextmanager
from flask import appcontext_pushed, g

from app.actions import post_add_invoice_lesson

from random import choice, sample
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from app.models import LessonSchedule, LessonActual, Teacher, LessonFee, Grade, Instrument, InvoiceLesson

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)

with app.app_context():
    print('in app context, before first request context')
    g.user = db.session.query(User).get(1)
    print('user: {0}'.format(g.user))

    grade = db.session.query(Grade).get(1)
    instrument = db.session.query(Instrument).get(1)
    lesson_fee = db.session.query(LessonFee) \
        .filter(LessonFee.grade == grade) \
        .filter(LessonFee.instrument == instrument) \
        .first()

    print(lesson_fee.price)

    item.amount = lesson_fee.price * len(d)
    session.merge(item)

    db.engine.dispose()

