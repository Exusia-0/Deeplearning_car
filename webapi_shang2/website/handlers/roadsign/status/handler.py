#coding=utf8
from typing import Optional, Awaitable

__author__ = 'quchunyu@baidu.com'

import os
import sys

import time
import json
import traceback

import tornado.web
import tornado.gen

from framework.edgeboard import Edgeboard
from framework.request_handler import RequestHandler


class RoadsignStatusHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    @tornado.gen.coroutine
    def options(self):
        self.write_response({})

    @tornado.gen.coroutine
    def post(self):
        payload_success = {
            'errno': 0,
            'message': 'status was transmitted to 5 successfully.'
        }
        payload_transmit_failed = {
            'errno': 1004,
            'message': 'status transmit was failed. the status was not 1 or 4.'
        }
        payload_invalid_args = {
            'errno': 1005,
            'message': 'status transmit was failed. invalid arguments'
        }
        parameter = self.get_parameter()
        if 'camera' not in parameter or   \
           'downusb' not in parameter or  \
           'location' not in parameter:
            payload = payload_invalid_args
            self.write_response(payload)
            return

        if self.status == 1 or self.status == 4:
            finished = Edgeboard.start_roadsign(parameter['camera'],
                                                parameter['downusb'],
                                                parameter['location'])
            if finished:
                self.status = 5
                self.json = json.dumps({})
                payload = payload_success
            else:
                payload = payload_invalid_args
        else:
            payload = payload_transmit_failed

        self.write_response(payload)
