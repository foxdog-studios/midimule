from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import ddp


def jarkle(device, conn, method):
    msg_id = 0

    while True:
        e = device.try_read()
        if not e:
            time.sleep(0.1)
            continue
        func, note, vel = e[0][:3]
        # Ignore Yamaha DTXPLORER click and 0 velocity second notes
        # and high hat pedal
        if func != 248 \
           and func != 185 \
           and note != 44 \
           and vel != 0:
            conn.send(ddp.MethodMessage(str(msg_id), method, [{
                "func": func,
                "note": note,
                "vel": vel,
            }]))
            msg_id += 1

