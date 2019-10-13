import os, time
from datetime import datetime, timedelta
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
basedir = os.path.abspath(os.path.dirname(__file__))

# print(time.strftime('%X %x %Z'))
# now = datetime.now()
# print(now.strftime('%Y-%m-%d'))
os.environ['TZ'] = 'Asia/Hong_Kong'
time.tzset()
# print (time.strftime('%X %x %Z'))
#
# now = datetime.now()
# print(now.strftime('%Y-%m-%d'))

CSRF_ENABLED = True
SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/clinic.db') + '?check_same_thread=False'
# SQLALCHEMY_ECHO = True
#SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'

# BABEL_DEFAULT_LOCALE = 'en'

# LANGUAGES = {
#     'en': {'flag':'gb', 'name':'English'},
#     'pt': {'flag':'pt', 'name':'Portuguese'},
#     'es': {'flag':'es', 'name':'Spanish'},
#     'de': {'flag':'de', 'name':'German'},
#     'zh': {'flag':'cn', 'name':'Chinese'},
#     'ru': {'flag':'ru', 'name':'Russian'}
# }

#------------------------------
# GLOBALS FOR GENERAL APP's
#------------------------------
UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
FILE_ALLOWED_EXTENSIONS = ("txt", "pdf", "jpeg", "jpg", "gif", "png", "doc", "docx")

# IMG_SIZE = (150,150,True)

# FAB_ROLES = {
#     "ReadOnly": [
#         [".*", "can_list"],
#         [".*", "can_show"],
#         ["Patient", "menu_access"],
#         ["^Appointment$", "menu_access"],
#         [".*", "can_get"],
#         [".*", "can_info"],
#         [".*", "can_calendar"],
#     ],
#     "Public": [
#         [".*", "menu_access"],
#         [".*", "can_list"],
#         [".*", "can_calendar"],
#     ],
# }


FAB_ROLES = {
    "Customer": [
        # ["^Customer$", "menu_access"],
        # ["^Customers \(Customer\)$", "menu_access"],
        [".*", "can_this_form_get"],
        [".*", "can_this_form_post"],
        [".*", "can_list"],
        [".*", "can_get"],
        [".*", "can_info"],
        [".*", "can_show"],
        [".*", "can_add"],
        [".*", "can_edit"],
        [".*", "can_delete"]
    ],
    "Staff": [
        ["^Customer$", "menu_access"],
        ["^Customers \(Staff\)$", "menu_access"],
        ["Appointment", "menu_access"],
        ["Coupon", "menu_access"],
        ["Category", "menu_access"],
        ["Config", "menu_access"],
        ["Categories", "menu_access"],
        ["Report", "menu_access"],
        ["Receipt", "menu_access"],
        ["Setting", "menu_access"],
        ["Profile", "menu_access"],
        # ["^Security$", "menu_access"],
        # ["List.*", "menu_access"],
        # ["User.*", "menu_access"],
        [".*", "can_this_form_get"],
        [".*", "can_this_form_post"],
        [".*", "can_list"],
        [".*", "can_get"],
        [".*", "can_userinfo"],
        [".*", "resetmypassword"],
        [".*", "resetpasswords"],
        [".*", "userinfoedit"],
        [".*", "can_info"],
        [".*", "can_show"],
        [".*", "can_add"],
        [".*", "can_edit"],
        [".*", "can_delete"],
        [".*", "can_download"],
        [".*", "can_calendar"],
        [".*", "can_action"],
        [".*", "can_greeting"]
    ],
    "Physician": [
        ["^Customer$", "menu_access"],
        ["^Customers \(Physician\)$", "menu_access"],
        ["Appointment", "menu_access"],
        ["Coupon", "menu_access"],
        ["Category", "menu_access"],
        ["Configs", "menu_access"],
        ["Categories", "menu_access"],
        ["Report", "menu_access"],
        ["Receipt", "menu_access"],
        ["Setting", "menu_access"],
        ["Profile", "menu_access"],
        # ["^Security$", "menu_access"],
        # ["List.*", "menu_access"],
        # ["User.*", "menu_access"],
        [".*", "can_this_form_get"],
        [".*", "can_this_form_post"],
        [".*", "can_list"],
        [".*", "can_get"],
        [".*", "can_userinfo"],
        [".*", "resetmypassword"],
        [".*", "resetpasswords"],
        [".*", "userinfoedit"],
        [".*", "can_info"],
        [".*", "can_show"],
        [".*", "can_add"],
        [".*", "can_edit"],
        [".*", "can_delete"],
        [".*", "can_download"],
        [".*", "can_calendar"],
        [".*", "can_action"],
        [".*", "download_receipt"],
        [".*", "preview_receipt"],
        [".*", "download_certificate"],
        [".*", "preview_certificate"],
        [".*", "customer"],
        [".*", "appointment"],
        [".*", "receipt"],
        [".*", 'return_to_list'],
        [".*", "can_greeting"]
    ],
}

AUTH_USER_REGISTRATION = False
AUTH_TYPE = AUTH_DB
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
AUTH_ROLE_READONLY = 'ReadOnly'

APP_NAME = "Miracle Prehab & Sports Clinic"
# APP_NAME = "$"
APP_THEME = ""                  # default
#APP_THEME = "cerulean.css"      # COOL
#APP_THEME = "amelia.css"
#APP_THEME = "cosmo.css"
#APP_THEME = "cyborg.css"       # COOL
#APP_THEME = "flatly.css"
#APP_THEME = "journal.css"
#APP_THEME = "readable.css"
#APP_THEME = "simplex.css"
#APP_THEME = "slate.css"          # COOL
#APP_THEME = "spacelab.css"      # NICE
#APP_THEME = "united.css"
