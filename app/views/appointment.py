from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.actions import action
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterEqual,\
                                                 BaseFilter, BaseFilterConverter, FilterRelation, FilterGreater

from flask_appbuilder.widgets import ListLinkWidget
from flask_appbuilder.api import BaseApi, expose

from flask_weasyprint import HTML, CSS, render_pdf
from wtforms import Form, validators, StringField, DateField, SubmitField, SelectField, HiddenField
from app.widgets import CustomizeSelect2Widget
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, TimePickerWidget, BS3TextFieldWidget, BS3TextFieldROWidget
from app.models import Appointment, AppointmentRequest
from app.utils import random_color, get_choices

from .base import *
from .base_util import *

import json


# from .receipt import AppointmentReceiptView


class ExampleApi(BaseApi):
    resource_name = 'example'

    @expose('/greeting')
    @has_access
    def greeting(self):
        return self.response(200, message="Hello")

    @expose('/greeting2', methods=['POST'])
    def greeting2(self):
        if request.method == 'GET':
            return self.response(200, message="Hello (GET)")
        # return self.response(201, message="Hello (POST)")
        else:
            print(request.form)
            a = {'name': 'Sarah', 'age': 24, 'isEmployed': True}
            j = json.dumps(a)
            return self.response(201, data=j)


class AppointmentRequestView(AuditModelView):
    datamodel = SQLAInterface(AppointmentRequest)
    list_widget = ListLinkWidget
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action']

    list_columns = ['receipt_no_display', 'physician', 'begin_datetime', 'end_datetime', 'facilities_booking']

    add_columns = ['title', 'first_name', 'last_name', 'contact_no',
                   'begin_datetime']
                   # , 'end_datetime', 'customer', 'physician']

    edit_columns = add_columns

    add_form_extra_fields = {
        'title': SelectField('Title', choices=get_choices('title'),
                                 validators=[validators.DataRequired()],
                                 widget=CustomizeSelect2Widget(extra_classes=""))
    }

    edit_form_extra_fields = add_form_extra_fields


class AppointmentView(AuditModelView):
    datamodel = SQLAInterface(Appointment)
    list_widget = ListLinkWidget
    # related_views = [AppointmentReceiptView]
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    # list_template = 'appbuilder/general/model/list.html'
    base_order = ('receipt_no', 'desc')
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action']
    list_columns = ['receipt_no_display', 'physician', 'begin_datetime', 'end_datetime', 'facilities_booking', 'diagnosis']

    label_columns = {'diagnosis': 'Diagnosis',
                     'injury_due_to': 'Injury due to accident, when was it',
                     'receipt_no_display': 'Receipt No'}
                    #'diagnosis': 'Referral Letter Exact Diagnosis as shown',

    add_columns = ['customer', 'physician', 'begin_datetime', 'end_datetime',
                   'referral_doctor', 'source_of_referral',
                   'sick_leave', 'insurance_cover', 'facilities_booking',
                   'injury_due_to', 'diagnosis', 'color_code']

    edit_columns = ['receipt_no', 'customer', 'physician', 'begin_datetime', 'end_datetime',
                   'referral_doctor', 'source_of_referral',
                   'sick_leave', 'insurance_cover', 'facilities_booking',
                   'injury_due_to', 'diagnosis', 'color_code']

    add_form_query_rel_fields = {'physician': [['user_type', FilterEqual, 'Physician']]}

    edit_form_query_rel_fields = add_form_query_rel_fields

    add_form_extra_fields = {
        'sick_leave': SelectField('Sick Leave', choices=get_choices('yes_no'),
                                  validators=[validators.DataRequired()],
                                  widget=CustomizeSelect2Widget(extra_classes=""),
                                  default="Yes"),
        'insurance_cover': SelectField('Insurance Cover', choices=get_choices('yes_no'),
                                       validators=[validators.DataRequired()],
                                       widget=CustomizeSelect2Widget(extra_classes=""),
                                       default="Yes"),
        'facilities_booking': SelectField('Facilities Booking', choices=get_choices('yes_no'),
                                          validators=[validators.DataRequired()],
                                          widget=CustomizeSelect2Widget(extra_classes=""),
                                          default="No"),
        'color_code': HiddenField()
    }

    edit_form_extra_fields = {
        'sick_leave': SelectField('Sick Leave', choices=get_choices('yes_no'),
                                  validators=[validators.DataRequired()],
                                  widget=CustomizeSelect2Widget(extra_classes=""),
                                  default="Yes"),
        'insurance_cover': SelectField('Insurance Cover', choices=get_choices('yes_no'),
                                       validators=[validators.DataRequired()],
                                       widget=CustomizeSelect2Widget(extra_classes=""),
                                       default="Yes"),
        'facilities_booking': SelectField('Facilities Booking', choices=get_choices('yes_no'),
                                          validators=[validators.DataRequired()],
                                          widget=CustomizeSelect2Widget(extra_classes=""),
                                          default="No"),
        'receipt_no': StringField('Receipt No', widget=BS3TextFieldWidget()),
        'color_code': HiddenField()
    }

    def __init__(self, **kwargs):
        self.add_exclude_columns.append('receipts')
        self.edit_exclude_columns.append('receipts')
        self.show_exclude_columns.append('receipts')
        super(AuditModelView, self).__init__(**kwargs)

    @expose("/edit/<pk>", methods=["GET", "POST"])
    @has_access
    def edit(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        widgets = self._edit(pk)

        query = """
                select count(*) from appointment
                where
                    facilities_booking = 'Yes' and
                    created_on < (select created_on from appointment where id = {}) and (

                    begin_datetime between (select begin_datetime from appointment where id = {}) and
                                         (select end_datetime from appointment where id = {})
                                         or
                    end_datetime between (select begin_datetime from appointment where id = {}) and
                                         (select end_datetime from appointment where id = {})
                    )
                """

        if not widgets:
            return self.post_edit_redirect()
        else:
            appointment = db.session.query(Appointment).filter_by(id=pk).one()
            if appointment.facilities_booking == 'Yes':
                count = db.session.execute(query.format(pk, pk, pk, pk, pk)).scalar()
                if count > 0:
                    flash('Facilities booking within this appointment period is reserved', 'danger')

            return self.render_template(
                self.edit_template,
                title=self.edit_title,
                widgets=widgets,
                related_views=self._related_views,
            )

    def pre_add(self, item):
        u = db.session.query(User).filter_by(id=item.physician.id).one()
        item.color_code = u.color_code
        if item.end_datetime is None:
            item.end_datetime = item.begin_datetime + timedelta(hours=1)

    @action("customer", "Back to Customer", "", "fa-user", btnclass="btn-warning", multiple=False)
    def customer(self, item):
        return redirect('/customerview/edit/{}'.format(str(item.customer_id)))

    @action("preview_certificate", "Preview Certificate", "", "fa-print", btnclass="btn-success", multiple=False)
    def preview_certificate(self, item):
        total = 0
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.update_redirect()
        return self.render_template('certificate/one.html', appointment=item, total=total, current_date=current_date)

    @action("download_certificate", "Download Certificate", "", "fa-download", btnclass="btn-success", multiple=False)
    def download_certificate(self, item):
        total = 0
        current_date = datetime.now().strftime("%Y-%m-%d")
        html = self.render_template('certificate/one.html', appointment=item, total=total, current_date=current_date)
        css = CSS(string="""
                       @page {
                        size: a4 portrait;
                           margin: 5mm 5mm 5mm 5mm;
                       }
                       """)
        return render_pdf(HTML(string=html), stylesheets=[css],
                          download_filename=None, automatic_download=False)


class AppointmentCalendarView(BaseView):
    default_view = 'calendar'

    @expose('/calendar')
    def calendar(self):
        resource_query = """
                    select 
                        id, first_name, last_name
                     from ab_user
                    """
        resource_cursor = db.session.execute(resource_query)

        resources = []
        for x in resource_cursor:
            d = dict()
            d['id'] = x['id']
            d['title'] = x['first_name'] + ' ' + x['last_name']
            resources.append(d)

        event_query = """
                    select 
                        id, customer_id, physician_id, begin_datetime, end_datetime, color_code,
                        customer_name, physician_name
                     from view_appointment_calendar
                    """

        event_cursor = db.session.execute(event_query)

        events = []
        appointment_color_dict = dict()
        for x in event_cursor:
            e = dict()
            e['id'] = x['id']
            e['resourceId'] = x['physician_id']
            e['start'] = datetime.strptime(x['begin_datetime'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S')
            e['end'] = datetime.strptime(x['end_datetime'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S')
            e['title'] = x['customer_name'] + ' (' + x['physician_name'] + ')'
            e['customer_id'] = x['customer_id']
            e['physician_id'] = x['physician_id']
            e['backgroundColor'] = x['color_code']
            e['textColor'] = '#FFFFFF'

            '''
            if x['physician_id'] in appointment_color_dict:
                pass
            else:
                appointment_color_dict[x['physician_id']] = random_color()

            e['backgroundColor'] = appointment_color_dict.get(x['physician_id'])
            '''

            # e['borderColor'] = '#ff0000'
            e['url'] = '/appointmentview/edit/{}'.format(x['id'])
            events.append(e)

        current_date = datetime.now().strftime("%Y-%m-%d")

        self.update_redirect()
        return self.render_template('lesson/scheduler.html',
                                    title="Appointment Calendar",
                                    current_date=current_date,
                                    resources=resources, events=events)
