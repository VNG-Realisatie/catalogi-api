Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess ztc-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/ztc/log/apache2/error.log"
        CustomLog "/srv/sites/ztc/log/apache2/access.log" common

        WSGIProcessGroup ztc-<target>

        Alias /media "/srv/sites/ztc/media/"
        Alias /static "/srv/sites/ztc/static/"

        WSGIScriptAlias / "/srv/sites/ztc/src/ztc/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-ztc-<target>]
    user = <user>
    command = /srv/sites/ztc/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/ztc/src/ztc/wsgi/wsgi_<target>.py
    home = /srv/sites/ztc/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/ztc/log/uwsgi_err.log
    stdout_logfile = /srv/sites/ztc/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_ztc_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/ztc/log/nginx-access.log;
      error_log /srv/sites/ztc/log/nginx-error.log;

      location /500.html {
        root /srv/sites/ztc/src/ztc/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/ztc/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/ztc/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_ztc_<target>;
      }
    }
