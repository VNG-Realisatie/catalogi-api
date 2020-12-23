Docker
======

The easiest way to get the project started is by using `Docker Compose`_.

Prerequisites
-------------

* `Docker`_
* `Docker Compose`_


Docker basics
-------------


1. Clone or download the code from `Github`_ in a folder like
   ``ztc``:

   .. code-block:: bash

       $ git clone https://github.com/VNG-realisatie/catalogi-api.git ztc
       Cloning into 'ztc'...
       ...

       $ cd ztc

2. Start the database and web services:

   .. code-block:: bash

       $ docker-compose up web -d
       Starting ztc_db_1 ... done
       Starting ztc_web_1 ... done

   This starts the web service and any services that it depends on.

   It can take a while before everything is done. Even after starting the web
   container, the database might still be migrating. You can always check the
   status with:

   .. code-block:: bash

       $ docker logs -f ztc_web_1


3. Create an admin user and load initial data. If different container names
   are shown above, use the container name ending with ``_web_1``:

   .. code-block:: bash

       $ docker exec -it ztc_web_1 /app/src/manage.py createsuperuser
       Username: admin
       ...
       Superuser created successfully.

4. Point your browser to ``http://localhost:8000/`` to access the project's
   management interface with the credentials used in step 3.

   If you are using ``Docker Machine``, you need to point your browser to the
   Docker VM IP address. You can get the IP address by doing
   ``docker-machine ls`` and point your browser to
   ``http://<ip>:8000/`` instead (where the ``<ip>`` is shown below the URL
   column):

   .. code-block:: bash

       $ docker-machine ls
       NAME      ACTIVE   DRIVER       STATE     URL
       default   *        virtualbox   Running   tcp://<ip>:<port>

5. To shutdown the services, use ``docker-compose down`` and to clean up your
   system you can run ``docker system prune``.


More Docker
-----------

If you just want to run the project as a Docker container and connect to an
external database, you can build and run the ``Dockerfile`` and pass several
environment variables. See ``src/ztc/conf/docker.py`` for
all settings.

.. code-block:: bash

    $ docker build . && docker run \
        -p 8000:8000 \
        -e DJANGO_SETTINGS_MODULE=ztc.conf.docker \
        -e DB_USERNAME=... \
        -e DB_PASSWORD=... \
        -e DB_HOST=... \
        --name ztc

    $ docker exec -it ztc /app/src/manage.py createsuperuser

Loading initial data
--------------------

The container will load any fixtures it can find at startup time. The default
location is ``/app/fixtures``, so you can mount a volume containing JSON
fixtures to populate your database initially.

You can override this location through the ``FIXTURES_DIR`` environment
variable. Only ``*.json`` files are considered.


.. _Github: https://github.com/VNG-realisatie/catalogi-api
.. _Docker: https://docs.docker.com/install/
.. _Docker Compose: https://docs.docker.com/compose/install/
