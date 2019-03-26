import chameleon
import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

import aiohttp_tal


async def test_func(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>${head}</h1>${text}</body></html>'
    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', func)

    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_render_class_based_view(aiohttp_client):
    class MyView(web.View):
        @aiohttp_tal.template('tmpl.pt')
        async def get(self):
            return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', MyView)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_meth(aiohttp_client):

    class Handler:

        @aiohttp_tal.template('tmpl.pt')
        async def meth(self, request):
            return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    handler = Handler()

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', handler.meth)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_convert_func_to_coroutine(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', func)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_render_not_initialized():

    async def func(request):
        return aiohttp_tal.render_template('template', request, None)

    app = web.Application()

    app.router.add_route('GET', '/', func)

    req = make_mocked_request('GET', '/', app=app)
    msg = "Template engine is not initialized, " \
          "call aiohttp_tal.setup(..., app_key={}" \
          ") first".format(aiohttp_tal.APP_KEY)

    with pytest.raises(web.HTTPInternalServerError) as ctx:
        await func(req)

    assert msg == ctx.value.text


async def test_set_status(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt', status=201)
    async def func(request):
        return {'head': 'HEAD', 'text': 'text'}

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', func)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    assert 201 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_render_template(aiohttp_client):

    async def func(request):
        return aiohttp_tal.render_template(
            'tmpl.pt', request,
            {'head': 'HEAD', 'text': 'text'})

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', func)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_render_template_custom_status(aiohttp_client):

    async def func(request):
        return aiohttp_tal.render_template(
            'tmpl.pt', request,
            {'head': 'HEAD', 'text': 'text'}, status=404)

    template = '<html><body><h1>${head}</h1>${text}</body></html>'

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': chameleon.PageTemplate(template)
    })

    app.router.add_route('*', '/', func)

    client = await aiohttp_client(app)

    resp = await client.get('/')

    assert 404 == resp.status
    txt = await resp.text()
    assert '<html><body><h1>HEAD</h1>text</body></html>' == txt


async def test_template_not_found():

    async def func(request):
        return aiohttp_tal.render_template('template', request, {})

    app = web.Application()
    aiohttp_tal.setup(app, loader={})

    app.router.add_route('GET', '/', func)

    req = make_mocked_request('GET', '/', app=app)

    with pytest.raises(web.HTTPInternalServerError) as ctx:
        await func(req)

    t = "Template 'template' not found"
    assert t == ctx.value.text
    assert t == ctx.value.reason


async def test_render_not_mapping():

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return 123

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': 'tmpl'})

    app.router.add_route('GET', '/', func)

    req = make_mocked_request('GET', '/', app=app)
    msg = "context should be mapping, not <class 'int'>"
    with pytest.raises(web.HTTPInternalServerError) as ctx:
        await func(req)

    assert msg == ctx.value.text


# async def test_render_without_context(aiohttp_client):

#     @aiohttp_tal.template('tmpl.pt')
#     async def func(request):
#         pass

#     template = '<html><body><p>${text}</p></body></html>'

#     app = web.Application()
#     aiohttp_tal.setup(app, loader={
#         'tmpl.pt': chameleon.PageTemplate(template)
#     })

#     app.router.add_route('GET', '/', func)

#     client = await aiohttp_client(app)
#     resp = await client.get('/')

#     assert 200 == resp.status
#     txt = await resp.text()
#     assert '<html><body><p></p></body></html>' == txt


async def test_render_default_is_autoescaped(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return {'text': '<script>alert(1)</script>'}

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': '<html>${text}</html>'})

    app.router.add_route('GET', '/', func)

    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html>&lt;script&gt;alert(1)&lt;/script&gt;</html>' == txt


async def test_render_can_disable_autoescape(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return {'text': '<script>alert(1)</script>'}

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': '<html>${structure:text}</html>'})

    app.router.add_route('GET', '/', func)

    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert '<html><script>alert(1)</script></html>' == txt


async def test_render_bare_funcs_deprecated(aiohttp_client):

    def wrapper(func):
        async def wrapped(request):
            with pytest.warns(DeprecationWarning,
                              match='Bare functions are deprecated'):
                return await func(request)
        return wrapped

    @wrapper
    @aiohttp_tal.template('tmpl.pt')
    def func(request):
        return {'text': 'OK'}

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': '${text}'})

    app.router.add_route('GET', '/', func)

    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert 'OK' == txt


async def test_skip_render_for_response_from_handler(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def func(request):
        return web.Response(text='OK')

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': '${text}'})

    app.router.add_route('GET', '/', func)

    client = await aiohttp_client(app)
    resp = await client.get('/')

    assert 200 == resp.status
    txt = await resp.text()
    assert 'OK' == txt
