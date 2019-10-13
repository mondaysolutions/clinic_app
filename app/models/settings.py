from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Numeric, DateTime
from .base import StatusMixin


class Coupon(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    code = Column(String(20), nullable=False)
    expiry_date = Column(Date, nullable=False)
    is_multiple = Column(String(10), default="No", nullable=False)
    coupon_status = Column(String(20), default="Open", nullable=False)
    discount = Column(Integer, nullable=False)

    def __repr__(self):
        return self.code

    @renders('discount')
    def discount_display(self):
        if self.discount:
            return str(self.discount) + '%'
        else:
            return ''


class Category(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    category_type = Column(String(20), nullable=False)
    description = Column(String(50), nullable=False)
    price = Column(Numeric(8, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    expiry_date = Column(Date, nullable=False)

    def category_label(self):
        return self.description + ' ' + self.price

    def price_label(self):
        return f'${self.price}'

    def __repr__(self):
        return f'{self.category_type} - {self.description} - ${self.price}'


class Config(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    key = Column(String(20), nullable=False)
    value = Column(String(50), nullable=False)
