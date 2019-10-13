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


def get_random_name(names_list, size=1):
    name_lst = [names_list[random.randrange(0, len(names_list))].decode("utf-8").capitalize() for i in range(0, size)]
    return " ".join(name_lst)





f = open('NAMES.DIC', "rb")
names_list = [x.strip() for x in f.readlines()]

f.close()

# print("===============================================")
# i = db.session.query(Invoice).get(1)
# print (i)
#


def random_number(ceil):
    return random.randint(0, ceil)

'''
def post_add(item, db, u):
    # print(item)
    datamodel = SQLAInterface(InvoiceLesson)
    datamodel.session = db.session
    datamodel_lesson_schedule = SQLAInterface(LessonSchedule)
    datamodel_lesson_schedule.session = db.session
    from datetime import datetime, timedelta

    d = []
    first_day = datetime(item.lesson_year, item.lesson_month, 1)

    if item.student_history.lesson_week > first_day.weekday():
        first_day = first_day + timedelta(days=(item.student_history.lesson_week - first_day.weekday()))
    elif item.lesson_week < first_day.weekday():
        first_day = first_day + timedelta(days=(7 + item.student_history.lesson_week - first_day.weekday()))
    else:
        pass

    # print(first_day)
    while first_day.month == item.lesson_month:
        d.append(first_day)

        s = LessonSchedule()
        s.invoice_lesson = item
        s.begin_datetime = datetime.strptime(first_day.strftime('%Y-%m-%d') + ' ' +
                                             item.student_history.lesson_begin_time + ':00', '%Y-%m-%d %H:%M:%S')
        s.end_datetime = datetime.strptime(first_day.strftime('%Y-%m-%d') + ' ' +
                                           item.student_history.lesson_end_time + ':00', '%Y-%m-%d %H:%M:%S')

        s.changed_by = u
        s.created_by = u

        datamodel.session.add(s)

        a = LessonActual()
        a.lesson_schedule = s
        a.begin_datetime = s.begin_datetime
        a.end_datetime = s.end_datetime
        a.changed_by = u
        a.created_by = u

        datamodel.session.add(a)
        try:
            datamodel.session.commit()
            # print("inserted", s)
        except Exception as e:
            print(e)
            datamodel.session.rollback()

        first_day = first_day + timedelta(days=7)

    pass
'''

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


# d1 = datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
# d2 = datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
#
# dr = random_date(d1, d2)
# print(dr.strftime('%Y-%m-%d %H:%M:%S.%f'))


app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)

with app.app_context():
    print('in app context, before first request context')
    g.user = db.session.query(User).get(1)
    print('user: {0}'.format(g.user))


    # u = db.session.query(User).get(1)
    # print(u)
    # g.user = u
    # print(g.user)
    t = db.session.query(Teacher).get(1)
    print(t)

    # i = [u.__dict__ for u in db.session.query(Instrument).all()]
    i = []
    for k in db.session.query(Instrument).all():
        i.append(k)

    # print(i [random_number(len(i)) ])

    grade = []
    for k in db.session.query(Grade).all():
        grade.append(k)


    # print(g [random_number(len(i)) ])


    # db.session.query(Student).delete()

    # for i in range(1, 11):
    #     c = Student()
    #     c.first_name = get_random_name(names_list, random.randrange(1, 2))
    #     c.last_name = get_random_name(names_list, random.randrange(1, 2))
    #     c.email = c.first_name + '.' + c.last_name + '@mail.com'
    #     c.changed_by = u
    #     c.created_by = u
    #
    #     db.session.add(c)
    #     try:
    #         db.session.commit()
    #         print("inserted", c)
    #     except Exception as e:
    #         print(e)
    #         db.session.rollback()

    # rs = db.session.query(Student)
    # for s in rs:
    #     print(s)
    #     h = StudentHistory()
    #     h.student = s
    #     h.teacher = t
    #     h.instrument = i[random_number(len(i)-1)]
    #     h.grade = g[random_number(len(i)-1)]
    #     h.start_date = datetime(2019, 1, 1)
    #     h.end_date = None
    #
    #     h.lesson_week = random_number(6)
    #     # lesson_begin_time = random_date(d1, d2)
    #     # h.lesson_begin_time = lesson_begin_time.strftime('%H:%M')
    #     # h.lesson_end_time = (lesson_begin_time + timedelta(minutes=45)).strftime('%H:%M')
    #     lesson_begin_time = datetime(2019, 1, 1, choice(list(set(range(10, 20)))) , choice(list(set([0,15,30,45]))))
    #     h.lesson_begin_time = lesson_begin_time.strftime('%H:%M')
    #     h.lesson_end_time = (lesson_begin_time + timedelta(minutes=45)).strftime('%H:%M')
    #     h.lesson_duration = 45
    #     h.changed_by = u
    #     h.created_by = u
    #     print(h)
    #     db.session.add(h)
    #     try:
    #         db.session.commit()
    #         print("inserted", h)
    #     except Exception as e:
    #         print(e)
    #         db.session.rollback()

    year = 2019
    month = 5
    query = """
            select * from student_history x 
            where 
            end_date is NULL and 
            x.id not in(
                select 
                    h.id
                from 
                    invoice_lesson i
                inner join (select * from student_history where end_date is NULL) as h on
                    h.id = i.student_history_id
                where
                i.lesson_year = {} and
                i.lesson_month = {}
            )
            """

    hs = []
    # for k in db.session.query(StudentHistory).all():

    # hs = [u.__dict__ for u in db.session.execute(query).all()]
    for row in db.session.execute(query.format(year, month)):
        result_dict = dict(zip(row.keys(), row))
        hs.append(result_dict)

    print(hs)
    print(len(hs))


    # db.session.query(InvoiceLesson).delete()
    # db.session.commit()

    for h in hs:
        invoice_lesson = InvoiceLesson()
        invoice_lesson.student = db.session.query(Student).get(h['student_id'])
        invoice_lesson.student_history = db.session.query(StudentHistory).get(h['id'])
    
        # invoice_date = Column(Date, default=datetime.date.today(), nullable=False)
    
        invoice_lesson.lesson_year = year
        invoice_lesson.lesson_month = month
        invoice_lesson.lesson_week = h['lesson_week']
        # invoice_lesson.changed_by = u
        # invoice_lesson.created_by = u
        invoice_lesson.payment = 'Outstanding'
    
        db.session.add(invoice_lesson)
        try:
            db.session.commit()
            db.session.refresh(invoice_lesson)
            print("inserted", invoice_lesson)
            # post_add(invoice_lesson, db, u)
    
            post_add_invoice_lesson (invoice_lesson, db.session)
    
        except Exception as e:
            print(e)
            db.session.rollback()


    db.engine.dispose()

