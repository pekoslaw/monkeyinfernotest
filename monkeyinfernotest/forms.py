
from datetime import datetime, date
from collections import OrderedDict

import django.forms.fields as fields
from django.forms.widgets import MultiWidget
from django.core.exceptions import ValidationError



class FormMetaclass(type):
    """Creates fields data for form Handler
    """
    
    def __init__(cls, name, bases, attrs):
        res = super(FormMetaclass, cls).__init__(name, bases, attrs)
        fds = OrderedDict()
        filtered_fields = []
        for name, field in attrs.items():
            if issubclass(field.__class__,fields.Field):
                filtered_fields.append([name, field])
        for name, field in sorted(filtered_fields, key=lambda x: cls.ORDER.index(x[0])):
            fds[name] = field
        cls.fields = fds
        return res
        
class GetSeter(object):
    """Allows dict like operation on field
    """
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
        
    def get(self, key):
        return getattr(self, key)
    
class CardExpirationWidget(MultiWidget):
    """Widget for credit card expiration date
    """
    def decompress(self, value):
        return [value.year, value.month] if value else [None, None]
    
    
class CardExpirationField(fields.MultiValueField, GetSeter):
    
    
    def __init__(self, *args, **kwargs):
        year = date.today().year
        flds = (fields.ChoiceField(label='year', choices=[(x,x) for x in range(year, year+10)]),
                     fields.ChoiceField(label='month', choices=[(x,str(x).zfill(2)) for x in range(1, 13)])
                    )
        super(CardExpirationField, self).__init__(
            fields = flds,
            *args,
            **kwargs
        )
        self.widget = CardExpirationWidget(widgets = [flds[0].widget, flds[1].widget])
    
    def clean(self, values):
        value = super(CardExpirationField, self).clean(values)
        d = date.today()
        if value < date(d.year, d.month, 1):
            raise ValidationError('Card expired')
        return value
    
    def compress(self, values):
        return date(int(values[0]), int(values[1]), 1)
    
class ReservationRangeWidget(MultiWidget):
    
    
    def decompress(self, value):
        return [value.year, value.month] if value else [None, None]
    
class ReservationRange(fields.MultiValueField, GetSeter):
    
    def __init__(self, *args, **kwargs):
        flds = (fields.DateField(label='Date from'),
                fields.DateField(label='Date to')
               )
        super(ReservationRange, self).__init__(
            fields = flds,
            *args,
            **kwargs
        )
        self.widget = ReservationRangeWidget(widgets = [flds[0].widget, flds[1].widget])
        
    def compress(self, values):
        
        return values
    
    def clean(self, values):
        value = super(ReservationRange, self).clean(values)
        start, end = value
        d = date.today()
        if start < date.today():
            raise ValidationError('Start can be today or in the future only')
        if start > end:
            raise ValidationError('End cannot be before start')
        return value

CAR_MODELS = (
        (1, 'Suzuki', ),
        (2, 'Polonez', ),
        )

def isdigit_validation(value):
    if not value.isdigit():
        raise ValidationError(u'Use numbers only')


#django fields with getitem setitem methods
class CharField(fields.CharField, GetSeter):pass

class ChoiceField(fields.ChoiceField, GetSeter):pass
    
class BooleanField(fields.BooleanField, GetSeter):pass
    
class CarRentalForm(object, metaclass=FormMetaclass):
    
    ORDER = ['first_name', 'last_name', 'credit_card_number',
             'expire_date', 'cvv', 'car_model', 'reservation',
             'accept_terms']
    
    first_name = CharField(label="First name", max_length=60)
    last_name = CharField(label="Last name", max_length=60)
    credit_card_number = CharField(label="Card number", min_length=13, max_length=16, validators =[isdigit_validation])
    expire_date = CardExpirationField(label="Expiration date")
    cvv = CharField(label='cvv', validators =[isdigit_validation])
    car_model = ChoiceField(label='Car model', choices=CAR_MODELS)
    reservation = ReservationRange(label='Reservation (from,to)')
    accept_terms = BooleanField(label="Accept terms", required=True)
    
    
    
    