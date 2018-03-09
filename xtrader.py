#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from conf.config import API_KEY, API_SECRET
from core.xcontroller import XController
from core.xrobot import XRobot
from settings import config_logger
from utils.arg_checker import *

if __name__ == '__main__':
    config_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--symbol', type=str, default='CNDBTC',
                        help='symbol')
    parser.add_argument('-q', '--quantity', type=quantity_float, default=450,
                        help='quantity must be greater than 0')
    parser.add_argument('-f', '--fee', type=fee_float, default=0.4,
                        help='fee must be greater than or equal to 0')
    parser.add_argument('-p', '--profit', type=profit_float, default=0.6,
                        help='profit must be greater than or equal to 0.3')
    parser.add_argument('-pa', '--price_adjust', type=price_adjust_int, default=1,
                        help='price_adjust must be greater than or equal to 1')
    parser.add_argument('-tc', '--transaction_count', type=count_int, default=1,
                        help='transaction count must be greater than or equal to 1')
    parser.add_argument('-rc', '--robot_count', type=count_int, default=1,
                        help='robot count must be greater than or equal to 1')
    parser.add_argument('--strategy', type=strategy, default='default_strategy.DefaultStrategy',
                        help='transaction strategy, and format is module_name.strategy_class_name')

    option = parser.parse_args()
    robot = XRobot(API_KEY, API_SECRET)
    xc = XController(robot, option)
    xc.fire()
