# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from collections import OrderedDict
import imp
import logging
import math
import os
import sys
import time

import rtmidi

LOG_LEVELS = (
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
)

LOG_LEVEL_TO_NAMES = OrderedDict((level, logging.getLevelName(level).lower())
                                 for level in LOG_LEVELS)
LOG_NAME_TO_LEVEL = OrderedDict((name, level)
                                for level, name in LOG_LEVEL_TO_NAMES.items())


def main(argv=None):
    args = parse_argv(argv=argv)
    config_logger(args)

    midi_in = rtmidi.MidiIn()

    if args.port is None:
        port_id = ask_port_id(midi_in)
    else:
        port_id = args.port

    if args.listener is None:
        import midimule
        listener = midimule.LoggingMidiPortListener()
    else:
        listener_module = imp.load_source('listener_module', args.listener)
        listener = listener_module.get_listener()

    listen_to_port(midi_in, port_id, listener)

    return 0


def parse_argv(argv=None):
    if argv is None:
        argv = sys.argv
    parser = ArgumentParser()
    parser.add_argument('-l', '--log-level', choices=LOG_NAME_TO_LEVEL.keys(),
                        default=LOG_LEVEL_TO_NAMES[logging.INFO])
    parser.add_argument('-L', '--listener')
    parser.add_argument('-p', '--port', type=int)
    return parser.parse_args(args=argv[1:])


def config_logger(args):
    global logger
    logging.basicConfig(
            datefmt='%H:%M:%S',
            format='[%(levelname).1s %(asctime)s] %(message)s',
            level=LOG_NAME_TO_LEVEL[args.log_level])
    logger = logging.getLogger(__name__)


def ask_port_id(midi_in):
    port_names = midi_in.get_ports()

    if not port_names:
        raise Exception('No MIDI ports')

    port_id_header = 'ID'
    port_name_header = 'Name'

    port_id_width = int(math.ceil(math.log10(len(port_names))))
    port_id_width = max(len(port_id_header), port_id_width)

    port_name_width = int(math.ceil(max(len(name) for name in port_names)))
    port_name_width = max(len(port_id_header), port_name_width)

    def print_row(port_id, port_name):
        print('| {:>{}} | {:{}} |'.format(
                port_id,
                port_id_width,
                port_name,
                port_name_width))

    print_row(port_id_header, port_name_header)
    for port_id, port_name in enumerate(port_names):
        print_row(port_id, port_name)

    while True:
        port_id = None
        try:
            port_id = int(raw_input('Enter MIDI port ID: '))
        except ValueError:
            pass
        else:
            if not 0 <= port_id < len(port_names):
                port_id = None
        if port_id is not None:
            return port_id
        print("Sorry, that wasn't a valid MIDI port ID.")


def listen_to_port(midi_in, port_id, listener):
    try:
        midi_in.set_callback(listener.on_message)
        listener.on_before_open()
        midi_in.open_port(port_id)
        listener.on_after_open()
        while True:
            time.sleep(10)
        listener.on_before_close()
    finally:
        midi_in.close_port()
        listener.on_after_close()


if __name__ == '__main__':
    try:
        return_code = main()
    except (KeyboardInterrupt, SystemExit):
        return_code = 0
    exit(return_code)

