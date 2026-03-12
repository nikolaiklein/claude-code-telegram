"""Selective-concurrency update processor for PTB.

Regular updates (messages, commands) process sequentially -- one at a time.
Stop button callbacks (stop:*) bypass the queue and run immediately so they
can interrupt the currently-running handler via asyncio.Event.
"""

import asyncio
from typing import Any, Awaitable

from telegram import Update
from telegram.ext._baseupdateprocessor import BaseUpdateProcessor


class StopAwareUpdateProcessor(BaseUpdateProcessor):
    """Update processor that lets stop callbacks bypass sequential processing."""

    _MAX_CONCURRENT = 256

    def __init__(self) -> None:
        super().__init__(max_concurrent_updates=self._MAX_CONCURRENT)
        self._sequential_lock = asyncio.Lock()

    @staticmethod
    def _is_stop_callback(update: object) -> bool:
        if not isinstance(update, Update):
            return False
        cb = update.callback_query
        return cb is not None and cb.data is not None and cb.data.startswith('stop:')

    async def do_process_update(self, update: object, coroutine: Awaitable[Any]) -> None:
        if self._is_stop_callback(update):
            await coroutine
        else:
            async with self._sequential_lock:
                await coroutine

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass
