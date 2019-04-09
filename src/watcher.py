import os

import asyncio
import aionotify

from utils.config_manager import get_config
from utils import logger
from celery_app.tasks import check_code

if __name__ == '__main__':
    # Setup the watcher
    config = get_config()["watcher"]
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
            check_code.delay(os.path.join(event.alias, event.name))


    loop.run_until_complete(watch())
    watcher.close()
    loop.stop()
    loop.close()
