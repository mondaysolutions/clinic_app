import io
import csv

from datetime import datetime, timedelta

from wtforms.validators import ValidationError
from flask import Flask, g, request, session
from app import db
from wtforms import IntegerField, FloatField
from flask_appbuilder.models.sqla.filters import FilterEqualFunction, FilterStartsWith, FilterEqual, FilterNotEqual, \
                                                 BaseFilter, BaseFilterConverter, FilterRelation, FilterGreater

from sqlalchemy import or_, desc, asc
from app.models import Customer, Coupon, Category, Receipt, Package


def get_now():
    return datetime.now()


def get_user():
    return g.user


def get_user_id():
    return g.user.id


def get_customer_id_from_url():
    a = request.url
    return int(a[a.find('=')+1:])


def get_receipt_id_from_url():
    a = request.url
    return int(a[a.find('=')+1:])
    # return 1


def get_receipt_no_from_url():
    a = request.url
    receipt_id = int(a[a.rfind('/') + 1:a.find('?')])
    receipt = db.session.query(Receipt).filter_by(id=receipt_id).one()
    return receipt.receipt_no


# def get_category_id_from_url():
class FilterPackageFunction(BaseFilter):
    name = "Filter category with a function"
    arg_name = "eqf"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        receipt_id = func()
        receipt = db.session.query(Receipt).filter_by(id=receipt_id).one()
        customer = db.session.query(Customer).filter_by(id=receipt.customer_id).one()
        # packages = db.session.query(Package).filter(or_(Package.sharing_mobile1 == customer.contact_no,
        #                                                 Package.sharing_mobile2 == customer.contact_no,
        #                                                 Package.sharing_mobile3 == customer.contact_no,
        #                                                 Package.sharing_mobile4 == customer.contact_no,
        #                                                 Package.sharing_mobile5 == customer.contact_no, ))
        # return packages
        return query.filter(or_(Package.sharing_mobile1 == customer.contact_no,
                         Package.sharing_mobile2 == customer.contact_no,
                         Package.sharing_mobile3 == customer.contact_no,
                         Package.sharing_mobile4 == customer.contact_no,
                         Package.sharing_mobile5 == customer.contact_no, ))


        # if receipt.receipt_type == 'General':
        #     return query.filter(field == 'Products')
        #
        # elif receipt.receipt_type == 'Appointment':
        #     q1 = query.filter(or_(field == 'Services', field == 'Products'))
        #
        #     customer = db.session.query(Customer).filter_by(id=receipt.customer_id).one()
        #     packages = db.session.query(Package).filter(Package.ticket_count > 0,
        #                                                 or_(Package.sharing_mobile1 == customer.contact_no,
        #                                                     Package.sharing_mobile2 == customer.contact_no,
        #                                                     Package.sharing_mobile3 == customer.contact_no,
        #                                                     Package.sharing_mobile4 == customer.contact_no,
        #                                                     Package.sharing_mobile5 == customer.contact_no, ))
        #     re
        #     q2 = None
        #     for p in packages:
        #         q = query.filter(Category.id == p.category_id)
        #         if q2:
        #             q2 = q2.union(q)
        #         else:
        #             q2 = q
        #
        #     if q2:
        #         q2 = q2.union(q1)
        #     else:
        #         q2 = q1
        #
        #     return q2.order_by(asc(Category.category_type))
        #
        # elif receipt.receipt_type == 'Package':
        #     package = db.session.query(Package).filter_by(receipt_no=receipt.receipt_no).one()
        #     return query.filter(Category.id == package.category_id)


class FilterCategoryFunction(BaseFilter):
    name = "Filter category with a function"
    arg_name = "eqf"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        receipt_id = func()
        receipt = db.session.query(Receipt).filter_by(id=receipt_id).one()

        if receipt.receipt_type == 'General':
            return query.filter(field == 'Products')

        elif receipt.receipt_type == 'Appointment':
            q1 = query.filter(or_(field == 'Services', field == 'Products'))
            return q1
            # customer = db.session.query(Customer).filter_by(id=receipt.customer_id).one()
            # packages = db.session.query(Package).filter(Package.ticket_count > 0,
            #                                             or_(Package.sharing_mobile1 == customer.contact_no,
            #                                                 Package.sharing_mobile2 == customer.contact_no,
            #                                                 Package.sharing_mobile3 == customer.contact_no,
            #                                                 Package.sharing_mobile4 == customer.contact_no,
            #                                                 Package.sharing_mobile5 == customer.contact_no,)).all()
            # q2 = None
            # for p in packages:
            #     q = query.filter(Category.id == p.category_id)
            #     if q2:
            #         q2 = q2.union(q)
            #     else:
            #         q2 = q
            #
            # if q2:
            #     q2 = q2.union(q1)
            # else:
            #     q2 = q1
            #
            # return q2.order_by(asc(Category.category_type))

        elif receipt.receipt_type == 'Package':
            package = db.session.query(Package).filter_by(receipt_no=receipt.receipt_no).one()
            return query.filter(Category.id == package.category_id)


class CustomizeIntegerField(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                if valuelist[0]:
                    self.data = int(valuelist[0])
                else:
                    self.data = None
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid integer value'))


class CustomizeFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                if valuelist[0]:
                    self.data = float(valuelist[0])
                else:
                    self.data = None
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))


class SharingMobileValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        value = field.data
        message = self.message
        if value:
            count = db.session.execute("select count(1) from customer where contact_no=:contact_no and status='A'", {'contact_no': value}).scalar()
            if count == 0:
                raise ValidationError(message)


class PassCodeValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):

        if form.data['pass_code']:
            pass_code = db.session.execute(
                    "select value from config where key=:key and status='A'", {'key': 'pass_code'}).scalar()
            if form.data['pass_code'] == pass_code:
                pass
            else:
                raise ValidationError("Please fill the right pass code")


class ReceiptItemValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if request.url.find('/add') != -1:
            a = 0
            if form.data['category']:
                a = a + 1
            try:
                if form.data['package']:
                    a = a + 1
            except KeyError as e:
                print(str(e))

            if form.data['description']:
                a = a + 1
            if a != 1:
                raise ValidationError("Select either Category / Package or fill in Description")


class ReceiptItemPriceValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if request.url.find('/add') != -1:
            if form.data['description'] and form.data['price'] is None:
                raise ValidationError("Please fill in the Price if Description is filled")


class ReceiptItemDescriptionValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if request.url.find('/add') != -1:
            if form.data['category'] and form.data['description'] != '':
                raise ValidationError("Select either Category or fill in Description")


class ReceiptItemCategoryValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if request.url.find('/add') != -1:
            if form.data['category'] and form.data['description'] != '':
                raise ValidationError("Select either Category or fill in Description")
            elif form.data['category'] is None and form.data['description'] == '':
                raise ValidationError("Select either Category or fill in Description")


class ReceiptTypeValidator(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.name == 'appointment':
            if form.data['appointment'] is None and form.data['receipt_type'] == 'Appointment':
                raise ValidationError("Select Appointment")
            elif form.data['appointment']:
                if form.data['receipt_type'] != 'Appointment':
                    raise ValidationError("Receipt Type not match")
        elif field.name == 'package':
            if form.data['package'] is None and form.data['receipt_type'] == 'Package':
                raise ValidationError("Select Package")
            elif form.data['package']:
                if form.data['receipt_type'] != 'Package':
                    raise ValidationError("Receipt Type not match")


class CouponCodeValidator(object):
    """
    Validates an email address. Note that this uses a very primitive regular
    expression and should only be used in instances where you later verify by
    other means, such as email activation or lookups.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        value = field.data
        message = self.message
        if value:
            count = db.session.execute("select count(1) from coupon where code=:code and status='A' and expiry_date > datetime('now')", {'code': value.upper()}).scalar()
            if count == 0:
                raise ValidationError(message)
        #
        # user_part, domain_part = value.rsplit('@', 1)
        #
        # if not self.user_regex.match(user_part):
        #     raise ValidationError(message)
        #
        # if not self.validate_hostname(domain_part):
        #     raise ValidationError(message)


def get_today():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')


def get_csv_str(query, start_date, end_date):
    output = io.StringIO()

    resource_cursor = db.session.execute(query.format(start_date, end_date))
    fieldnames = resource_cursor.keys();
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for x in resource_cursor:
        d = dict()
        for fieldname in fieldnames:
            d[fieldname] = x[fieldname]
        writer.writerow(d)
    return output.getvalue()


def get_field_setup_query(query, model, column_name):
    """
        Help function for SQLA filters, checks for dot notation on column names.
        If it exists, will join the query with the model
        from the first part of the field name.

        example:
            Contact.created_by: if created_by is a User model,
            it will be joined to the query.
    """
    if not hasattr(model, column_name):
        # it's an inner obj attr
        rel_model = getattr(model, column_name.split(".")[0]).mapper.class_
        query = query.join(rel_model)
        return query, getattr(rel_model, column_name.split(".")[1])
    else:
        return query, getattr(model, column_name)


