============
Installation
============

The Zaaktypecatalogus (ZTC) is developed in Python using the
`Django framework <https://www.djangoproject.com/>`_ and the
`Django Rest Framework <http://www.django-rest-framework.org/>`_.

For platform specific installation instructions, see the "deployment" folder.

Getting started
===============

Quick start using Docker
------------------------

The easiest way to get started is by using
`Docker Compose <https://docs.docker.com/compose/install/>`_.

1. Clone or download the code from
   `Github <https://github.com/Haarlem/zaaktypecataloguscomponent>`_ in a
   folder like ``ztc``:

   .. code-block:: bash

       $ git clone git@github.com:Haarlem/zaaktypecataloguscomponent.git ztc
       Cloning into 'ztc'...
       ...

       $ cd ztc

2. Start the database and Zaaktypecatalogus services:

   .. code-block:: bash

       $ docker-compose up -d
       Starting ztc_db_1 ... done
       Starting ztc_web_1 ... done

3. Create an admin user for our Zaaktypecatalogus and load initial data. If
   different container names are shown above, use the container name ending
   with ``_web_1``:

   .. code-block:: bash

       $ docker exec -it ztc_web_1 /app/src/manage.py createsuperuser
       Username: admin
       ...
       Superuser created successfully.

       $ docker exec -it ztc_web_1 /app/src/manage.py loaddata admin_index groups
       Installed 5 object(s) from 2 fixture(s)

4. Point your browser to ``http://localhost:8000/`` to access the
   Zaaktypecatalogus with the credentials used in step 3.

   If you are using ``Docker Machine``, you need to point your browser to the
   Docker VM IP address. You can get the IP address by doing
   ``docker-machine ls`` and point your browser to
   ``http://<ip>:8000/`` instead (where the IP is shown below the URL column):

   .. code-block:: bash

       $ docker-machine ls
       NAME      ACTIVE   DRIVER       STATE     URL
       default   *        virtualbox   Running   tcp://<ip>:<port>

5. To shutdown the services, use ``docker-compose down``.

More Docker
-----------

If you just want to run the Zaaktypecatalogus as a Docker container and
connect to an external database, you can build and run the ``Dockerfile`` and
pass several environment variables. See ``src/ztc/conf/docker.py`` for all
settings.

.. code-block:: bash

    $ docker build . && docker run \
        -p 8000:8000 \
        -e DJANGO_SETTINGS_MODULE=ztc.conf.docker \
        -e DATABASE_USERNAME=... \
        -e DATABASE_PASSWORD=... \
        -e DATABASE_HOST=... \
        --name ztc

    $ docker exec -it ztc /app/src/manage.py createsuperuser


Developers
==========

Prerequisites
-------------

You need the following libraries and/or programs:

* Python 3.4 or above
* Python Virtualenv and Pip
* PostgreSQL 9.1 or above

Setting up your local development environment
---------------------------------------------

For developers who are familiar with Django, this project should be straight
forward to set up.

#. Grab the code.

#. Create a PostgreSQL database and database user. By default, the database,
   database user, and password are all ``ztc``.

#. Create and activate your virtual environment:

   .. code-block:: bash

       $ virtualenv env
       $ source env/bin/activate

#. Install all required Python libraries:

   .. code-block:: bash

       $ pip install -r requirements/dev.txt

#. Copy ``src/ztc/conf/local_example.py`` to ``src/ztc/conf/local.py`` and
   modify it to your likings.

#. Link the static files, create the database tables and load initial data:

   .. code-block:: bash

       $ python src/manage.py collectstatic --link
       $ python src/manage.py migrate
       $ python src/manage.py loaddata admin_index groups

#. Create a super user:

   .. code-block:: bash

       $ python src/manage.py createsuperuser

#. Start the webserver:

   .. code-block:: bash

   $ python src/manage.py runserver

#. Done!

You can find the API documentation at:

* http://localhost:8000/api/v1/schema/

You can find the admin interface at:

* http://localhost:8000/admin/

API Access token
----------------

The API requires a valid access token. You can generate one in the admin
at http://localhost:8000/admin/oauth2_provider/accesstoken/, with scope
``read write``.

Next, configure your API Client (Postman) or similar to use the auth: add the
header ``Authorization: Bearer <token>``.

Testsuite
---------

To run the test suite:

.. code-block:: bash

    $ pip install -r requirements/dev.txt
    $ python src/manage.py test ztc

Settings
========

All settings for the Zaaktypecatalogus can be found in ``src/ztc/conf``.
The file ``local.py`` overwrites settings from the base configuration.

There are no specific settings for the Zaaktypecatalogus. See
`Django Rest Framework settings <http://www.django-rest-framework.org/api-guide/settings/>`_
for all API related settings.

Commands
========

Commands can be executed using:

.. code-block:: bash

    $ python src/manage.py <command>

There are no specific commands for the Zaaktypecatalogus. See
`Django framework <https://docs.djangoproject.com/en/dev/ref/django-admin/#available-commands>`_
for all default commands, or type ``python src/manage.py --help``.
