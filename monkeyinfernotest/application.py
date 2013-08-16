
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.escape import json_decode
from tornado.template import Loader


from monkeyinfernotest.histogram import WordsHistogram



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
    ])