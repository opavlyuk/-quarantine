# quarantine
``quarantine`` is a tool for tracking file writes and executing callbacks.

Depends on [inotify](http://man7.org/linux/man-pages/man7/inotify.7.html).

It tracks write to file in catalogue, set in ``config.yml`` and run callback, specified in ``quarantine/src/celery_app/tasks.py:check_code``.

By default, writes captured filename to log, specified ``config.yml``.

## Usage
### Dockerized usage (Reccomended)
1. Install ``docker`` (https://docs.docker.com/install/)
2. ``git clone git@github.com:opavlyuk/quarantine.git && cd quarantine``
3. Make sure, that ``watch_dir`` and ``results`` catalogues from ``config.yml`` exist in your system. 
2. ``docker-compose build``
3. ``docker-compose up``

## TODO
1. Improve README
2. Set uid and gid for celery worker
3. Investigate the best approach to save and report callback results
4. Improve celery workers configuration
