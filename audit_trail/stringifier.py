from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import formats


class ModelFieldStringifier(object):

    custom_stringify_methods = {
        models.DateTimeField: 'stringify_datetime',
        models.DateField: 'stringify_date',
        models.ForeignKey: 'stringify_fk'
    }

    @classmethod
    def stringify(cls, field, value=None):
        value = value
        field_class = field.__class__

        if field_class in cls.custom_stringify_methods:
            stringifier = cls.custom_stringify_methods[field_class]

            if isinstance(stringifier, basestring):
                stringifier = getattr(cls, stringifier)

            return stringifier(value, field)

        if value is None:
            return None

        if getattr(field, 'choices', None):
            try:
                return unicode(dict(field.choices)[value])
            except KeyError:
                return unicode(value)
            except Exception, e:
                raise

        return unicode(value)

    @staticmethod
    def stringify_datetime(value, *args):
        if value is None:
            return None
        return formats.date_format(value, "DATETIME_FORMAT")

    @staticmethod
    def stringify_date(value, *args):
        if value is None:
            return None
        return formats.date_format(value, "DATE_FORMAT")

    @staticmethod
    def stringify_fk(value, field):
        if value is None:
            return None

        # if it's not model instance we assume it's an id
        if not isinstance(value, field.related_model):
            try:
                value = field.related_model.objects.get(id=value)
            except ObjectDoesNotExist:
                return None

        return unicode(value)

    @classmethod
    def add_stringifier(cls, field_class, callback):
        cls.custom_stringify_methods[field_class] = callback

