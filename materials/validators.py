from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is not None:
            if 'youtube.com' not in tmp_val.split('/'):
                raise ValidationError('You can write only youtube-url')


class PayValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        tmp_val1 = dict(value).get(self.field1)
        tmp_val2 = dict(value).get(self.field2)
        if tmp_val1 is None and tmp_val2 is None:
            raise ValidationError('You have to fill course or lesson id')
        if tmp_val1 is not None and tmp_val2 is not None:
            raise ValidationError('You filled both of fields, but have to fill one of them')
