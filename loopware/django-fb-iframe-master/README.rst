Django Facebook iFrame
======================

Django and Facebook do not get along. When embedding a microsite into Facebook it will call an iframe with a ``POST`` request. Of course your Django project will return a CSRF verification failed.

This little Django app will prevent that specific error by converting a POST request with the key ``signed_request`` to a ``GET`` request. Of course this is just plain ugly, but Facebook should not mess with our application.


Installation
------------

Install django-fb-iframe with pip::

    $ pip install django-fb-iframe


Configuration
-------------

In your settings module...

* Add ``fb_iframe`` to ``INSTALLED_APPS``
* Add ``fb_iframe.middleware.FacebookMiddleware`` to ``MIDDLEWARE_CLASSES``

.. note::

    You need to make sure that you place the FacebookMiddleware before the CSRF protection middleware.


Credits
------------

This app contains a snippet of `fandjango's <https://github.com/jgorset/fandjango>`_ middleware.