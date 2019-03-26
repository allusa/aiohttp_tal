from aiohttp import web

import aiohttp_tal


async def test_filters(aiohttp_client):

    @aiohttp_tal.template('tmpl.pt')
    async def index(request):
        return {}

    def add_2(value):
        return value + 2

    app = web.Application()
    aiohttp_tal.setup(
        app,
        loader={'tmpl.pt': "${ add_2(5) }"},
        filters={'add_2': add_2}
    )

    app.router.add_route('GET', '/', index)
    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert 200 == resp.status
    txt = await resp.text()
    assert '7' == txt
