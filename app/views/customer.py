from flask import Flask, render_template, flash, request, redirect, url_for
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder.widgets import ListLinkWidget
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.actions import action
from flask_appbuilder.fields import QuerySelectField
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterEqual,\
                                                 BaseFilter, BaseFilterConverter, FilterRelation

from flask_appbuilder.security.sqla.models import User

from flask import Flask, g
from wtforms import validators
from wtforms import SelectField

from app import db

from app.widgets import CustomizeSelect2Widget
from app.models import Customer, CustomerDocument, Appointment, Package, MedicalHistory
from app.utils import get_choices

from .base import AuditModelView
from .base_util import *
from .appointment import AppointmentView
from .package import PackageView
from .receipt import ReceiptView, ReceiptCustomerView

from flask_appbuilder.urltools import Stack


class CustomFilterEqualFunction(BaseFilter):
    name = "Filter view with a function"
    arg_name = "eqf"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        if get_user().roles[0].name == 'Admin' or get_user().roles[0].name == 'Staff':
            return query
        else :
            return query.filter((Customer.physician1 == get_user()) | (Customer.physician2 == get_user()) )
            # or_(Customer.physician1 == 'phy1', Customer.physician2 == 'phy1'))


class CustomFilterRoleFunction(BaseFilter):
    name = "Filter view with a function"
    arg_name = "eqf"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        # for r in get_user().roles:
        #     if r.name == 'Physician':
        #         return query
        if get_user().roles[0].name == 'Admin' or get_user().roles[0].name == 'Staff':
            return query
        else :
            return query.filter((Customer.physician1 == get_user()) | (Customer.physician2 == get_user()) |
                                (Customer.physician3 == get_user()) | (Customer.physician4 == get_user()) |
                                (Customer.physician5 == get_user()))
            # or_(Customer.physician1 == 'phy1', Customer.physician2 == 'phy1'))


class CustomerDocumentView(AuditModelView):
    datamodel = SQLAInterface(CustomerDocument)
    base_permissions = ['can_list', 'can_add', 'can_delete', 'can_download', 'can_show', 'can_action']
    label_columns = {"file_name": "File Name", "download": "Download", "preview_image": "Preview Image"}
    add_columns = ["file", "description", "customer"]
    edit_columns = ["file", "description", "customer"]
    list_columns = ["file_name", "description", "download"]
    show_columns = ["file_name", "description", "download", "preview_image"]

    @action("customer", "Back to Customer", "", "fa-user", btnclass="btn-warning", multiple=False)
    def customer(self, item):
        return redirect('/customerview/edit/{}'.format(str(item.customer_id)))


class MedicalHistoryView(AuditModelView):
    datamodel = SQLAInterface(MedicalHistory)

    list_columns = ["operation", "heart_diseases", "diabetes", "dizziness", "allergy"]
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_delete', 'can_download', 'can_action']

    add_columns = ['customer', 'heart_diseases', 'diabetes', 'dizziness', 'allergy',
                   'operation', 'operation_date', 'cancer', 'certificated_date',
                   'medicine_currently_taking', 'emergency_medicine', 'notes']
    edit_columns = add_columns

    add_fieldsets = [
        ('Diseases', {'fields': [
                "heart_diseases", "diabetes", "dizziness", "allergy",
                ],
            }),
        ('Operation & Cancer', {
                'fields': [
                    "customer", "operation", "operation_date", "cancer", "certificated_date",
                ]
            }),

        ('Remarks', {'fields': [
                    "medicine_currently_taking", "emergency_medicine", "notes",
                ],
            }),
    ]

    edit_fieldsets = add_fieldsets

    add_form_extra_fields = {
        'heart_diseases': SelectField('Heart Diseases', choices=get_choices('yes_no'),
                                      validators=[validators.DataRequired()],
                                      widget=CustomizeSelect2Widget(extra_classes="")),
        'diabetes': SelectField('Diabetes', choices=get_choices('yes_no'),
                                validators=[validators.DataRequired()],
                                widget=CustomizeSelect2Widget(extra_classes="")),
        'dizziness': SelectField('Dizziness', choices=get_choices('yes_no'),
                                 validators=[validators.DataRequired()],
                                 widget=CustomizeSelect2Widget(extra_classes="")),
        'allergy': SelectField('Allergy', choices=get_choices('yes_no'),
                               validators=[validators.DataRequired()],
                               widget=CustomizeSelect2Widget(extra_classes="")),
    }

    edit_form_extra_fields = add_form_extra_fields

    @action("customer", "Back to Customer", "", "fa-user", btnclass="btn-warning", multiple=False)
    def customer(self, item):
        return redirect('/customerview/edit/{}'.format(str(item.customer_id)))


def physician_query_func():
    return db.session.query(User).filter_by(user_type='Physician')


def physician_get_pk_func(item):
    return item.id


class CustomerView(AuditModelView):
    datamodel = SQLAInterface(Customer)
    list_widget = ListLinkWidget
    related_views = [AppointmentView, PackageView, ReceiptCustomerView, CustomerDocumentView, MedicalHistoryView]
    # show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit.html'
    # list_template = 'appbuilder/general/model/list.html'

    search_columns = ['first_name', 'last_name', 'hkid', 'contact_no']

    list_columns = ['first_name', 'last_name', 'display_hkid', 'display_contact_no']

    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_search']

    label_columns = {'physician1': 'Primary Physician',
                     'physician2': 'Physician',
                     'physician3': 'Physician',
                     'physician4': 'Physician',
                     'physician5': 'Physician',
                     'hkid': 'HK ID',
                     'display_hkid': 'HK ID',
                     'display_contact_no': 'Contact No'}

    base_order = ('first_name', 'asc')

    add_form_query_rel_fields = {'physician1': [['user_type', FilterEqual, 'Physician']],
                                 'physician2': [['user_type', FilterEqual, 'Physician']],
                                 'physician3': [['user_type', FilterEqual, 'Physician']],
                                 'physician4': [['user_type', FilterEqual, 'Physician']],
                                 'physician5': [['user_type', FilterEqual, 'Physician']]
                               }

    edit_form_query_rel_fields = add_form_query_rel_fields

    base_filters = [['physician1', CustomFilterRoleFunction, get_user]]
    # base_filters = or_(Customer.physician1 == get_user()', User.name == 'akshay')

    add_columns = ["title", "first_name", "last_name", "chinese_name",
                   "date_of_birth", "hkid", "email", "contact_no", "mobile_no", "emergency_contact",
                   "referral_doctor", "source_of_referral",
                   "physician1", "physician2", "physician3", "physician4", "physician5"]

    edit_columns = add_columns

    add_fieldsets = [
        ('Personal', {
                'fields': [
                    "title", "first_name", "last_name", "hkid", "contact_no", 'physician1', "date_of_birth"
                ]
            }),
        ('Info', {'fields': [
                    "chinese_name", "email", "mobile_no", "emergency_contact", "referral_doctor", "source_of_referral",
                ],
                'expanded':False
            }),
        ('Other Physicians', {'fields': [
                    "physician2", "physician3", "physician4", "physician5",
                ],
                'expanded':False
            }),
    ]

    edit_fieldsets = add_fieldsets

    add_form_extra_fields = {
        'title': SelectField('Title', choices=get_choices('title'),
                                 validators=[validators.DataRequired()],
                                 widget=CustomizeSelect2Widget(extra_classes="")),

        # 'physician1': SelectField('Primary Physician', choices=get_choices('ab_user'),
        #                           validators=[validators.DataRequired()],
        #                           widget=CustomizeSelect2Widget(extra_classes=""),
        #                           default=get_user),
        'physician1':   QuerySelectField('Primary Physician',
                                         query_func=physician_query_func,
                                         get_pk_func=physician_get_pk_func,
                                         allow_blank=False,
                                         validators=[validators.DataRequired()],
                                         widget=Select2Widget(extra_classes=""),
                                         default=get_user),
        'physician2': QuerySelectField('Physician 2',
                                       query_func=physician_query_func,
                                       get_pk_func=physician_get_pk_func,
                                       allow_blank=True,
                                       validators=[],
                                       widget=Select2Widget(extra_classes="")),
        'physician3': QuerySelectField('Physician 3',
                                       query_func=physician_query_func,
                                       get_pk_func=physician_get_pk_func,
                                       allow_blank=True,
                                       validators=[],
                                       widget=Select2Widget(extra_classes="")),
        'physician4': QuerySelectField('Physician 4',
                                       query_func=physician_query_func,
                                       get_pk_func=physician_get_pk_func,
                                       allow_blank=True,
                                       validators=[],
                                       widget=Select2Widget(extra_classes="")),
        'physician5': QuerySelectField('Physician 5',
                                       query_func=physician_query_func,
                                       get_pk_func=physician_get_pk_func,
                                       allow_blank=True,
                                       validators=[],
                                       widget=Select2Widget(extra_classes=""))
    }

    edit_form_extra_fields = add_form_extra_fields

    def __init__(self, **kwargs):
        self.add_exclude_columns.append('appointments')
        self.edit_exclude_columns.append('appointments')
        self.show_exclude_columns.append('appointments')
        self.add_exclude_columns.append('customer_documents')
        self.edit_exclude_columns.append('customer_documents')
        self.show_exclude_columns.append('customer_documents')
        self.add_exclude_columns.append('medical_historys')
        self.edit_exclude_columns.append('medical_historys')
        self.show_exclude_columns.append('medical_historys')
        super(AuditModelView, self).__init__(**kwargs)

    def get_redirect(self):
        """
            Returns the previous url.
        """
        index_url = self.appbuilder.get_url_for_index
        page_history = Stack(session.get("page_history", []))
        pop = page_history.pop()

        if pop is None:
            return index_url
        else:
            if pop.find('/customerview/add') != -1:
                return f'/customerview/edit/{self.pk}'
            elif pop.find('/customerview/edit') != -1:
                return pop
            else:
                session["page_history"] = page_history.to_json()
                url = page_history.pop() or index_url
                return url


class CustomerStaffView(CustomerView):
    related_views = [AppointmentView, PackageView, ReceiptCustomerView]

