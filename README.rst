aiohttp_tal
===========
.. image:: https://travis-ci.com/allusa/aiohttp_tal.svg?branch=master
    :target: https://travis-ci.com/allusa/aiohttp_tal
.. image:: https://img.shields.io/pypi/v/aiohttp-tal.svg
    :target: https://pypi.python.org/pypi/aiohttp-tal
.. image:: https://readthedocs.org/projects/aiohttp-tal/badge/?version=latest
    :target: https://aiohttp-tal.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


TAL_ Chameleon_ template engine renderer for `aiohttp.web`__.
Based on aiohttp_jinja2_.

.. _TAL: https://chameleon.readthedocs.io/en/latest/reference.html
.. _Chameleon: https://chameleon.readthedocs.io
.. _aiohttp_web: https://aiohttp.readthedocs.io/en/latest/web.html
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2

__ aiohttp_web_


Installation
------------
Install from PyPI::

    pip install aiohttp-tal


Developing
----------

Install requirement and launch tests::

    pip install -r requirements-dev.txt
    pytest tests


Usage
-----

For more details on usage, see https://aiohttp-tal.readthedocs.io/en/latest/usage.html.


Before template rendering you have to setup *TAL environment* first:

.. code-block:: python

    app = web.Application()
    aiohttp_tal.setup(app,
        loader=chameleon.PageTemplateLoader('/path/to/templates/folder'))

Import:

.. code-block:: python

    import aiohttp_tal
    import chameleon

After that you may to use template engine in your *web-handlers*. The
most convenient way is to decorate a *web-handler*.

Using the function based web handlers:

.. code-block:: python

    @aiohttp_tal.template('tmpl.pt')
    def handler(request):
        return {'name': 'Andrew', 'surname': 'Svetlov'}



License
-------

``aiohttp_tal`` is offered under the GPLv3 license.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
