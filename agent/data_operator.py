# -*- coding: utf-8 -*-
import time
import logging
import urllib
import urllib2
from collections import defaultdict
from datetime import datetime

import config
import common

# key是monitor_type， value是该类型下的monitor data
all_data = defaultdict(list)


def recv_monitor_data(appname, monitor_name, monitor_type, value):
    monitor_id = '%s.%s.%s.%s' % (config.user_id, config.hostname, appname, monitor_name)
    logging.debug('recv_monitor_data:%s %s %s', monitor_id, monitor_type, value)
    data = {'monitor_id': monitor_id,
            'monitor_type': monitor_type,
            'value': value,
            }
    all_data[monitor_type].append(data)


def get_num_monitor_data(data):
    result = defaultdict(long)

    # 对num_sum类型的数据计算总和
    datas = data['num_sum']
    for data in datas:
        try:
            result[data['monitor_id']] += long(data['value'])
        except:
            logging.exception('get_num_monitor_data error:%s', data)

    # 对num_avg类型的数据计算平均数
    avg_total = defaultdict(long)
    avg_count = defaultdict(int)
    datas = data['num_avg']
    for data in datas:
        monitor_id = data['monitor_id']
        try:
            value = long(data['value'])
            avg_total[monitor_id] += value
            avg_count[monitor_id] += 1
        except:
            logging.exception('get_num_monitor_data error:%s', data)

    for monitor_id in avg_total.keys():
        result[monitor_id] = round(avg_total[monitor_id] / avg_count[monitor_id])

    return result
     

def get_text_monitor_data(data):
    result = defaultdict(str)
    datas = data['text']
    for data in datas:
        result[data['monitor_id']] += data['value']
    return datas


def send_data(url, to_send):
    logging.debug('begin send_data:%s %s', url, to_send)
    if not to_send:
        return
    try:
        req = urllib2.Request(url)
        data = urllib.urlencode(to_send)
        response = urllib2.urlopen(req, data)
        logging.debug('send_data success:%s %s', url, response.read())
    except:
        logging.exception('send_data error:%s %s', url, to_send)


class DataSender(common.StoppableThread):
    def __init__(self):
        common.StoppableThread.__init__(self, name="DataSender")
    
    def run(self):
        while not self.stop_event.is_set():
            try:
                if datetime.now().second == 0:
                    current_data = all_data.copy()
                    all_data.clear()

                    data = get_num_monitor_data(current_data)
                    send_data(config.num_collector_url, data)

                    data = get_text_monitor_data(current_data)
                    send_data(config.text_collector_url, data)
                time.sleep(1)
            except:
                logging.exception('DataSender run error')
