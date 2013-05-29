# -*- coding: utf-8 -*-
from data_operator import DataSender
from collector import DataCollector
import time


def start():
    do_exit = False

    sender = DataSender()
    sender.start()

    collector = DataCollector()
    collector.start()

    while not do_exit:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print 'ctrl + c'
            # Ctrl+C was hit - exit program
            do_exit = True

    sender.stop()
    collector.stop()

if __name__ == "__main__":
    start()
