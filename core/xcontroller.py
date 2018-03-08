#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import math
import threading
import time


class XController:
    INIT_WAIT_TIME = 30
    BUY_WAIT_TIME = 0.5
    SELL_WAIT_TIME = 1

    INIT_TIMES = 1024
    BUY_TIMES = 3
    SELL_TIMES = 3

    def __init__(self, robot, option):
        self.robot = robot
        self.option = option
        self._data = threading.local()

    def fire(self):
        for i in range(self.option.robot_count):
            trader = threading.Thread(target=self.run, name="XRobot{}({})".format(i, self.option.symbol))
            trader.start()

    def run(self):
        for i in range(self.option.transaction_count):
            logging.info("[Start]Transaction{} is started.".format(i))
            if self._init() is False:
                logging.error('[Init]Init failed, XTrader will exit.')
                return

            buy_order = None
            while buy_order is None:
                buy_order = self._buy()
                time.sleep(XController.BUY_WAIT_TIME)

            sell_order = None
            while sell_order is None:
                sell_order = self._sell()
                time.sleep(XController.SELL_WAIT_TIME)

            logging.info("[End]Transaction{} is ended.".format(i))

    def _init(self):
        for i in range(XController.INIT_TIMES):
            try:
                symbol_info = self.robot.get_symbol_info(self.option.symbol)
                if symbol_info is None:
                    logging.info("[Init]Symbol is not supported: {}".format(self.option.symbol))
                    return False

                self._data.symbol = symbol_info['symbol']

                symbol_info['filters'] = {item['filterType']: item for item in symbol_info['filters']}
                self._data.min_qty = float(symbol_info['filters']['LOT_SIZE']['minQty'])
                self._data.min_price = float(symbol_info['filters']['PRICE_FILTER']['minPrice'])
                self._data.min_notional = float(symbol_info['filters']['MIN_NOTIONAL']['minNotional'])
                self._data.step_size = float(symbol_info['filters']['LOT_SIZE']['stepSize'])
                self._data.tick_size = float(symbol_info['filters']['PRICE_FILTER']['tickSize'])

                quantity = self.option.quantity
                quantity = self._data.min_qty if quantity < self._data.min_qty else quantity
                quantity = float(self._data.step_size * math.floor(quantity / self._data.step_size))
                self._data.quantity = quantity

                self._data.fee = self.option.fee
                self._data.profit = self.option.profit
                self._data.price_adjust = self.option.price_adjust

                return True
            except Exception as e:
                logging.error("[Init Exception {}]={}".format(i, e))
                time.sleep(XController.INIT_WAIT_TIME)
        return False

    def _buy(self):
        order = None
        if self.robot.can_buy(self._data):
            buy_count = 0
            while buy_count < XController.BUY_TIMES:
                order = self.robot.buy(self._data.symbol, self._data.quantity, self._data.buy_price)

                if order is not None:
                    break

                buy_count += 1
        return order

    def _sell(self):
        order = None
        if self.robot.can_sell(self._data):
            sell_count = 0

            while sell_count < XController.SELL_TIMES:
                order = self.robot.sell(self._data.symbol, self._data.quantity, self._data.sell_price)

                if order is not None:
                    break

                sell_count += 1
        return order
