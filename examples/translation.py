"""

First time:

* pybabel extract -F babel.cfg -o locales/mydomain.pot .
* pybabel init -D mydomain -i locales/mydomain.pot -d locales -l ca
* pybabel init -D mydomain -i locales/mydomain.pot -d locales -l fr_fr
* pybabel compile -D mydomain -d locales

Updates:

* pybabel extract -F babel.cfg -o locales/mydomain.pot .
* pybabel update -D mydomain -i locales/mydomain.pot -d locales
* pybabel compile -D mydomain -d locales

"""
from pathlib import Path

from aiohttp import web
from aiohttp_babel.locale import load_gettext_translations, set_default_locale
from aiohttp_babel.middlewares import babel_middleware, _
import aiohttp_tal
from chameleon import PageTemplateLoader


THIS_DIR = Path(__file__).parent

set_default_locale('en_GB')
load_gettext_translations(str(THIS_DIR / 'locales'), 'mydomain')


@aiohttp_tal.template('index.html')
async def index(request):
    return {
        'title': request.app['name'],
        'intro': "Success! you've setup a basic aiohttp app with TAL.",
        }


@aiohttp_tal.template('translation.html')
async def translation(request):
    return {
        'title': _('First page'),
        'request': request,
        }


def translate(msgid, domain=None, mapping=None, context=None,
              target_language=None, default=None):
    # _(message, plural_message=None, count=None, **kwargs):
    return str(_(msgid))


async def create_app():
    app = web.Application(middlewares=[babel_middleware])
    app.update(name='Testing aiohttp TAL')

    tal_loader = PageTemplateLoader(str(THIS_DIR / 'templates'),
                                    translate=translate,
                                    auto_reload=True  # debugging
                                    )
    aiohttp_tal.setup(app, loader=tal_loader)

    app.add_routes([web.static('/static', str(THIS_DIR / 'static'))])
    app['static_root_url'] = '/static'
    app.router.add_get('/', index, name='index')
    app.router.add_get('/translation', translation, name='translation')

    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=8080)
