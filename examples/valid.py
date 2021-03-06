from pathlib import Path

from aiohttp import web
import aiohttp_tal
from chameleon import PageTemplateLoader


THIS_DIR = Path(__file__).parent


@aiohttp_tal.template('index.html')
async def index(request):
    return {
        'title': request.app['name'],
        'intro': "Success! you've setup a basic aiohttp app with TAL.",
        }


@aiohttp_tal.template('valid.html')
async def page(request):
    return {
        'title': 'Valid W3C page',
        'intro': "Validated on https://validator.w3.org",
        }


async def create_app():
    app = web.Application()
    app.update(name='Testing aiohttp TAL')

    tal_loader = PageTemplateLoader(str(THIS_DIR / 'templates'),
                                    enable_data_attributes=True,  # data-tal-*
                                    auto_reload=True  # debugging
                                    )
    aiohttp_tal.setup(app, loader=tal_loader)

    app.add_routes([web.static('/static', str(THIS_DIR / 'static'))])
    app['static_root_url'] = '/static'
    app.router.add_get('/', index, name='index')
    app.router.add_get('/page', page, name='translation')

    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=8080)
