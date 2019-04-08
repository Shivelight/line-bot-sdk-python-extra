🤖 line-bot-sdk-python-extra
============================

.. image:: https://img.shields.io/pypi/v/line-bot-sdk-extra.svg
   :target: https://pypi.python.org/pypi/line-bot-sdk-extra
   :alt: PyPI - Version

.. image:: https://img.shields.io/pypi/status/line-bot-sdk-extra.svg
   :target: https://pypi.python.org/pypi/line-bot-sdk-extra
   :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/pyversions/line-bot-sdk-extra.svg
   :target: https://pypi.python.org/pypi/line-bot-sdk-extra
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/l/line-bot-sdk-extra.svg
   :target: https://pypi.python.org/pypi/line-bot-sdk-extra
   :alt: PyPI - License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style - Black

.. image:: https://img.shields.io/badge/Ko--fi-donate-blue.svg
   :target: https://ko-fi.com/shivelight
   :alt: Ko-fi - Donate

Extra feature for `LINE Messaging API SDK for Python <line-bot-sdk-python_>`_.


Installation
------------

::

   pip install line-bot-sdk-extra

or::

   python setup.py install

To use the package::

>>> import linebotx


Features
--------

Asynchronous API
^^^^^^^^^^^^^^^^

Allows you to write non-blocking code which makes your bot respond much faster with little changes.

Synchronous:

.. code-block:: python

   from linebot import LineBotApi, WebhookHandler
   line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
   handler = WebhookHandler('YOUR_CHANNEL_SECRET')


Asynchronous:

.. code-block:: python

   from linebotx import LineBotApiAsync, WebhookHandlerAsync
   line_bot_api = LineBotApiAsync('YOUR_CHANNEL_ACCESS_TOKEN')
   handler = WebhookHandlerAsync('YOUR_CHANNEL_SECRET')


Equivalent Counterpart
""""""""""""""""""""""

+---------------------+----------------+
| linebotx            | linebot        |
+=====================+================+
| LineBotApiAsync     | LineBotApi     |
+---------------------+----------------+
| AioHttpClient       | HttpClient     |
+---------------------+----------------+
| AioHttpResponse     | HttpResponse   |
+---------------------+----------------+
| WebhookHandlerAsync | WebhookHandler |
+---------------------+----------------+

**NOTE:** Every public method is coroutine and should be awaited. For example:

.. code-block:: python

    @app.route("/callback", methods=['POST'])
    async def callback():
       ...
       await handler.handle(body, signature)
       ...


    @handler.add(MessageEvent, message=TextMessage)
    async def handle_message(event):
        await line_bot_api.reply_message(
           event.reply_token,
           TextSendMessage(text=event.message.text))


Additional Methods
""""""""""""""""""

coroutine :code:`LineBotApiAsync.close()`
   Close underlying http client.

coroutine :code:`AioHttpClient.close()`
   See `aiohttp.ClientSession.close() <https://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientSession.close>`_.


Timeout
"""""""

To set a timeout you can pass `aiohttp.ClientTimeout <https://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientTimeout>`_ object instead of numeric value.


Examples
""""""""

- `sanic-echo <https://github.com/Shivelight/line-bot-sdk-python-extra/tree/master/examples/sanic-echo>`_ - Sample echo-bot using sanic_.


Contributing
------------

If you would like to contribute, please check for open issues or open a new issue if you have ideas, changes, or bugs to report.


References
----------

This project is just a small addition to the original SDK, please refer to `line-bot-sdk-python <line-bot-sdk-python_>`_ or the `docs <https://line-bot-sdk-python.readthedocs.io/en/latest/>`_.

.. _sanic: https://github.com/huge-success/sanic
.. _line-bot-sdk-python: https://github.com/line/line-bot-sdk-python
