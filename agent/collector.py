# -*- coding: utf-8 -*-
import threading
from urlparse import parse_qs
from cgi import parse_header
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import config
import logging
import data_operator


class RequestHandler(ThreadingMixIn, BaseHTTPRequestHandler):
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        length = int(self.headers['content-length'])
        postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        return postvars

    def do_POST(self):
        postvars = self.parse_POST()
        logging.debug('do post:%s', postvars)

        monitor_id = postvars.get('monitor_id')
        monitor_type = postvars.get('monitor_type')
        monitor_value = postvars.get('value')

        if monitor_id is None or monitor_type is None or monitor_value is None:
            self.send_error(400, 'arg error')
            return

        data_operator.recv_monitor_data(monitor_id[0], monitor_type[0], monitor_value[0])
        self.send_response(200)


class DataCollector(object):
    def start(self):
        self.server = HTTPServer((config.agent_host, config.agent_port), RequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        logging.warn('DataCollector start:%s %s', config.agent_host, config.agent_port)

    def stop(self):
        logging.warn('DataCollector will stop:%s %s', config.agent_host, config.agent_port)
        self.server.shutdown()
        self.thread.join()
