from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.baseviews import BaseView, expose
from flask_appbuilder.actions import action
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterEqual,\
                                                 BaseFilter, BaseFilterConverter, FilterRelation, FilterGreater

from flask_appbuilder.widgets import ListLinkWidget
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, TimePickerWidget, BS3TextFieldWidget, BS3TextFieldROWidget

from flask_weasyprint import HTML, CSS, render_pdf
from wtforms import Form, validators, StringField, DateField, SubmitField, SelectField, HiddenField
from app.widgets import CustomizeSelect2Widget
from app.models import Package, PackageTicket

from app.utils import random_color, get_choices

from .base import *
from .base_util import *
# from .receipt import PackageReceiptView


class PackageTicketView(AuditModelView):
    datamodel = SQLAInterface(PackageTicket)
    base_permissions = ['can_list', 'can_action']

    list_columns = ['mobile', 'begin_datetime', 'end_datetime']


class PackageView(AuditModelView):
    datamodel = SQLAInterface(Package)
    list_widget = ListLinkWidget
    related_views = [PackageTicketView]
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    list_template = 'appbuilder/general/model/list.html'

    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action', 'can_delete']

    list_columns = ['receipt_no_display', 'description', 'begin_date', 'end_date', 'ticket_count', 'ticket_remaining']

    label_columns = {'receipt_no_display': 'Receipt No',
                     'ticket_count': 'Ticket Count',
                     'ticket_remaining': 'Ticket Remaining',
                     }

    add_columns = ['customer', 'category', 'description', 'begin_date', 'end_date',
                   'sharing_mobile1', 'sharing_mobile2',
                   'sharing_mobile3', 'sharing_mobile4', 'sharing_mobile5', 'ticket_count', 'ticket_remaining']

    edit_columns = ['receipt_no', 'customer', 'description', 'begin_date', 'end_date',
                    'sharing_mobile1', 'sharing_mobile2', 'sharing_mobile3', 'sharing_mobile4',
                    'sharing_mobile5', 'ticket_count', 'ticket_remaining']

    validators_columns = {
        'sharing_mobile1': [SharingMobileValidator(message='Invalid Customer Mobile')],
        'sharing_mobile2': [SharingMobileValidator(message='Invalid Customer Mobile')],
        'sharing_mobile3': [SharingMobileValidator(message='Invalid Customer Mobile')],
        'sharing_mobile4': [SharingMobileValidator(message='Invalid Customer Mobile')],
        'sharing_mobile5': [SharingMobileValidator(message='Invalid Customer Mobile')]
    }

    add_form_query_rel_fields = {'category': [['category_type', FilterEqual, 'Packages'],
                                              ['expiry_date', FilterGreater, get_now()]]}

    add_form_extra_fields = {
        'description': HiddenField(),
        'ticket_count': HiddenField(),
        'ticket_remaining': HiddenField(),
    }

    edit_form_extra_fields = {
        'receipt_no': StringField('Receipt No', widget=BS3TextFieldROWidget()),
        'ticket_count': StringField('Ticket Count', widget=BS3TextFieldROWidget()),
        'ticket_remaining': StringField('Ticket Remaining', widget=BS3TextFieldROWidget())
    }

    def __init__(self, **kwargs):
        self.add_exclude_columns.append('receipts')
        self.edit_exclude_columns.append('receipts')
        self.show_exclude_columns.append('receipts')
        super(AuditModelView, self).__init__(**kwargs)

    def pre_add(self, item):
        item.description = f'{item.category.category_type} - {item.category.description}'
        item.ticket_count = item.category.quantity
        item.ticket_remaining = item.category.quantity

    @action("customer", "Back to Customer", "", "fa-user", btnclass="btn-warning", multiple=False)
    def customer(self, item):
        return redirect('/customerview/edit/{}'.format(str(item.customer_id)))
