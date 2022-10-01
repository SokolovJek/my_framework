from wsgiref.simple_server import make_server
from framework.main import Application
from urls import fronts
from patterns.creational_patterns import Logger
from patterns.structural_pattern import UrlDecorator

loger = Logger('run')
application = Application(routes=UrlDecorator.urls, fronts=fronts)

with make_server('', 8020, application) as httpd:
    loger.log('Serving on port 8020...')
    print('Serving on port 8020...')
    httpd.serve_forever()
