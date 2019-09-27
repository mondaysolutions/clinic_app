import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Numeric, DateTime

from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from flask import Markup

from .base import StatusMixin


class AppointmentRequest(StatusMixin, Model):

    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=True)
    customer = relationship("Customer")

    physician_id = Column(Integer, ForeignKey('ab_user.id'), nullable=True)
    physician = relationship("User", foreign_keys=[physician_id])

    begin_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=True)

    salvation = Column(String(10), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    contact_no = Column(String(20), nullable=False)


class Appointment(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")

    physician_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    physician = relationship("User", foreign_keys=[physician_id])

    begin_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=True)

    # coupon_id = Column(Integer, ForeignKey('coupon.id'), nullable=True)
    # coupon = relationship("Coupon")

    referral_doctor = Column(String(50), nullable=True)
    source_of_referral = Column(String(50), nullable=True)

    sick_leave = Column(String(50), nullable=True)

    insurance_cover = Column(String(50), nullable=True)
    injury_due_to = Column(String(100), nullable=True)
    facilities_booking = Column(String(50), nullable=True)

    diagnosis = Column(Text, nullable=True)
    receipt_no = Column(String(10), nullable=False, default='-')

    color_code = Column(String(10), nullable=True)

    def __repr__(self):
        return f'{self.begin_datetime} - {self.end_datetime}'

    @renders('receipt_no')
    def receipt_no_display(self):
        if self.receipt_no:
            return self.receipt_no
        else:
            return '-'

