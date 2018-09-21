# sanic-asyncjinja2
Jinja2 in async mode with Sanic [experimental]

[![Build Status](https://img.shields.io/travis/EndurantDevs/sanic-asyncjinja2.svg?logo=travis)](https://travis-ci.org/EndurantDevs/sanic-asyncjinja2) [![Latest Version](https://img.shields.io/pypi/v/sanic-asyncjinja2.svg)](https://pypi.python.org/pypi/sanic-asyncjinja2/) [![Python Versions](https://img.shields.io/pypi/pyversions/sanic-asyncjinja2.svg)](https://github.com/EndurantDevs/sanic-asyncjinja2/blob/master/setup.py) [![Tests Coverage](https://img.shields.io/codecov/c/github/EndurantDevs/sanic-asyncjinja2/master.svg)](https://codecov.io/gh/EndurantDevs/sanic-asyncjinja2)

It is based on [sanic-jinja2](https://github.com/lixxu/sanic-jinja2). 
It provides two decorators @template and @stream_template.
The main change is in using render_async and generate_async for the decorator functions.

@stream_template is just and experimental way to make HTTP response via sanic.response.stream
It gives you ability to decrease time to the first byte on response and stream long response during the processing template with data.

### Example code ###
```python
import asyncio
from sanic import Sanic
from sanic_asyncjinja2 import SanicAsyncJinja2


app = Sanic(__name__)
jinja = SanicAsyncJinja2()
jinja.init_app(app)


@app.route('/', methods=["GET", ])
@jinja.template("hello.html")
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
# to win the time to the first byte on response
# on one of our production servers
# it is helpful with big responses
@app.route('/simplestream', methods=["GET", ])
@jinja.stream_template("hello.html")
async def handler2(request):
    very_long_text = "Very long response here..." 
    return {"name": "world", "text": very_long_text}
```
