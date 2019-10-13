from flask_appbuilder.models.sqla.interface import SQLAInterface

from wtforms import Form, validators, StringField, DateField, SubmitField, SelectField
from app.widgets import CustomizeSelect2Widget
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, TimePickerWidget, BS3TextFieldWidget
from app.utils import get_choices
from app.models import Coupon, Category, Config

from .base_util import *
from .base import *


class ConfigView(AuditModelView):
    datamodel = SQLAInterface(Config)
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action']
    list_columns = ['key']


class CouponView(AuditModelView):
    datamodel = SQLAInterface(Coupon)
    # list_template = 'appbuilder/general/model/list.html'
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action']

    list_columns = ['code', 'discount_display', 'expiry_date', 'is_multiple', 'coupon_status', 'status_display']
    label_columns = {'discount_display': 'Discount (%)',
                     'status_display': 'Is Void'}

    add_columns = ['code', 'expiry_date', 'is_multiple', 'coupon_status', 'discount']
    edit_columns = ['code', 'expiry_date', 'is_multiple', 'coupon_status', 'discount', 'status']

    add_form_extra_fields = {
        'is_multiple': SelectField('Is Multiple', choices=get_choices('yes_no'),
                                   validators=[validators.DataRequired()],
                                   widget=CustomizeSelect2Widget(extra_classes=""),
                                   default="No"),
        'coupon_status': SelectField('Coupon Status', choices=get_choices('open_close'),
                                     validators=[validators.DataRequired()],
                                     widget=CustomizeSelect2Widget(extra_classes=""),
                                     default="Open"),
        'discount': StringField('Discount (%)', widget=BS3TextFieldWidget()),
    }

    edit_form_extra_fields = {
        'is_multiple': SelectField('Is Multiple', choices=get_choices('yes_no'),
                                   validators=[validators.DataRequired()],
                                   widget=CustomizeSelect2Widget(extra_classes=""),
                                   default="No"),
        'coupon_status': SelectField('Coupon Status', choices=get_choices('open_close'),
                                     validators=[validators.DataRequired()],
                                     widget=CustomizeSelect2Widget(extra_classes=""),
                                     default="Open"),
        'discount': StringField('Discount (%)', widget=BS3TextFieldWidget()),
        'status': SelectField('Is Void', choices=get_choices('is_void'),
                              validators=[validators.DataRequired()],
                              widget=CustomizeSelect2Widget(extra_classes=""))
    }

    def pre_add(self, item):
        if item.code:
            item.code = item.code.upper()

    def pre_update(self, item):
        if item.code:
            item.code = item.code.upper()


class CategoryView(AuditModelView):
    datamodel = SQLAInterface(Category)
    base_permissions = ['can_list', 'can_add', 'can_edit']

    list_columns = ['category_type', 'description', 'price_label', 'quantity', 'expiry_date']
    label_columns = {'category_type': 'Type',
                     'price_label': 'Price',
                     'status_display': 'Is Void'}

    add_form_extra_fields = {
        'category_type': SelectField('Type', choices=get_choices('category'),
                                     validators=[validators.DataRequired()],
                                     widget=CustomizeSelect2Widget(extra_classes="")),
    }
    edit_form_extra_fields = {
        'category_type': SelectField('Type', choices=get_choices('category'),
                                     validators=[validators.DataRequired()],
                                     widget=CustomizeSelect2Widget(extra_classes="")),
        'status':SelectField('Is Void', choices=get_choices('is_void'),
                             validators=[validators.DataRequired()],
                             widget=CustomizeSelect2Widget(extra_classes=""))
    }

    base_order = ('category_type', 'asc')
