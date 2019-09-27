import time
import re
from wtforms.validators import ValidationError

time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')


def is_time_format_re(s):
    return bool(time_re.match(s))


def is_time_format(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


class TimeRequired(object):

    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE)

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        value = field.data

        message = self.message
        if message is None:
            message = field.gettext('Invalid time format.')

        if not is_time_format(value):
            raise ValidationError(message)


