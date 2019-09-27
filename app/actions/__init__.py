from datetime import datetime, timedelta
from app.models import LessonSchedule, LessonActual, Teacher, LessonFee, Grade, Instrument, InvoiceLesson


def post_add_invoice_lesson(item, session):

    d = []
    first_day = datetime(item.lesson_year, item.lesson_month, 1)

    if item.student_history.lesson_week > first_day.weekday():
        first_day = first_day + timedelta(days=(item.student_history.lesson_week - first_day.weekday()))
    elif item.lesson_week < first_day.weekday():
        first_day = first_day + timedelta(days=(7 + item.student_history.lesson_week - first_day.weekday()))
    else:
        pass

    grade = session.query(Grade).get(item.student_history.grade_id)
    instrument = session.query(Instrument).get(item.student_history.instrument_id)
    lesson_fee = session.query(LessonFee)\
                        .filter(LessonFee.grade == grade)\
                        .filter(LessonFee.instrument == instrument) \
                        .filter(LessonFee.duration == item.student_history.lesson_duration) \
                        .first()

    while first_day.month == item.lesson_month:
        d.append(first_day)

        s = LessonSchedule()
        s.invoice_lesson = item
        s.begin_datetime = datetime.strptime(first_day.strftime('%Y-%m-%d') + ' ' +
                                             item.student_history.lesson_begin_time + ':00', '%Y-%m-%d %H:%M:%S')
        s.end_datetime = datetime.strptime(first_day.strftime('%Y-%m-%d') + ' ' +
                                           item.student_history.lesson_end_time + ':00', '%Y-%m-%d %H:%M:%S')
        s.lesson_fee = lesson_fee.price
        s.pay_month = item.lesson_month
        s.pay_year = item.lesson_year

        t = session.query(Teacher).get(item.student_history.teacher_id)
        s.teacher = t

        session.add(s)
        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

        a = LessonActual()
        a.lesson_schedule = s
        a.begin_datetime = s.begin_datetime
        a.end_datetime = s.end_datetime

        session.add(a)
        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

        first_day = first_day + timedelta(days=7)

