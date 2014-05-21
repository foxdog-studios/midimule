# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def get_listener():
    return LoggingMidiPortListener()


class MidiPortListener(object):
    def on_before_open(self):
        pass

    def on_after_open(self):
        pass

    def on_message(self, message, data=None):
        pass

    def on_before_close(self):
        pass

    def on_after_close(self):
        pass


class LoggingMidiPortListener(MidiPortListener):
    def on_message(self, message, data=None):
        print(message)

