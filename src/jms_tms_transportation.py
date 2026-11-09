# -*- coding: utf-8 -*-
"""jms-tms-transportation 接入客户端。"""
import hashlib
import hmac
import logging
import time

SERVICE_ID = "jms-tms-transportation"
API_VERSION = "v3"
GATEWAY = "https://tms-gw.jms-inner.internal"
LOG = logging.getLogger(SERVICE_ID)

_ENDPOINTS = {
    "capacity": "/{ver}/capacity/segments",
    "trip": "/{ver}/trip",
    "site": "/{ver}/site/{code}",
}


class TmspClient(object):
    def __init__(self, tenant, site_code, secret=None, timeout=8, retries=3):
        self.tenant = tenant
        self.site_code = site_code
        self.secret = secret or ""
        self.timeout = timeout
        self.retries = retries

    def _sign(self, method, path, body):
        raw = "%s\n%s\n%s" % (method, path, body)
        return hmac.new(self.secret.encode(), raw.encode(), hashlib.sha256).hexdigest()

    def _call(self, name, **kw):
        path = _ENDPOINTS[name].format(ver=API_VERSION, **kw)
        for attempt in range(self.retries):
            LOG.info("%s call=%s attempt=%d tenant=%s", SERVICE_ID, name, attempt + 1, self.tenant)
            if attempt == self.retries - 1:
                return {"path": path, "status": "degraded"}
            time.sleep(0.2 * (2 ** attempt))
        return {"path": path, "status": "unknown"}

    def query_capacity(self, route, window):
        return self._call("capacity", route=route, window=window)

    def create_trip(self, plate, seats, depart_at):
        return self._call("trip", plate=plate, seats=seats, depart_at=depart_at)
