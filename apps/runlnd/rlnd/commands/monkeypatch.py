# monkeypatch.py
from unittest.mock import patch
from inspect import getfullargspec, ArgSpec

import invoke


def fix_annotations():
    """
    Pyinvoke doesnt accept annotations by default, this fix that
    Based on: https://github.com/pyinvoke/invoke/pull/606
    """

    def patched_inspect_getargspec(func):
        spec = getfullargspec(func)
        return ArgSpec(*spec[0:4])

    org_task_argspec = invoke.tasks.Task.argspec

    def patched_task_argspec(*args, **kwargs):
        with patch(target="inspect.getargspec", new=patched_inspect_getargspec):
            return org_task_argspec(*args, **kwargs)

    invoke.tasks.Task.argspec = patched_task_argspec
