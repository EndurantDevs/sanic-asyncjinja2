# -*- coding: utf-8 -*-
import re
from setuptools import setup

REQUIRES = [
    'sanic',
    'jinja2',
    'sanic-jinja2'
]

def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('sanic_asyncjinja2/__init__.py')

setup(
    name='sanic-asyncjinja2',
    version=__version__,
    description='Sanic integration with Jinja2 in async mode [experimental]',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Endurant Devs',
    author_email='info@endurantdevs.com',
    url='https://github.com/EndurantDevs/sanic-asyncjinja2',
    packages=['sanic_asyncjinja2'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-asyncio"],
    install_requires=REQUIRES,
    license='MIT',
    zip_safe=False,
    keywords='sanic-asyncjinja2 sanic jinja2 template',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
