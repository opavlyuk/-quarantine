#!/usr/bin/env python
import os
import sys

import asyncio
import aionotify

sys.path.append(os.getcwd())  # Ugly workaround
from src.helpers.reporting import new_in_msg
from src.utils.config_manager import config
from src.utils.log import logger
from src.celery_app.tasks import checkers

if __name__ == '__main__':
    # Setup the watcher
    config = config["watcher"]
    watch_dir = config["watch_dir"]
    watcher = aionotify.Watcher()
    watcher.watch(path=watch_dir, flags=aionotify.Flags.CLOSE_WRITE)

    # Prepare the loop
    loop = asyncio.get_event_loop()


    async def watch():
        await watcher.setup(loop)
        while True:
            event = await watcher.get_event()
            logger.debug(f"Captured event {event}")
            with open(os.path.join(event.alias, event.name)) as f:
                user_code = f.read()
                incoming = new_in_msg("1:python-1", user_code)
                checker = checkers[incoming["task_id"]]
                checker.delay(incoming)


    loop.run_until_complete(watch())
    watcher.close()
    loop.stop()
    loop.close()
