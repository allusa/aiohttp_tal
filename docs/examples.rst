Examples
========

Download full examples code from `GitHub <https://github.com/allusa/aiohttp_tal/tree/master/examples>`_.



Simple
------

A simple TAL example with METAL macros.

Install::

  pip install aiohttp-tal

Run::

  python simple.py


.. literalinclude:: ../examples/simple.py
   :language: python
   :caption: simple.py

Macro
*****

.. literalinclude:: ../examples/templates/base.html
   :language: html
   :caption: templates/base.html

Page template
*************

.. literalinclude:: ../examples/templates/index.html
   :language: html
   :caption: templates/index.html



Translation (I18N)
------------------


See `TAL I18N <https://chameleon.readthedocs.io/en/latest/reference.html#translation-i18n>`_ and `aiohttp_babel <https://github.com/jie/aiohttp_babel>`_.


Install::

  pip install aiohttp-tal aiohttp_babel babel-lingua-chameleon

Run::

  python translation.py

.. literalinclude:: ../examples/translation.py
   :language: python
   :caption: translation.py


Page template with i18n
***********************

.. literalinclude:: ../examples/templates/translation.html
   :language: html
   :caption: templates/translation.html
