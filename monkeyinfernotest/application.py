
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.escape import json_decode
from tornado.template import Loader
import django.conf; django.conf.settings.configure()    # Disable django settings
import django.utils.encoding

from monkeyinfernotest.histogram import WordsHistogram
from monkeyinfernotest.forms import CarRentalForm

class FormHandler(RequestHandler):
    
    def setup(self):
        self.loader = Loader("monkeyinfernotest/templates")
        self.tmpl={}
        self.rental_fields = CarRentalForm().fields
        self.args = self.rental_fields.keys()
    
    
    def get(self):
        self.setup()
        self.validate_form({k : None for k in self.args}, 'rental_fields')
        
        data = self.loader.load("carrental.html").generate(data=self, check=False)
        self.write(data)
        
    def post(self):
        self.setup()
        request = self.get_request_data()
        self.validate_form(request, 'rental_fields')
        
        data = self.loader.load("carrental.html").generate(data=self, check=True)
        self.write(data)
    
    def get_request_data(self):
        """Creates request data for validate form
        """
        result = {}
        for key, field in self.rental_fields.items():
            if hasattr(field, 'fields'):
                result[key] = []
                for index in range(len(field.fields)):
                    result[key].append(self.get_argument(key+'_'+str(index), default=None))
            else:
                result[key] = self.get_argument(key, default=None)
            
        return result
        
    
    def validate_form(self, request, form_fields):
        self.tmpl['validated'] = True
        for name, field in getattr(self, form_fields).items():
            field['value'] = request.get(name, None)
            try:
                field['cleaned'] = field.clean(field['value'])
                field['valid'] = True
            except django.forms.fields.ValidationError as ex:
                field['valid'] = False
                field['error_msg'] = ex.messages[0]
            except django.utils.encoding.DjangoUnicodeDecodeError as ex:
                log.exception(ex)
                field['valid'] = False
                field['error_msg'] = ex.message
        self.form_valid = False not in [v['valid'] for f, v in getattr(self, form_fields).items()]
        return self.form_valid

    def field_class(self, field_name, form_fields):
        if getattr(self, form_fields)[field_name] and not getattr(self, form_fields)[field_name].get('valid'):
            return ' invalid'
        return ''

    def field_value(self, field_name, form_fields):
        value = getattr(self, form_fields)[field_name].get('value')
        if value == 0:
            value = 0
        elif value in [None, False]:
            value = ''
        return value
    
    def field_error(self, field_name, form_fields):
        return getattr(self, form_fields)[field_name].get('error_msg') or ''


class MainHandler(RequestHandler):
    """Rendering main page
    """
    
    def get(self):
        loader = Loader("monkeyinfernotest/templates")
        data = loader.load("index.html").generate()
        self.write(data)
        
class AjaxHandler(RequestHandler):
    """Sort data for javascript request
    """
    
    def post(self):
        data = json_decode(self.request.body)
        histogram = WordsHistogram(data['article'])
        self.write(histogram.to_json())
    
        
application = Application([
        (r"/$", MainHandler),
        (r"/static/(.*)", StaticFileHandler, {"path": "monkeyinfernotest/staticfiles"}),
        (r"/ajax/$", AjaxHandler),
        (r"/carrental/$", FormHandler),
    ])