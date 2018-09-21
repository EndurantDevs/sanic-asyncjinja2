import asyncio
import functools
from sanic_jinja2 import SanicJinja2
from sanic_jinja2 import update_request_context
from collections import Mapping

from sanic.response import StreamingHTTPResponse, HTTPResponse
from sanic.exceptions import ServerError
from sanic.views import HTTPMethodView

from jinja2 import TemplateNotFound


class SanicAsyncJinja2(SanicJinja2):
    def __init__(self, app=None, loader=None, pkg_name=None, pkg_path=None,
                 context_processors=None, **kwargs):
        kwargs.update({"enable_async": True})
        super().__init__(app, loader, pkg_name, pkg_path,
                         context_processors, **kwargs)

    @staticmethod
    def template(template_name, encoding='utf-8', headers=None, status=200):
        """Decorate web-handler to convert returned dict context into
        sanic.response.Response
        filled with template_name template.
        :param template_name: template name.
        :param request: a parameter from web-handler,
                        sanic.request.Request instance.
        :param context: context for rendering.
        """

        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                if asyncio.iscoroutinefunction(func):
                    coro = func
                else:
                    coro = asyncio.coroutine(func)

                context = await coro(*args, **kwargs)

                # wrapped function return HTTPResponse
                # instead of dict-like object
                if isinstance(context, HTTPResponse):
                    return context

                # wrapped function is class method
                # and got `self` as first argument
                if isinstance(args[0], HTTPMethodView):
                    request = args[1]
                else:
                    request = args[0]

                if context is None:
                    context = {}

                env = getattr(request.app, 'jinja_env', None)
                if not env:
                    raise ServerError(
                        "Template engine has not been initialized yet.",
                        status_code=500,
                    )
                try:
                    template = env.get_template(template_name)
                except TemplateNotFound as e:
                    raise ServerError(
                        "Template '{}' not found".format(template_name),
                        status_code=500,
                    )
                if not isinstance(context, Mapping):
                    raise ServerError(
                        "context should be mapping, not {}".format(
                            type(context)),
                        status_code=500,
                    )
                # if request.get(REQUEST_CONTEXT_KEY):
                #     context = dict(request[REQUEST_CONTEXT_KEY], **context)
                update_request_context(request, context)

                text = await template.render_async(context)

                content_type = "text/html; charset={}".format(encoding)

                return HTTPResponse(
                    text, status=status, headers=headers,
                    content_type=content_type
                )

            return wrapped

        return wrapper

    @staticmethod
    def stream_template(template_name, encoding='utf-8', headers=None, status=200):
        """Decorate web-handler to convert returned dict context into
        sanic.response.Response
        filled with template_name template.
        :param template_name: template name.
        :param request: a parameter from web-handler,
                        sanic.request.Request instance.
        :param context: context for rendering.
        """

        def wrapper(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                if asyncio.iscoroutinefunction(func):
                    coro = func
                else:
                    coro = asyncio.coroutine(func)

                context = await coro(*args, **kwargs)

                # wrapped function return HTTPResponse
                # instead of dict-like object
                if isinstance(context, HTTPResponse):
                    return context

                # wrapped function is class method
                # and got `self` as first argument
                if isinstance(args[0], HTTPMethodView):
                    request = args[1]
                else:
                    request = args[0]

                if context is None:
                    context = {}

                env = getattr(request.app, 'jinja_env', None)
                if not env:
                    raise ServerError(
                        "Template engine has not been initialized yet.",
                        status_code=500,
                    )
                try:
                    template = env.get_template(template_name)
                except TemplateNotFound as e:
                    raise ServerError(
                        "Template '{}' not found".format(template_name),
                        status_code=500,
                    )
                if not isinstance(context, Mapping):
                    raise ServerError(
                        "context should be mapping, not {}".format(
                            type(context)),
                        status_code=500,
                    )
                # if request.get(REQUEST_CONTEXT_KEY):
                #     context = dict(request[REQUEST_CONTEXT_KEY], **context)
                update_request_context(request, context)

                content_type = "text/html; charset={}".format(encoding)

                async def do_response(response):
                    async for chunk in template.generate_async(context):
                        await response.write(chunk)

                return StreamingHTTPResponse(
                    do_response, status=status, headers=headers,
                    content_type=content_type
                )

            return wrapped

        return wrapper
