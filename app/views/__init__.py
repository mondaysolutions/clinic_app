from app import appbuilder

from .report import *
from .settings import *
from .receipt import *
from .appointment import *
from .package import *
from .customer import *


def get_user():
    return g.user


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


db.create_all()

appbuilder.add_view_no_menu(ReceiptGeneralItemView, "ReceiptGeneralItemView")
appbuilder.add_view_no_menu(ReceiptCustomerItemView, "ReceiptCustomerItemView")
appbuilder.add_view_no_menu(CustomerDocumentView, "CustomerDocumentView")
appbuilder.add_view_no_menu(MedicalHistoryView, "MedicalHistoryView")
appbuilder.add_view_no_menu(AppointmentView, "AppointmentView")
appbuilder.add_view_no_menu(PackageView, "PackageView")
appbuilder.add_view_no_menu(PackageTicketView, "PackageTicketView")
appbuilder.add_view_no_menu(ReceiptCustomerView, "ReceiptCustomerView")


appbuilder.add_view(CustomerView, "Customers (Physician)", icon="", category="Customer")
appbuilder.add_view(CustomerStaffView, "Customers (Staff)", icon="", category="Customer")
appbuilder.add_view(AppointmentCalendarView, "Appointment Calendar", icon="", category="Appointment")
appbuilder.add_view(AppointmentRequestView, "Appointment Request", icon="", category="Appointment")
appbuilder.add_view(ReceiptGeneralView, "Receipts", icon="", category="Receipt")
appbuilder.add_view(CouponView, "Coupons", icon="", category="Settings")
appbuilder.add_view(CategoryView, "Categories", icon="", category="Settings")
appbuilder.add_view(ReportView, "Reports", icon="", category="Report")

appbuilder.add_api(ExampleApi)