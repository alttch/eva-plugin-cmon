__author__ = 'Altertech, https://www.altertech.com/'
__copyright__ = 'Copyright (C) 2012-2021 Altertech'
__license__ = 'Apache License 2.0'
__version__ = "0.0.1"
"""
Plugin configuration:

    influx_path: http://host:port, required
    influx_db: database, required
    influx_username: user name (optional)
    influx_password: password (optional)
    influx_timeout: timeout (default: 5 sec)
    interval: collect interval (default: 5 sec)

    Only InfluxDB v1 (or v2 with backward compat. API enabled) is supported
"""

import eva.pluginapi as pa
import time

from types import SimpleNamespace

flags = SimpleNamespace(ready=False)

logger = pa.get_logger()

from datetime import datetime
import requests
import threading


def init(config, **kwargs):
    pa.check_product('sfa')
    flags.influx_path = config['influx_path']
    flags.influx_db = config['influx_db']
    flags.username = config.get('influx_username')
    flags.password = config.get('influx_password')
    flags.timeout = config.get('influx_timeout', 5)
    flags.interval = config.get('interval', 5)
    flags.ready = True


def start(**kwargs):
    if flags.ready:
        threading.Thread(target=worker, daemon=True).start()


def worker():
    if flags.username:
        auth = requests.auth.HTTPBasicAuth(flags.username, flags.password)
    else:
        auth = None
    sess = requests.Session()
    while True:
        time.sleep(flags.interval)
        try:
            data = pa.api_call('list_controllers')
            for c in data:
                i = c['oid']
                s = 1 if c['connected'] else 0
                q = f'{i} connected={s}'
                logger.info(f'{datetime.now()} {q}')
                r = sess.post(
                    url=f'{flags.influx_path}/write?db={flags.influx_db}',
                    data=q,
                    headers={'Content-Type': 'application/octet-stream'},
                    auth=auth,
                    timeout=flags.timeout)
                if not r.ok:
                    raise RuntimeError(f'Influxdb error {r.status_code}')
        except Exception as e:
            logger.error(e)
            pa.log_traceback()
