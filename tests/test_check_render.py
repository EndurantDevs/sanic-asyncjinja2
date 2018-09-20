# -*- coding: utf-8 -*-
import asyncio
import json
import pytest
from sanic import Sanic

from sanic_asyncjinja2 import SanicAsyncJinja2

import asyncio

from webtest_sanic import TestApp

loop = asyncio.get_event_loop()

# creating test application
app = Sanic(__name__)
jinja = SanicAsyncJinja2()
jinja.init_app(app)


@app.route('/', methods=["GET", ])
@jinja.template("hello.html")
def handler(request):
    return {"name": "world"}

@app.route('/simplestream', methods=["GET", ])
@jinja.stream_template("hello.html")
def handler(request):
    return {"name": "world"}



# @app.route('/echo_post', methods=["POST", ])
# def echo_post(request):
#     form_body = request.form
#     return J(form_body)
#
#
# @app.route('/echo_json', methods=["POST", ])
# def echo_json(request):
#     json_body = request.json
#     return J(json_body)
#
#
# @app.route('/echo_headers', methods=["GET", ])
# def echo_headers(request):
#     # just an enough wrong way to split MultiDict with unique keys into dict
#     result = {}
#     for key in request.headers:
#         result[key] = request.headers.get(key)
#     return J(result)
#
#
# @app.route('/echo_params', methods=["GET", ])
# def echo_params(request):
#     return J(request.args)


@pytest.fixture()
def wt():
    return TestApp(app, loop=loop)


def test_get(wt):
    res = wt.get('/')
    assert res.status_code == 200
    expected = "Hello, world!"
    assert res.text == expected

def test_stream(wt):
    res = wt.get('/simplestream')
    assert res.status_code == 200
    expected = "Hello, world!"
    assert res.text == expected

# def test_post_form(wt):
#     res = wt.post('/echo_post', {'name': ['Steve']})
#     assert res.json == {'name': ['Steve']}
#
#
# def test_post_json(wt):
#     res = wt.post_json('/echo_json', {'name': 'Steve'})
#     assert res.json == {'name': 'Steve'}
#
#
# def test_headers(wt):
#     res = wt.get('/echo_headers', headers={'X-Foo': 'Bar'})
#     assert res.json['x-foo'] == 'Bar'
#
#
# def test_params(wt):
#     res = wt.get('/echo_params?foo=bar')
#     assert res.json == {'foo': ['bar']}
