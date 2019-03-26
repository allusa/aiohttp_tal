.. currentmodule:: aiohttp_jinja2

Usage
=====

:mod:`aiohttp_tal` has the same API as :mod:`aiohttp_jinja2`. See https://aiohttp-jinja2.readthedocs.io/en/stable/#reference for more information.


It uses :mod:`chameleon` as template loader. See `chameleon.PageTemplate*` template classes, e.g:

* :class:`chameleon.PageTemplate` for TAL string input (default for `string` input)
* :class:`chameleon.PageTemplateFile` for TAL filename input
* :class:`chameleon.chameleon.PageTemplateLoader` for directory of TAL templates input


.. _initialization:

Initialization
--------------

Simple initialization::

   import chameleon
   import aiohttp_tal
   from aiohttp import web
   from pathlib import Path


   THIS_DIR = Path(__file__).parent

   app = web.Application()
   loader = chameleon.PageTemplateLoader(str(THIS_DIR / 'templates'))
   aiohttp_tal.setup(app, loader=loader)

where `loader` could also be a `dict` of template name and TAL input::

 loader = {'tmpl.pt': chameleon.PageTemplate('<html>${text}</html>')}

or directly the TAL `string` input::

 loader =  {'tmpl.pt': '<html>${text}</html>'}



Rendering
---------

Based on https://aiohttp-jinja2.readthedocs.io/en/stable/#usage and https://aiohttp-jinja2.readthedocs.io/en/stable/#default-globals.


After :ref:`initializing *TAL environment* <initialization>`, you may use template engine in your
:term:`web-handlers<web-handler>`. The most convenient way is to
decorate a :term:`web-handler`.

Using the function based web handlers::

    @aiohttp_tal.template('tmpl.pt')
    def handler(request):
        return {'name': 'Andrew', 'surname': 'Svetlov'}

Or the class-based views (:class:`aiohttp.web.View`)::

    class Handler(web.View):
        @aiohttp_tal.template('tmpl.pt')
        async def get(self):
            return {'name': 'Andrew', 'surname': 'Svetlov'}

On handler call the :func:`template` decorator will pass
returned dictionary ``{'name': 'Andrew', 'surname': 'Svetlov'}`` into
template named ``"tmpl.pt"`` for getting resulting HTML text.

If you need more complex processing (set response headers for example)
you may call :func:`render_template` function.

Using a function based web handler::

    async def handler(request):
        context = {'name': 'Andrew', 'surname': 'Svetlov'}
        response = aiohttp_tal.render_template('tmpl.pt',
                                               request,
                                               context)
        response.headers['Content-Language'] = 'ru'
        return response

Or, again, a class-based view (:class:`aiohttp.web.View`)::

    class Handler(web.View):
        async def get(self):
            context = {'name': 'Andrew', 'surname': 'Svetlov'}
            response = aiohttp_tal.render_template('tmpl.pt',
                                                   self.request,
                                                   context)
            response.headers['Content-Language'] = 'ru'
            return response

Context processors is a way to add some variables to each
template context. It works like :attr:`aiohttp_tal.Environment().globals`,
but calculate variables each request. So if you need to
add global constants it will be better to use
:attr:`aiohttp_tal.Environment().globals` directly. But if you variables depends of
request (e.g. current user) you have to use context processors.

Context processors is following last-win strategy.
Therefore a context processor could rewrite variables delivered with
previous one.

In order to use context processors create required processors::

    async def foo_processor(request):
        return {'foo': 'bar'}

And pass them into :func:`setup`::

    aiohttp_tal.setup(
        app,
        context_processors=[foo_processor,
                            aiohttp_tal.request_processor],
        loader=loader)

As you can see, there is a built-in :func:`request_processor`, which
adds current :class:`aiohttp.web.Request` into context of templates
under ``'request'`` name.

Here is an example of how to add current user dependant logic
to template (requires ``aiohttp_security`` library)::

    from aiohttp_security import authorized_userid

    async def current_user_ctx_processor(request):
        userid = await authorized_userid(request)
        is_anonymous = not bool(userid)
        return {'current_user': {'is_anonymous': is_anonymous}}

Template::

    <body>
        <div>
            <a tal:condition="current_user.is_anonymous" href="${url('login')}">Login</a>
            <a tal:condition="not:current_user.is_anonymous"  href="${url('logout')}">Logout</a>
        </div>
    </body>


Default Globals
...............

.. highlight:: html+jinja

``app`` is always made in templates via :attr:`aiohttp_tal.Environment().globals`::

    <body>
        <h1>Welcome to ${app['name']}</h1>
    </body>


Two more helpers are also enabled by default: ``url`` and ``static``.

``url`` can be used with just a view name::

    <body>
        <a href="${url('index')}">Index Page</a>
    </body>


Or with arguments::

    <body>
        <a href="${url('user', id=123)}">User Page</a>
    </body>

A query can be added to the url with the special ``query_`` keyword argument::

    <body>
        <a href="${url('user', id=123, query_={'foo': 'bar'})}">User Page</a>
    </body>


For a view defined by ``app.router.add_get('/user-profile/{id}/',
user, name='user')``, the above would give::

    <body>
        <a href="/user-profile/123/?foo=bar">User Page</a>
    </body>


This is useful as it would allow your static path to switch in
deployment or testing with just one line.

The ``static`` function has similar usage, except it requires you to
set ``static_root_url`` on the app

.. code-block:: python

    app = web.Application()
    aiohttp_tal.setup(app,
        loader=chameleon.PageTemplateLoader('/path/to/templates/folder'))
    app['static_root_url'] = '/static'

Then in the template::

        <script src="${static('dist/main.js')}"></script>


Would result in::

        <script src="/static/dist/main.js"></script>


Both ``url`` and ``static`` can be disabled by passing
``default_helpers=False`` to ``aiohttp_tal.setup``.

