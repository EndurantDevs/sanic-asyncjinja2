# -*- coding: utf-8 -*-
import pytest
from sanic import Sanic

from sanic_asyncjinja2 import SanicAsyncJinja2

import asyncio

from webtest_sanic import TestApp

import time

# creating test application
app = Sanic(__name__)
jinja = SanicAsyncJinja2()
jinja.init_app(app)


@app.route('/', methods=["GET", ])
@jinja.stream_template("hello.html")
def index(request):
    return {"name": "world"}


@app.route('/slow_query', methods=["GET", ])
@jinja.template("hello.html")
async def slow_handler(request):
    async def func1():
        await asyncio.sleep(2)
        return "name"

    async def func2():
        await asyncio.sleep(2)
        return "world"

    async def gfunc(k, v):
        key, value = await asyncio.gather(k, v)
        return {key: value}

    f1 = func1()
    f2 = func2()
    g = await gfunc(f1, f2)
    return g


# this is just a stupid idea
# to win the time to the first byte on reponse
# might be helpful for long responses
@app.route('/simplestream', methods=["GET", ])
@jinja.stream_template("hello.html")
def handler2(request):
    return {"name": "world"}


@pytest.fixture()
def wt():
    loop = asyncio.get_event_loop()
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


def test_time(wt):
    start = time.time()
    res = wt.get('/slow_query')
    end = time.time()
    assert res.status_code == 200
    expected = "Hello, world!"
    assert res.text == expected
    time_diff = end - start
    assert time_diff < 2.2
