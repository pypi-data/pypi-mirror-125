# Copyright © 2021 Center of Research & Development <info@crnd.pro>

#######################################################################
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################

""" Retry via iteration

This module provide helper functions, to easily implement retry logic
via iteration over attempts.

Check documentation of functions: retry_iter and a_retry_iter
"""


import time
import random
import asyncio


class RetryTimeout:
    """ Simple class that could be used to work with retry timeouts
    """
    def __init__(self, timeout, timeout_type='fixed',
                 timeout_max=None, max_retries=3):
        self.timeout_type = timeout_type
        self.timeout_min = timeout
        self.timeout_max = timeout_max
        self.max_retries = max_retries

        self._validate()

        self._increase_step = None

    def _validate(self):
        if self.timeout_type not in ('fixed', 'increase', 'random'):
            raise ValueError("Incorrect value for timeout type")

    @property
    def increase_step(self):
        if self._increase_step is None:
            self._increase_step = (
                (self.timeout_max - self.timeout_min) / self.max_retries)
        return self._increase_step

    @classmethod
    def parse(cls, timeout, max_retries=3):
        if isinstance(timeout, cls):
            return timeout
        if isinstance(timeout, (int, float)):
            return cls(timeout, max_retries=max_retries)
        if isinstance(timeout, (list, tuple)) and len(timeout) == 3:
            timeout_type, retry_timeout, retry_timeout_max = timeout
            return cls(
                retry_timeout,
                timeout_type=timeout_type,
                timeout_max=retry_timeout_max,
                max_retries=max_retries)
        raise TypeError("Incorrect type of value for timeout")

    def loop(self):
        attempt = 0
        timeout = self.timeout_min
        while attempt < self.max_retries:
            attempt += 1

            # Do work
            yield attempt, timeout

            if self.timeout_type == 'increase':
                timeout += self.increase_step
            elif self.timeout_type == 'random':
                timeout += random.uniform(
                    self.timeout_min, self.timeout_max)


def _retry_iter_internal(timeout, max_retries):
    """ Internal impelemntation of retry_iter
    """
    timeout = RetryTimeout.parse(timeout, max_retries=max_retries)
    for attempt, retry_timeout in timeout.loop():
        # Do work
        yield attempt, retry_timeout


def retry_iter(interval_timeout=0.5, max_retries=3, first_timeout=True):
    """ Retry as iterator - simple function that could be used as iterator to
        provide *retry* mechanism.

        :param float interval_timeout: timeout to sleep between retries
        :param int max_retries: Number of retries before end of loop
        :param bool first_timeout: Do we need timeout before first iteration

        Example of usage::

            state = False
            for attempt in retry_iter(max_retries=5):
                if do_operation(params):
                    state = True
                    break
            if not state:
                raise Exception("Operation failed")
    """
    timeout = RetryTimeout.parse(interval_timeout, max_retries=max_retries)

    enable_timeout = first_timeout

    for attempt, retry_timeout in timeout.loop():
        if enable_timeout:
            time.sleep(retry_timeout)

        yield attempt

        enable_timeout = True


async def a_retry_iter(interval_timeout=0.5,
                       max_retries=3,
                       first_timeout=True):
    """ Async version of ``retry_iter`` function.

        :param float interval_timeout: timout to sleep between retries
        :param int max_retries: Number of retries before end of loop
        :param bool first_timeout: Do we need timeout before first iteration

        Example of usage::
            state = False
            async for attempt in a_retry_iter(max_retries=5):
                if await do_operation(params):
                    state = True
                    break
            if not state:
                raise Exception("Operation failed")
    """
    timeout = RetryTimeout.parse(interval_timeout, max_retries=max_retries)
    enable_timeout = first_timeout

    for attempt, retry_timeout in timeout.loop():

        if enable_timeout:
            await asyncio.sleep(retry_timeout)

        # Do work
        yield attempt

        enable_timeout = True
