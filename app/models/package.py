from flask_appbuilder.models.decorators import renders
from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from .base import StatusMixin
from app.models import Customer
from flask import Flask, g, request, session
from app import db


def get_customer_contact_no():
    a = request.url
    customer_id = int(a[a.find('=')+1:])
    customer = db.session.query(Customer).filter_by(id=customer_id).one()
    return customer.contact_no

    # try:
    #     return g.user.id
    # except Exception:
    #     return None


class Package(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")

    begin_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category")

    description = Column(String(100), nullable=False)

    sharing_mobile1 = Column(String(20), nullable=False, default=get_customer_contact_no)
    sharing_mobile2 = Column(String(20), nullable=True)
    sharing_mobile3 = Column(String(20), nullable=True)
    sharing_mobile4 = Column(String(20), nullable=True)
    sharing_mobile5 = Column(String(20), nullable=True)

    receipt_no = Column(String(10), nullable=False, default='-')
    ticket_count = Column(Integer, nullable=False)
    ticket_remaining = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.category} ({self.begin_date} - {self.end_date})'

    @renders('receipt_no')
    def receipt_no_display(self):
        if self.receipt_no:
            return self.receipt_no
        else:
            return '-'


class PackageTicket(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    package_id = Column(Integer, ForeignKey('package.id'), nullable=False)
    package = relationship("Package")

    mobile = Column(String(20), nullable=True)

    begin_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=True)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")

    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    appointment = relationship("Appointment")

    @renders('appointment_begin_datetime')
    def appointment_begin_datetime(self):
        return self.appointment.begin_datetime

    @renders('appointment_end_datetime')
    def appointment_end_datetime(self):
        return self.appointment.end_datetime

