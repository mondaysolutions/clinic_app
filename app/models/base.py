from datetime import datetime
from sqlalchemy import Column, String, Date, Numeric

from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder.models.decorators import renders
from flask import Markup


class StatusMixin(AuditMixin):
    status = Column(String(1), default='A', nullable=False)

    # @renders('status')
    # def status_display(self):
    #     if self.status == 'A':
    #         return 'No'
    #     else:
    #         return 'Yes'

    @renders('is_void')
    def is_void(self):
        if self.status == 'A':
            return 'No'
        else:
            return 'Yes'


class InvoiceMixin(StatusMixin):
    invoice_date = Column(Date, default=datetime.today, nullable=False)
    payment = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=True)
    payment_reference = Column(String(20), nullable=True)
    payment_date = Column(Date, nullable=True)
    amount = Column(Numeric(8, 2), nullable=True)

    @renders('amount_display')
    def amount_display(self):
        if self.amount is None:
            return Markup(" - ")
        else:
            return Markup("$" + str(self.amount))

