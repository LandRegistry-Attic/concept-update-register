import json
from wtforms import Form, StringField, TextAreaField, validators, FormField, FieldList

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

class RegisteredOwnerForm(Form):
    name = StringField('Name')
    address = StringField('Address')

class LenderForm(Form):
    name = StringField('Name')

class RelatedTitleForm(Form):
    title_number = StringField('Title Number')

class TitleForm(Form):
    title_id = StringField('Title ID', validators=[validators.input_required()])
    address = StringField('Address', validators=[validators.input_required()])
    extent = JSONField('Extent (as GeoJSON)')
    registered_owners = FieldList(FormField(RegisteredOwnerForm), min_entries=2)
    lenders = FieldList(FormField(LenderForm), min_entries=2)
    related_titles = FieldList(FormField(RelatedTitleForm), min_entries=5)
