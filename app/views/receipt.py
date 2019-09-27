from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.actions import action
from flask import Flask, render_template, flash, request, redirect, url_for, abort
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, TimePickerWidget, BS3TextFieldWidget, BS3TextFieldROWidget
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterEqual, FilterNotEqual, \
                                                 BaseFilter, BaseFilterConverter, FilterRelation, FilterGreater

from flask_appbuilder.widgets import ListLinkWidget
from flask_weasyprint import HTML, CSS, render_pdf
from wtforms import Form, validators, StringField, DateField, SubmitField, SelectField, HiddenField


from app.widgets import CustomizeSelect2Widget

from app.models import Appointment, Coupon, Receipt, ReceiptItem, Category, Package, PackageTicket
from app.utils import random_color, get_choices

from .base import AuditModelView
from .base_util import *
from flask_appbuilder.urltools import (
    get_filter_args,
    get_order_args,
    get_page_args,
    get_page_size_args,
    Stack
)


class ReceiptItemView(AuditModelView):
    datamodel = SQLAInterface(ReceiptItem)
    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action']

    list_columns = ['description_display', 'price_display', 'quantity', 'apply_coupon', 'discount_display', 'amount_display', 'status_display']
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    list_template = 'appbuilder/general/model/list.html'
    label_columns = {'discount_display': 'Discount',
                     'price_display': 'Price',
                     'amount_display': 'Amount',
                     'status_display': 'Is Void',
                     'description_display': 'Description'}
    add_form_extra_fields = {
        'description': StringField('Description', validators=[ReceiptItemValidator(message='Invalid')],
                                   widget=BS3TextFieldWidget()),
        'price': CustomizeFloatField('Price', validators=[ReceiptItemPriceValidator()],
                                     widget=BS3TextFieldWidget()),
        'apply_coupon': SelectField('Apply Coupon', choices=get_choices('yes_no'),
                                    validators=[validators.DataRequired()],
                                    widget=CustomizeSelect2Widget(extra_classes=""),
                                    default='No'),
        'quantity': IntegerField('Quantity', validators=[validators.DataRequired()],
                                 widget=BS3TextFieldWidget(), default='1')
    }
    edit_form_extra_fields = {
        'description': StringField('Description', validators=[validators.DataRequired()],
                                   widget=BS3TextFieldWidget()),
        'apply_coupon': SelectField('Apply Coupon', choices=get_choices('yes_no'),
                                    validators=[validators.DataRequired()],
                                    widget=CustomizeSelect2Widget(extra_classes=""),
                                    default='No'),
        'quantity': CustomizeIntegerField('Quantity', validators=[validators.DataRequired()],
                                          widget=BS3TextFieldWidget()),
        'discount': CustomizeFloatField('Discount',  widget=BS3TextFieldWidget()),
        'amount': CustomizeFloatField('Amount', validators=[validators.DataRequired()],
                                      widget=BS3TextFieldWidget()),
        'status': SelectField('Is Void', choices=get_choices('is_void'),
                              validators=[validators.DataRequired()],
                              widget=CustomizeSelect2Widget(extra_classes="")),
    }

    def get_redirect(self):
        if self.url is not None and request.method == "POST":
            if self.url.find('edit') != -1:
                page_history = Stack(session.get("page_history", []))
                url = page_history.pop()
                url = page_history.pop()
                return url

                # return self.url

            elif self.url.find('add') != -1:
                page_history = Stack(session.get("page_history", []))
                url = page_history.pop()
                url = page_history.pop()
                return url

                # page_history.pop()
                # return self.url.replace('add', 'edit/' + str(self.pk), 1)

            else:
                index_url = self.appbuilder.get_url_for_index
                page_history = Stack(session.get("page_history", []))

                if page_history.pop() is None:
                    return index_url
                session["page_history"] = page_history.to_json()
                url = page_history.pop() or index_url
                print(url)
                print(request.url)
                print(request.method)
                return url
        else:
            index_url = self.appbuilder.get_url_for_index
            page_history = Stack(session.get("page_history", []))

            if page_history.pop() is None:
                return index_url
            session["page_history"] = page_history.to_json()
            url = page_history.pop() or index_url
            print(url)
            print(request.url)
            print(request.method)
            return url


class ReceiptGeneralItemView(ReceiptItemView):
    add_columns = ['receipt', 'category', 'description', 'price', 'quantity', 'apply_coupon']
    edit_columns = ['receipt', 'description', 'price', 'quantity', 'apply_coupon', 'discount', 'amount', 'status']

    def pre_add(self, item):
        if item.category:
            item.price = item.category.price
            item.description = f'{item.category.category_type} - {item.category.description}'

        if item.receipt.coupon_code and item.apply_coupon == 'Yes':
            discount = db.session.execute("select discount from coupon where code='{}'".format(item.receipt.coupon_code)).scalar()
            item.discount = discount
            item.amount = item.price * int(item.quantity) * (100 - discount) / 100
        else:
            item.amount = item.price * int(item.quantity)


class ReceiptCustomerItemView(ReceiptItemView):
    add_columns = ['receipt', 'category', 'package', 'description', 'price', 'quantity', 'apply_coupon']
    edit_columns = ['receipt', 'description', 'price', 'quantity', 'apply_coupon', 'discount', 'amount', 'status']
    add_form_query_rel_fields = {
        'category': [['expiry_date', FilterGreater, get_now()],
                     ['category_type', FilterCategoryFunction, get_receipt_id_from_url]
                     ],
        'package': [['ticket_remaining', FilterGreater, 0],
                     ['sharing_mobile1', FilterPackageFunction, get_receipt_id_from_url]
                     ],
    }

    validators_columns = {
        'category': [ReceiptItemValidator(message='Invalid')],
        'package': [ReceiptItemValidator(message='Invalid')],
        'description': [ReceiptItemValidator(message='Invalid')],
    }

    def pre_add(self, item):
        if item.package:
            item.discount = 100
            item.amount = 0
            item.quantity = 1
            item.description = f'{item.package}'
            category = db.session.query(Category).filter_by(id=item.package.category_id).one()
            item.price = category.price
        else:
            if item.category:
                item.price = item.category.price
                item.description = f'{item.category.category_type} - {item.category.description}'
            if item.receipt.coupon_code and item.apply_coupon == 'Yes':
                discount = db.session.execute("select discount from coupon where code='{}'".format(item.receipt.coupon_code)).scalar()
                item.discount = discount
                item.amount = item.price * int(item.quantity) * (100 - discount) / 100
            else:
                item.amount = item.price * int(item.quantity)

    def post_add(self, item):
        if item.package:
            c = db.session.query(Customer).filter_by(id=item.receipt.customer_id).one()
            a = db.session.query(Appointment).filter_by(receipt_no=item.receipt.receipt_no).one()
            p = item.package

            p.ticket_remaining = p.ticket_remaining - 1
            pt = PackageTicket()
            pt.package = p
            pt.mobile = c.contact_no
            pt.begin_datetime = a.begin_datetime
            pt.end_datetime = a.end_datetime
            pt.customer = c

            try:
                db.session.add(pt)
                db.session.commit()
                print('commit')
            except Exception as e:
                print(e)
                db.session.rollback()


class ReceiptView(AuditModelView):
    datamodel = SQLAInterface(Receipt)
    list_widget = ListLinkWidget
    # related_views = [ReceiptItemView]
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    list_template = 'appbuilder/general/model/list.html'

    list_columns = ['receipt_no', 'receipt_date', 'receipt_type', 'coupon_code', 'payment_method', 'status_display']

    base_permissions = ['can_list', 'can_add', 'can_edit', 'can_action', 'can_delete', 'can_search']

    label_columns = {'status_display': 'Is Void'}

    base_order = ('receipt_no', 'desc')

    def __init__(self, **kwargs):
        self.add_exclude_columns.append('receipt_items')
        self.edit_exclude_columns.append('receipt_items')
        self.show_exclude_columns.append('receipt_items')
        super(AuditModelView, self).__init__(**kwargs)

    def _edit(self, pk):
        """
            Edit function logic, override to implement different logic
            returns Edit widget and related list or None
        """
        is_valid_form = True
        pages = get_page_args()
        page_sizes = get_page_size_args()
        orders = get_order_args()
        get_filter_args(self._filters)
        exclude_cols = self._filters.get_relation_cols()

        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        # convert pk to correct type, if pk is non string type.
        pk = self.datamodel.get_pk_value(item)
        self.pk = pk
        self.url = request.url

        if request.method == "POST":
            form = self.edit_form.refresh(request.form)
            # fill the form with the suppressed cols, generated from exclude_cols
            self._fill_form_exclude_cols(exclude_cols, form)
            # trick to pass unique validation
            form._id = pk
            if form.validate():
                self.process_form(form, False)
                form.populate_obj(item)
                try:
                    self.pre_update(item)
                except Exception as e:
                    flash(str(e), "danger")
                else:
                    if self.datamodel.edit(item):
                        self.post_update(item)
                    flash(*self.datamodel.message)
                finally:
                    return None
            else:
                is_valid_form = False
        else:
            # Only force form refresh for select cascade events
            form = self.edit_form.refresh(obj=item)
            # Perform additional actions to pre-fill the edit form.
            self.prefill_form(form, pk)

        widgets = self._get_edit_widget(pk=pk, form=form, exclude_cols=exclude_cols)

        # if item.receipt_type == 'Package':
        #     self.related_views = []
        #     self._related_views = []

        widgets = self._get_related_views_widgets(
            item,
            filters={},
            orders=orders,
            pages=pages,
            page_sizes=page_sizes,
            widgets=widgets,
        )

        if is_valid_form:
            self.update_redirect()
        return widgets

    def pre_add(self, item):
        count = db.session.execute('select count(1) from receipt').scalar()
        item.receipt_no = str(count+1).zfill(5)
        if item.coupon_code:
            item.coupon_code = item.coupon_code.upper()

        # print(item.receipt_no)

    def pre_update(self, item):
        if item.coupon_code:
            item.coupon_code = item.coupon_code.upper()

    def post_add(self, item):
        if item.appointment_id:
            receipt = db.session.query(Receipt).filter_by(id=item.id).one()
            appointment = db.session.query(Appointment).filter_by(id=receipt.appointment_id).one()
            appointment.receipt_no = receipt.receipt_no

            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()

        elif item.package_id:
            receipt = db.session.query(Receipt).filter_by(id=item.id).one()
            package = db.session.query(Package).filter_by(id=receipt.package_id).one()
            category = db.session.query(Category).filter_by(id=package.category_id).one()
            package.receipt_no = receipt.receipt_no
            print(package)
            try:
                db.session.commit()
                print('commit')
            except Exception as e:
                print(e)
                db.session.rollback()

            a = ReceiptItem()
            a.quantity = 1
            a.receipt = receipt
            a.category = category
            a.description = f'{category.category_type} - {category.description}'
            a.price = a.category.price
            if receipt.coupon_code:
                a.apply_coupon = 'Yes'
                discount = db.session.execute("select discount from coupon where code='{}'".format(receipt.coupon_code)).scalar()
                a.discount = discount
                a.amount = a.price * a.quantity * (100 - discount) / 100
            else:
                a.apply_coupon = 'No'
                a.amount = a.price * a.quantity

            try:
                db.session.add(a)
                db.session.commit()
                print('commit')
            except Exception as e:
                print(e)
                db.session.rollback()

    @action("preview_receipt", "Preview Receipt", "", "fa-print", btnclass="btn-success", multiple=False)
    def preview_receipt(self, item):
        total = 0

        self.update_redirect()
        return self.render_template('receipt/one.html', receipt=item, total=total)

    @action("download_receipt", "Download Receipt", "", "fa-download", btnclass="btn-success", multiple=False, target='_blank')
    def download_receipt(self, item):
        total = 0

        html = self.render_template('receipt/one.html', receipt=item, total=total)
        css = CSS(string="""
                   @page {
                    size: a4 portrait;
                       margin: 5mm 5mm 5mm 5mm;
                   }
                   """)
        return render_pdf(HTML(string=html), stylesheets=[css],
                          download_filename=None, automatic_download=False)


class ReceiptCustomerView(ReceiptView):
    related_views = [ReceiptCustomerItemView]
    search_columns = ['receipt_no', 'receipt_date']

    add_columns = ['receipt_type', 'receipt_date', 'customer', 'appointment', 'package', 'coupon_code',
                   'payment_method', 'payment_reference']
    edit_columns = ['receipt_no', 'receipt_type', 'receipt_date', 'customer', 'coupon_code',
                    'payment_method', 'payment_reference', 'status']

    add_form_query_rel_fields = {'appointment': [['customer_id', FilterEqualFunction, get_customer_id_from_url],
                                                 ['receipt_no', FilterEqual, '-'],
                                                 ],
                                 'package': [['customer_id', FilterEqualFunction, get_customer_id_from_url],
                                             ['receipt_no', FilterEqual, '-'],
                                             ],
                                 }

    # edit_form_query_rel_fields = {'appointment': [['receipt_no', FilterEqualFunction, get_receipt_no_from_url]],
    #                               'package': [['receipt_no', FilterEqualFunction, get_receipt_no_from_url]]
    #                               }

    add_form_extra_fields = {
        'payment_method': SelectField('Payment Method', choices=get_choices('payment_method'),
                                      validators=[validators.DataRequired()],
                                      widget=CustomizeSelect2Widget(extra_classes="")),
        'receipt_type': SelectField('Receipt Type', choices=get_choices('receipt_type'),
                                    validators=[validators.DataRequired()],
                                    widget=CustomizeSelect2Widget(extra_classes="")),
    }

    edit_form_extra_fields = {
        'payment_method': SelectField('Payment Method', choices=get_choices('payment_method'),
                                      validators=[validators.DataRequired()],
                                      widget=CustomizeSelect2Widget(extra_classes="")),
        'status': SelectField('Is Void', choices=get_choices('is_void'),
                              validators=[validators.DataRequired()],
                              widget=CustomizeSelect2Widget(extra_classes="")),
        'appointment': StringField('Appointment', widget=BS3TextFieldROWidget()),
        'package': StringField('Package', widget=BS3TextFieldROWidget()),
        'receipt_type': StringField('Receipt Type', validators=[validators.DataRequired()],
                                    widget=BS3TextFieldROWidget(),),
        'receipt_no': StringField('Receipt No', widget=BS3TextFieldROWidget()),
    }

    validators_columns = {
        'coupon_code': [CouponCodeValidator(message='Invalid Coupon Code')],
        'appointment': [ReceiptTypeValidator(message='Invalid')],
        'package': [ReceiptTypeValidator(message='Invalid')]
    }

    @action("customer", "Back to Customer", "", "fa-user", btnclass="btn-warning", multiple=False)
    def customer(self, item):
        return redirect('/customerview/edit/{}'.format(str(item.customer_id)))


class ReceiptGeneralView(ReceiptView):
    related_views = [ReceiptGeneralItemView]
    search_columns = ['receipt_no', 'receipt_date']
    add_columns = ['receipt_type', 'receipt_date',  'coupon_code',
                   'payment_method', 'payment_reference']
    edit_columns = ['receipt_no', 'receipt_type', 'receipt_date', 'coupon_code',
                    'payment_method', 'payment_reference', 'status']

    add_form_extra_fields = {
        'payment_method': SelectField('Payment Method', choices=get_choices('payment_method'),
                                      validators=[validators.DataRequired()],
                                      widget=CustomizeSelect2Widget(extra_classes="")),
        'receipt_type': StringField('Receipt No', validators=[validators.DataRequired()], widget=BS3TextFieldROWidget(), default="General"),
    }

    edit_form_extra_fields = {
        'payment_method': SelectField('Payment Method', choices=get_choices('payment_method'),
                                      validators=[validators.DataRequired()],
                                      widget=CustomizeSelect2Widget(extra_classes="")),
        'status': SelectField('Is Void', choices=get_choices('is_void'),
                              validators=[validators.DataRequired()],
                              widget=CustomizeSelect2Widget(extra_classes="")),
        'receipt_type': StringField('Receipt Type', validators=[validators.DataRequired()], widget=BS3TextFieldROWidget(), default="General"),
        'receipt_no': StringField('Receipt No', widget=BS3TextFieldROWidget()),
    }

    validators_columns = {
        'coupon_code': [CouponCodeValidator(message='Invalid Coupon Code')],
    }

    base_filters = [['customer', FilterEqual, None]]

    pass

