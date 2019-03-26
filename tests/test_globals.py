import pytest
from aiohttp import web

import aiohttp_tal


def test_get_env():
    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': "tmpl"})

    env = aiohttp_tal.get_env(app)
    assert isinstance(env, aiohttp_tal.Environment)
    assert env is aiohttp_tal.get_env(app)


async def test_url(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def index(request):
        return {}

    async def other(request):
        return

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': "${ url('other', name='John_Doe')}"})

    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/user/{name}', other, name='other')
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '/user/John_Doe' == txt


async def test_url_with_query(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def index(request):
        return {}

    app = web.Application()
    aiohttp_tal.setup(app, loader={
        'tmpl.pt': "${ url('index', query_={'foo': 'bar'})}"})

    app.router.add_get('/', index, name='index')
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '/?foo=bar' == txt


async def test_url_int_param(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def index(request):
        return {}

    async def other(request):
        return

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': "${ url('other', arg=1)}"})

    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/uid/{arg}', other, name='other')
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '/uid/1' == txt


async def test_url_param_forbidden_type(aiohttp_client):

    async def index(request):
        with pytest.raises(TypeError,
                           match=(r"argument value should be str or int, "
                                  r"got arg -> \[<class 'bool'>\] True")):
            aiohttp_tal.render_template('tmpl.pt', request, {})
        return web.Response()

    async def other(request):
        return

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': "${ url('other', arg=True)}"})

    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/uid/{arg}', other, name='other')
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status


async def test_helpers_disabled(aiohttp_client):

    async def index(request):
        with pytest.raises(NameError,
                           match="url"):
            aiohttp_tal.render_template('tmpl.pt', request, {})
        return web.Response()

    app = web.Application()
    aiohttp_tal.setup(
        app,
        default_helpers=False,
        loader={'tmpl.pt': "${url('index')}"})

    app.router.add_route('GET', '/', index)
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status


async def test_static(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def index(request):
        return {}

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': "${ static('whatever.js') }"})

    app['static_root_url'] = '/static'
    app.router.add_route('GET', '/', index)
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '/static/whatever.js' == txt


async def test_static_var_missing(aiohttp_client, caplog):

    async def index(request):
        with pytest.raises(RuntimeError, match='static_root_url'):
            aiohttp_tal.render_template('tmpl.pt', request, {})
        return web.Response()

    app = web.Application()
    aiohttp_tal.setup(app, loader={'tmpl.pt': "${ static('whatever.js') }"})

    app.router.add_route('GET', '/', index)
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status  # static_root_url is not set
