
import tornado.ioloop
from monkeyinfernotest.application import application

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()