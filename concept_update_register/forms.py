import json
from wtforms import Form, StringField, TextAreaField, validators

class JSONField(TextAreaField):
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        else:
            return self.data and unicode(json.dumps(self.data)) or u''

    def process_formdata(self, value):
        if value:
            try:
                self.data = json.loads(value[0])
            except ValueError:
                raise ValueError(self.gettext(u'Invalid JSON data.'))

class TitleForm(Form):
    title_id = StringField('Title ID', validators=[validators.input_required()])
    property_address = StringField('Property address', validators=[validators.input_required()])
    extent = JSONField('Extent (as GeoJSON)')
