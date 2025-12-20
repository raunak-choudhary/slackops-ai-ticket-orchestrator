from __future__ import annotations

import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def record_latency(operation: str):
    start = time.time()
    try:
        yield
        duration = time.time() - start
        logger.info("op=%s status=success latency=%.3f", operation, duration)
    except Exception:
        duration = time.time() - start
        logger.info("op=%s status=failure latency=%.3f", operation, duration)
        raise