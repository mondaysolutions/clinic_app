import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Numeric, DateTime

from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from flask import Markup

from .base import StatusMixin


class Receipt(StatusMixin, Model):
    id = Column(Integer, primary_key=True)
    receipt_no = Column(String(50), nullable=False)

    receipt_type = Column(String(10), nullable=False)

    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=True)
    customer = relationship("Customer")

    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=True)
    appointment = relationship("Appointment")

    package_id = Column(Integer, ForeignKey('package.id'), nullable=True)
    package = relationship("Package")

    coupon_code = Column(String(50), nullable=True)
    receipt_date = Column(Date, default=datetime.date.today(), nullable=False)
    payment_method = Column(String(20), nullable=False)
    payment_reference = Column(String(50), nullable=True)

    receipt_items = relationship("ReceiptItem", cascade="all, delete-orphan")


class ReceiptItem(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    receipt = relationship("Receipt")

    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship("Category")

    package_id = Column(Integer, ForeignKey('package.id'), nullable=True)
    package = relationship("Package")

    description = Column(String(100), nullable=True)
    price = Column(Numeric(8, 2), nullable=True)

    quantity = Column(Integer, nullable=False, default=1)
    apply_coupon = Column(String(10), nullable=False)
    discount = Column(Numeric(8, 2), nullable=True)
    amount = Column(Numeric(8, 2), nullable=True)

    # def item_description(self):
    #     if self.category.category_type == 'Others':
    #         return '{} - {} - ${}'.format(self.category.category_type, self.description, self.price)
    #     else:
    #         if self.discount:
    #             return '{} - {} - ${} (Coupon Code - {}, discount {}%)'.format(self.category.category_type, self.category.description,
    #                                          self.category.price, self.receipt.appointment.coupon_code, int(self.discount))
    #         else:
    #             return '{} - {} - ${}'.format(self.category.category_type, self.category.description, self.category.price)

    def item_description(self):
        if self.discount:
            if self.discount == 100:
                return f'{self.description} - ${self.price} (Package Ticket, discount {int(self.discount)}%)'
            else:
                return f'{self.description} - ${self.price} (Coupon Code - {self.receipt.coupon_code}, discount {int(self.discount)}%)'
        else:
            return f'{self.description} - ${self.price}'

    @renders('description')
    def description_display(self):
        if self.description:
            return self.description
        else:
            return ''

    @renders('price')
    def price_display(self):
        if self.price:
            return f'${self.price}'
        else:
            return ''

    @renders('discount')
    def discount_display(self):
        if self.discount:
            return f'-{int(self.discount)}%'
        else:
            return ''

    @renders('amount')
    def amount_display(self):
        return f'${self.amount}'
        # if self.amount:
        #     return f'${self.amount}'
        # else:
        #     return ''


