#!/usr/bin/env python

from distutils.core import setup


setup(name='monkeyinfernotest',
    version='0.1',
    packages=['monkeyinfernotest'],
    description='Money Inferno test',
    author=u'Piotr Kalmus',
    author_email='pckalmus@gmail.com',
    url='https://github.com/pekoslaw/monkeyinfernotest',
    keywords = ['tornado', 'angularjs'],
    requires = [
        'tornado (==3.1)',
        'simplejson'
        ]
    
)