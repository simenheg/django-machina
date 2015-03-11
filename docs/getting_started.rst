Getting started
===============

Requirements
------------

* `Python`_ 2.7, 3.3 or 3.4
* `Django`_ 1.4.x, 1.5.x, 1.6.x or 1.7.x
* `Pillow`_ 2.2. or higher
* `Django-model-utils`_ 2.0. or higher
* `Django-mptt`_ 0.6.1. or higher
* `Django-guardian`_ 1.2. or higher
* `Django-haystack`_ 2.1. or higher
* `Django-markdown`_ 0.7. or higher
* `Django-compressor`_ 1.4. or higher
* `Django-bootstrap3`_ 3.0. or higher
* `South`_ 1.0.1 or higher if you are using Django < 1.7


.. warning:: While *django-machina* is compatible with Django 1.5.x, this version of Django
             is no longer supported by the Django team. Please upgrade to
             Django 1.6.x or 1.7.x immediately.

.. note::

	*Django-machina* uses Markdown (*django-markdown*) by default as a syntax for forum messages, but you can change this
	in your settings.

	*Django-machina*'s default templates use *django-compressor* to handle static files and *django-bootstrap3* to render
	forms. These packages are optional and you can override this by using your own templates.

.. _Python: https://www.python.org
.. _Django: https://www.djangoproject.com
.. _Pillow: http://python-pillow.github.io/
.. _Django-model-utils: https://github.com/carljm/django-model-utils
.. _Django-mptt: https://github.com/django-mptt/django-mptt
.. _Django-guardian: https://github.com/lukaszb/django-guardian
.. _Django-haystack: https://github.com/django-haystack/django-haystack
.. _Django-markdown: https://github.com/klen/django_markdown
.. _Django-compressor: https://github.com/django-compressor/django-compressor
.. _Django-bootstrap3: https://github.com/dyve/django-bootstrap3
.. _South: http://south.aeracode.org/

Installation
------------

Install *django-machina* using::

  pip install git+git://github.com/ellmetha/django-machina.git

.. note::

	Please remember that *django-machina* is still in heavy development. It is not yet suitable for production environments.

Project configuration
---------------------

Django settings
~~~~~~~~~~~~~~~

First update your ``INSTALLED_APPS`` in your project's settings module. Modify it to be a list and append the *django-machina*'s  apps to this list::

  from machina import get_vanilla_apps

  INSTALLED_APS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    
    # Machina related apps:
    'mptt',
    'guardian',
    'haystack',

    'bootstrap3',
    'compressor',
    'django_markdown',
  ] + get_vanilla_apps()

.. note::

  As previously stated, *django-markdown* is the default syntax used for forum messages and *django-compressor* and *django-bootstrap3* are used in templates to handle static files and form rendering. These modules are optional really and you may decide to override the *django-machina*'s templates to use other modules. 

*Django-machina* uses *django-mptt* to handle the tree of forum instances and *django-guardian* is used to allow per-forum permissions management. Search capabilities are provided by *django-haystack*.

Then update your ``TEMPLATE_CONTEXT_PROCESSORS`` setting as follows::

  TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    # Machina
    'machina.core.context_processors.metadata',
  )

Then edit your ``TEMPLATE_DIRS`` setting so that it includes the *django-machina*'s template directory::

  from machina import MACHINA_MAIN_TEMPLATE_DIR

  TEMPLATE_DIRS = (
    # ...
    MACHINA_MAIN_TEMPLATE_DIR,
  )

Finally you have to add a new cache to your settings. This cache will be used to store temporary post attachments. Note that this ``machina_attachments`` cache must use the ``django.core.cache.backends.filebased.FileBasedCache`` backend, as follows::

  CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
      'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
      'LOCATION': '/tmp',
    }
  }

Django-guardian settings
~~~~~~~~~~~~~~~~~~~~~~~~

*Django-machina* uses the *django-guardian* module to allow you define your forum permissions in a permissive way. As *django-guardian* provides object permissions capabilities, you can define specific user or group permissions for each forum you create.

*Django-machina* supports anonymous posting and handle anonymous users. So you need to create an ``ANONYMOUS_USER_ID`` setting in order to allow *django-machina* to properly handle anonymous user permissions inside your forum::

  ANONYMOUS_USER_ID = -1

Django-haystack settings
~~~~~~~~~~~~~~~~~~~~~~~~

*Django-machina* uses *django-haystack* to provide search for forum conversations. *Django-haystack* allows you to plug in many search backends so you may want to choose the one that best suits your need.

You can start using the basic search provided by the *django-haystack*'s simple backend::

  HAYSTACK_CONNECTIONS = {
    'default': {
      'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
  }

You can also decide to use a more powerfull backend such as *Solr* or *Whoosh*::

  HAYSTACK_CONNECTIONS = {
    'default': {
      'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
      'PATH': os.path.join(PROJECT_PATH, 'whoosh_index'),
    },
  }

Database and migrations
-----------------------

*Django-machina* provides *South* migrations and new-style migrations. If you are using Django 1.6 or below, you should use *South* 1.0 or higher in order to benefit from the migrations. This way you can use the migration command provided by *South*::

  python manage.py migrate

If you are using Django 1.7 or higher, just use the ``syncdb`` or ``migrate`` commands::

  python manage.py syncdb

URLs configuration
------------------

Finally you have to update your main ``urls.py`` module in order to include forum's URLs::

  from machina.app import board

  urlpatterns = patterns(
    # [...]

    # Apps
    url(r'^forum/', include(board.urls)),
  )

*Congrats! You're in.*