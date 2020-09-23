from datetime import datetime, date

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.baseviews import BaseView, expose
from flask_wtf import FlaskForm
from flask_appbuilder import SimpleFormView
from flask import Response, make_response, flash
from io import StringIO, BytesIO
import mimetypes
import xlsxwriter
from datetime import datetime
from werkzeug.datastructures import Headers
from flask_appbuilder.forms import DynamicForm
from wtforms import Form, validators, StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, DateTimePickerWidget, DatePickerWidget
from flask_appbuilder.security.decorators import has_access, has_access_api, permission_name
from datetime import datetime
from .base_util import *


class ReportForm(DynamicForm):
    start_date = DateField('Start Date',
                           default=date.today,
                           format='%Y-%m-%d',
                           validators=[DataRequired(message="You need to enter the date in format YYYY-MM-DD.")],
                           widget=DatePickerWidget(extra_classes=""))
    end_date = DateField('End Date',
                         default=date.today,
                         format='%Y-%m-%d',
                         validators=[DataRequired(message="You need to enter the date in format YYYY-MM-DD.")],
                         widget=DatePickerWidget(extra_classes=""))
    # submit = SubmitField('Report')


class ReportView(SimpleFormView):
    # default_view = 'report'

    form = ReportForm
    form_title = 'Reports'
    message = 'My form submitted'

    def form_get(self, form):
        # form.field1.data = 'This was prefilled'
        # flash(self.message, 'info')
        pass

    @expose("/form", methods=["GET"])
    @has_access
    def this_form_get(self):
        self._init_vars()
        form = self.form.refresh()

        self.form_get(form)
        widgets = self._get_edit_widget(form=form, submit_name='Report')
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    def form_post(self, form):
        # post process form
        start_date = form.start_date.data
        end_date = form.end_date.data

        resource_query_day_balance = """
                                        select receipt_date, sum(total)
                                            from view_report_receipt
                                        group by
                                            receipt_date
                                        having receipt_date >= '{}' and receipt_date <= '{}' 
                                     """

        resource_query = """
                            select 
                                'MP' || receipt_no as receipt_no, receipt_date, physio_name, customer_name, contact_no, substr(hkid,1,4) || 'XXX' as hkid, date_of_birth,
                                payment_method, payment_reference, total
                            from view_report_receipt
                            where 1=1 
                            and receipt_date >= '{}'
                            and receipt_date <= '{}' 
                            order by receipt_no asc, receipt_date asc
                        """

        resource_query_items = """
                            select 
                                'MP' || receipt_no as receipt_no, receipt_date, physio_name, category_type, description, apply_coupon, coupon_code, 
                                original_price, actual_price
                            from view_report_receipt_item
                            where 1 = 1
                            and receipt_date >= '{}' 
                            and receipt_date <= '{}' 
                            order by receipt_no asc, receipt_date asc
                        """

        str_1 = get_csv_str(resource_query_day_balance, start_date, end_date)
        str_2 = get_csv_str(resource_query, start_date, end_date)
        str_3 = get_csv_str(resource_query_items, start_date, end_date)

        response = make_response(str_1 + '\n\n\n' + str_2 + '\n\n\n' + str_3)
        # cd = 'attachment; filename=report.csv'
        cd = 'inline; filename=report.csv'

        response.headers['Content-Disposition'] = cd
        response.mimetype = 'text/csv'
        return response

        # flash(self.message, 'info')

    # @expose('/report')
    # # @has_access
    # def report(self):
    #
    #     current_date = datetime.now().strftime("%Y-%m-%d")
    #
    #     self.update_redirect()
    #     return self.render_template('report/index.html',
    #                                 title="Report",
    #                                 current_date=current_date)

    # @action("download_certificate", "Download Certificate", "", "fa-download", btnclass="btn-info", multiple=False)
    # def download_invoice(self, item):
    #
    #     total = 0
    #     current_date = datetime.now().strftime("%Y-%m-%d")
    #     html = self.render_template('certificate/one.html', appointment=item, total=total, current_date=current_date)
    #     css = CSS(string="""
    #                        @page {
    #                         size: a4 portrait;
    #                            margin: 5mm 5mm 5mm 5mm;
    #                        }
    #                        """)
    #     return render_pdf(HTML(string=html), stylesheets=[css],
    #                       download_filename=None, automatic_download=False)

    # @expose('/csv', methods=['GET'])
    # def download_csv(self):
    #
    #     resource_query = """
    #                         select
    #                             id, first_name, last_name
    #                          from ab_user
    #                         """
    #     # where instrument = '{}'
    #     resource_cursor = db.session.execute(resource_query)
    #     resources = []
    #     for x in resource_cursor:
    #         resources.append(x['first_name'] + ' ' + x['last_name'])
    #
    #     csv = ','.join(resources)
    #     print(csv)
    #     # csv = 'foo,bar,baz\nhai,bai,crai\n'
    #     response = make_response(csv)
    #     # cd = 'attachment; filename=mycsv.csv'
    #     cd = 'inline; filename=mycsv.csv'
    #
    #     response.headers['Content-Disposition'] = cd
    #     response.mimetype = 'text/csv'
    #     return response
    #
    # @expose('/excel', methods=['GET'])
    # # @has_access
    # def download_excel(self):
    #     try:
    #         # Flask response
    #         response = Response()
    #         response.status_code = 200
    #
    #         # Create an in-memory output file for the new workbook.
    #         output = BytesIO()
    #
    #         # Craete workbook
    #         workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #         worksheet = workbook.add_worksheet('hello')
    #
    #         # Write some test data.
    #         worksheet.write(0, 0, 'Hello, world!')
    #
    #         # Close the workbook before streaming the data.
    #         workbook.close()
    #
    #         # Rewind the buffer.
    #         output.seek(0)
    #
    #         # Add output to response
    #         response.data = output.read()
    #
    #         # Set filname and mimetype
    #         file_name = 'export_{}_{}.xlsx'.format('this_awesome', datetime.now())
    #         mimetype_tuple = mimetypes.guess_type(file_name)
    #
    #         # HTTP headers for forcing file download
    #         response_headers = Headers({
    #             'Pragma': "public",  # required,
    #             'Expires': '0',
    #             'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
    #             'Cache-Control': 'private',  # required for certain browsers,
    #             'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #             'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
    #             'Content-Transfer-Encoding': 'binary',
    #             'Content-Length': len(response.data)
    #         })
    #
    #         if not mimetype_tuple[1] is None:
    #             response.update({
    #                 'Content-Encoding': mimetype_tuple[1]
    #             })
    #
    #         # Add headers
    #         response.headers = response_headers
    #
    #         # jquery.fileDownload.js requirements
    #         response.set_cookie('fileDownload', 'true', path='/')
    #
    #         # Return the response
    #         return response
    #
    #     except Exception as e:
    #         print(e)


