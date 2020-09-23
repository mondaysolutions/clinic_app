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
from flask import send_file


class UploadsView(BaseView):

    @expose("/<string:filename>")
    @has_access
    def download(self, filename):
        return send_file(
            self.appbuilder.app.config["UPLOAD_FOLDER"] + filename,
            attachment_filename=None,
            as_attachment=False,
        )
