import random
from app import db
from datetime import datetime, timedelta
from flask_appbuilder.security.sqla.models import User

today = datetime.now() #.strftime("%Y-%m-%d")


def random_color():
    r = lambda: random.randint(63, 192)
    # print('#%02X%02X%02X' % (r(), r(), r()))
    return '#%02X%02X%02X' % (r(), r(), r())


def random_light_color():
    r = lambda: random.randint(192, 255)
    # print('#%02X%02X%02X' % (r(), r(), r()))
    return '#%02X%02X%02X' % (r(), r(), r())


def random_dark_color():
    r = lambda: random.randint(0, 127)
    # print('#%02X%02X%02X' % (r(), r(), r()))
    return '#%02X%02X%02X' % (r(), r(), r())


def get_choices(t):
    if t == 'year':
        if today.month == 12:
            return [(str(today.year), str(today.year)),
                    (str(today.year-1), str(today.year-1))]
        else:
            return [(str(today.year), str(today.year))]
    elif t == 'month':
        return [('1', 'January'),
                ('2', 'February'),
                ('3', 'March'),
                ('4', 'April'),
                ('5', 'May'),
                ('6', 'June'),
                ('7', 'July'),
                ('8', 'August'),
                ('9', 'September'),
                ('10', 'October'),
                ('11', 'November'),
                ('12', 'December')]
    elif t == 'week':
        return [('0', 'Monday'),
                ('1', 'Tuesday'),
                ('2', 'Wednesday'),
                ('3', 'Thursday'),
                ('4', 'Friday'),
                ('5', 'Saturday'),
                ('6', 'Sunday')]
    elif t == 'hour':
        return [('20', '20'),
                ('10', '10'),
                ('5', '5'),
                ('1', '1'),
                ('0.5', '0.5')]
    elif t == 'duration':
        return [('30', '30'),
                ('45', '45'),
                ('60', '60')]
    elif t == 'payment':
        return [('Outstanding', 'Outstanding'),
                ('Settled', 'Settled')]
    elif t == 'payment_method':
        return [('Apple Pay', 'Apple Pay'),
                ('Cash', 'Cash'),
                ('G Pay', 'G Pay'),
                ('Bank Transfer', 'Bank Transfer'),
                ('Credit Card', 'Credit Card'),
                ('JCB', 'JCB'),
                ('MasterCard', 'MasterCard'),
                ('Samsung Pay', 'Samsung Pay'),
                ('Union Pay', 'Union Pay'),
                ('Visa', 'Visa'),
                ('WeChat', 'WeChat')]
    elif t == 'yes_no':
        return [('Yes', 'Yes'),
                ('No', 'No')]
    elif t == 'open_close':
        return [('Open', 'Open'),
                ('Close', 'Close')]
    elif t == 'preview_print':
        return [('Preview', 'Preview'),
                ('Print', 'Print')]
    elif t == 'lesson_remark':
        return [('Regular', 'Regular'),
                ('Leave', 'Leave'),
                ('Absent', 'Absent')]
    elif t == 'gender':
        return [('Male', 'Male'),
                ('Female', 'Female')]
    elif t == 'speciality':
        return [('Physio', 'Physio'),
                ('Therapist', 'Therapist')]
    elif t == 'category':
        return [('Services', 'Services'),
                ('Packages', 'Packages'),
                ('Products', 'Products'),
                ('Others', 'Others')]
    elif t == 'title':
        return [('Miss', 'Miss'),
                ('Mrs', 'Mrs'),
                ('Mr', 'Mr')]
    elif t == 'user_type':
        return [('Admin', 'Admin'),
                ('Physician', 'Physician'),
                ('Staff', 'Staff')]
    elif t == 'is_void':
        return [('I', 'Yes'),
                ('A', 'No')]
    elif t == 'receipt_type':
        return [('Appointment', 'Appointment'),
                ('Package', 'Package'),
                ('General', 'General')]
    elif t == 'ab_user':
        # db.session.execute("select id, first_name, last_name from ab_user")
        # query = "select id, first_name || ' ' || last_name as name from ab_user where user_type='Physician'"
        # results = []
        # for row in db.session.execute(query):
        #     result_dict = dict(zip(row.keys(), row))
        #     results.append((str(result_dict['id']), result_dict['name']))
        #
        # return results
        results = []
        user_list = db.session.query(User).filter_by(user_type='Physician').all()
        for u in user_list:
            results.append((str(u.id), u))
        return results

def get_month_name(i):
    months = ["",
              "January",
              "Febuary",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]
    return months[i]


def get_week_name(i):
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return week[i]
