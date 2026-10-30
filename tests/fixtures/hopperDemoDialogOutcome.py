#!/usr/bin/env python3
"""Exercise the demo watcher's post-authentication timeout outcomes."""

import importlib.util
import json
import os
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location(
    "hopper_demo_x11", Path(__file__).resolve().parents[2] / "scripts/hopper-demo-x11.py"
)
assert spec is not None and spec.loader is not None
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def timeout_outcome(configured, requested=None):
    if configured is None:
        os.environ.pop(helper.DIALOG_TIMEOUT_ENV, None)
    else:
        os.environ[helper.DIALOG_TIMEOUT_ENV] = configured
    try:
        return {"ms": helper.configured_dialog_timeout_ms(requested)}
    except helper.AdapterFailure as failure:
        return {"code": failure.code, "reason": failure.reason}


def failure_outcome(owned, window_observed):
    failure = helper.classify_watch_timeout(owned, window_observed)
    return {"code": failure.code, "reason": failure.reason}


print(
    json.dumps(
        {
            "not_owned": failure_outcome(False, False),
            "admitted_without_window": failure_outcome(True, False),
            "admitted_with_window": failure_outcome(True, True),
            "default_timeout": timeout_outcome(None),
            "configured_timeout": timeout_outcome("25000"),
            "requested_timeout": timeout_outcome("25000", 500),
            "invalid_timeout": timeout_outcome("-5"),
        },
        separators=(",", ":"),
    )
)
