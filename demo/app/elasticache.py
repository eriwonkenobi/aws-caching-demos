from app.connections import _elasticache_connect
from datetime import datetime
from hurry.filesize import size

import json
import os


def _elasticache_flush():
    r = _elasticache_connect()
    start = datetime.now()
    r.flushdb()
    stop = datetime.now()
    diff = (stop-start).total_seconds()
    payload = json.dumps({"Response": "Elasticache successfully flushed",
                          "Duration": str(diff),
                          "Measurement": "Seconds"}, indent=2)
    return payload
