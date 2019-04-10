# quarantine
``quarantine`` is a tool for tracking file writes and executing callbacks.

Depends on [inotify](http://man7.org/linux/man-pages/man7/inotify.7.html).
Python3.7 required.

It tracks write to file in catalogue, set in ``config.yml`` and run callback, specified in ``quarantine/src/celery_app/tasks.py:check_code``.

By default, writes captured filename to log, specified ``config.yml``.

## Usage
### Dockerized usage (Recommended)
1. Install ``docker`` (https://docs.docker.com/install/).
2. ``git clone git@github.com:opavlyuk/quarantine.git && cd quarantine``
3. Make sure, to set all volumes in ``docker-compose.yml`` ([howto](https://docs.docker.com/compose/compose-file/#volumes)).
5. ``docker-compose build``
6. ``docker-compose up``

### Usage without docker
1. ``git clone git@github.com:opavlyuk/quarantine.git && cd quarantine``.
2. Install and run [redis](https://redis.io/topics/quickstart) or use docker ``docker run -d -p 6379:6379 redis``.
3. Configure ``config.yml``.
4. Make sure, that all catalogues, configured in ``config.yml`` exist in your system.
5. Create and activate virtual environment with python3.7, e.g. ``python -m venv venv && source venv/bin/activate``.
6. Install requirement ``pip install -r requirements.txt``
7. Run celery worker ``celery worker -A src.celery_app.application -l DEBUG --time-limit=3 --max-memory-per-child=30000 --logfile="/var/log/quarantine/%n%I.log" -D``
8. Run monitoring script ``python src/watcher.py``
9. To stop celery ``celery -A src.celery_app.application control shutdown``

## TODO
1. Improve README
2. Set uid and gid for celery worker
3. Investigate the best approach to save and report callback results
4. Improve celery workers configuration
