#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from conf.config import API_KEY, API_SECRET
from core.xcontroller import XController
from core.xrobot import XRobot
from settings import config_logger

if __name__ == '__main__':
    config_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--symbol', type=str, help='symbol', default='CNDBTC')
    parser.add_argument('-q', '--quantity', type=float, help='quantity', default=450)
    parser.add_argument('-f', '--fee', type=float, help='fee', default=0.3)
    parser.add_argument('-p', '--profit', type=float, help='profit', default=0.5)
    parser.add_argument('-pa', '--price_adjust', type=int, help='price adjust', default=1)
    parser.add_argument('-tc', '--transaction_count', type=int, help='transaction count', default=2)
    parser.add_argument('-rc', '--robot_count', type=int, help='robot count', default=1)

    option = parser.parse_args()
    robot = XRobot(API_KEY, API_SECRET)
    xc = XController(robot, option)
    xc.fire()
