import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Numeric, DateTime

from sqlalchemy.orm import relationship

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders
from flask import Markup, url_for

from app import appbuilder

from .base import StatusMixin


class CustomerDocument(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")

    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("CustomerDocumentView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def preview_image(self):
        return Markup(
            '<img src="'
            + appbuilder.app.config['IMG_UPLOAD_URL'] + str(self.file)
            + '">'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))


class MedicalHistory(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")

    operation = Column(String(100), nullable=True)
    operation_date = Column(String(50), nullable=True)
    cancer = Column(String(100), nullable=True)
    certificated_date = Column(String(50), nullable=True)

    heart_diseases = Column(String(10), nullable=True)
    diabetes = Column(String(10), nullable=True)
    dizziness = Column(String(10), nullable=True)
    allergy = Column(String(10), nullable=True)

    medicine_currently_taking = Column(String(100), nullable=True)
    emergency_medicine = Column(String(100), nullable=True)

    notes = Column(Text, nullable=True)


class Customer(StatusMixin, Model):
    id = Column(Integer, primary_key=True)

    salvation = Column(String(10), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    chinese_name = Column(String(20), nullable=True)

    date_of_birth = Column(String(10), nullable=True)
    hkid = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True)

    contact_no = Column(String(20), nullable=False)
    mobile_no = Column(String(20), nullable=True)
    emergency_contact = Column(String(20), nullable=True)

    referral_doctor = Column(String(50), nullable=True)
    source_of_referral = Column(String(50), nullable=True)

    appointments = relationship("Appointment", cascade="all, delete-orphan")
    packages = relationship("Package", cascade="all, delete-orphan")
    receipts = relationship("Receipt", cascade="all, delete-orphan")
    customer_documents = relationship("CustomerDocument", cascade="all, delete-orphan")
    medical_historys = relationship("MedicalHistory", cascade="all, delete-orphan")

    physician1_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    physician1 = relationship("User", foreign_keys=[physician1_id])

    physician2_id = Column(Integer, ForeignKey('ab_user.id'), nullable=True)
    physician2 = relationship("User", foreign_keys=[physician2_id])

    physician3_id = Column(Integer, ForeignKey('ab_user.id'), nullable=True)
    physician3 = relationship("User", foreign_keys=[physician3_id])

    physician4_id = Column(Integer, ForeignKey('ab_user.id'), nullable=True)
    physician4 = relationship("User", foreign_keys=[physician4_id])

    physician5_id = Column(Integer, ForeignKey('ab_user.id'), nullable=True)
    physician5 = relationship("User", foreign_keys=[physician5_id])

    def __repr__(self):
        return self.first_name + ' ' + self.last_name



