from wtforms.widgets.core import HTMLString, html_params, escape_html
from wtforms.compat import text_type, iteritems

from flask_babel import lazy_gettext as _

from wtforms.widgets import Input


class CustomInput(Input):
    input_type = None

    def __init__(self, input_type=None, **kwargs):
        self.params = kwargs
        super(CustomInput, self).__init__(input_type=input_type)

    def __call__(self, field, **kwargs):
        for param, value in self.params.iteritems():
            kwargs.setdefault(param, value)
        return super(CustomInput, self).__call__(field, **kwargs)


class CustomTextInput(CustomInput):
    input_type = 'text'


class CustomizeSelect(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        html = ['<select %s><option selected value="__None"></option>' % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        options = dict(kwargs, value=value)
        if selected:
            options['selected'] = True
        return HTMLString('<option %s>%s</option>' % (html_params(**options), escape_html(label, quote=False)))


class CustomizeSelect2Widget(CustomizeSelect):
    extra_classes = None

    def __init__(self, extra_classes=None, style=None):
        self.extra_classes = extra_classes
        self.style = style or u'width:400px'
        return super(CustomizeSelect2Widget, self).__init__()

    def __call__(self, field, **kwargs):
        kwargs['class'] = u'my_select2 form-control'
        if self.extra_classes:
            kwargs['class'] = kwargs['class'] + ' ' + self.extra_classes
        kwargs['style'] = self.style
        kwargs['data-placeholder'] = _('Select Value')
        if 'name_' in kwargs:
            field.name = kwargs['name_']
        return super(CustomizeSelect2Widget, self).__call__(field, **kwargs)
