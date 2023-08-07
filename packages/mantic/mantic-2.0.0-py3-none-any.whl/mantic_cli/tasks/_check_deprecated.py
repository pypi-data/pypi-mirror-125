# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""The ``check-deprecated`` task.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import sys

import invoke

from mantic import actions, infra

from ..config import config
from ._task import Task

_task: Task = Task.transmute({
    "iterable": ("ignore",),
    "optional": ("ignore",),
    "help": {
        "ignore": (
            "Paths to ignore",
            f"{', '.join(config.ignore)}",
            ),
        },
    })


@invoke.task(**_task.primitive())
def check_deprecated(_context, ignore):
    """Check if there are features to deprecate."""

    if len(ignore) == 0:
        ignore = config.ignore

    task = actions.CheckDeprecated(infra.logs, ignore = tuple(ignore))
    task()
    sys.exit(task.exit.value)
