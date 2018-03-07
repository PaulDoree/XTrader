#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import threading
import time


class XController:
    BUY_WAIT_TIME = 0.5
    SELL_WAIT_TIME = 1

    BUY_TIMES = 3
    SELL_TIMES = 3

    def __init__(self, robot, option):
        self.robot = robot
        self.option = option
        self._params = threading.local()

    def fire(self):
        # params validate
        is_valid = self._validate()
        if is_valid is False:
            logging.error('[Validate]Validate args failed, XTrader will exit.')
            return

        for i in range(self.option.robot_count):
            trader = threading.Thread(target=self.run, name="XRobot{}({})".format(i, self.option.symbol))
            trader.start()

    def run(self):
        transaction_count = sys.maxsize if self.option.transaction_count <= 0 else self.option.transaction_count
        for i in range(transaction_count):
            logging.info("[Start]Transaction{} is started.".format(i))

            buy_order = None
            while buy_order is None:
                buy_order = self._buy()
                time.sleep(XController.BUY_WAIT_TIME)

            sell_order = None
            while sell_order is None:
                sell_order = self._sell()
                time.sleep(XController.SELL_WAIT_TIME)

            logging.info("[End]Transaction{} is ended.".format(i))

    def _validate(self):
        # check fee
        fee = self.option.fee
        if fee < 0.2:
            logging.error("[Check]Invalid fee: {}.".format(self.option.fee))
            return False

        # check profit
        profit = self.option.profit
        if profit < 0:
            logging.error("[Check]Invalid profit: {}.".format(self.option.profit))
            return False

        # check price factor
        price_adjust = self.option.price_adjust
        if price_adjust < 0:
            logging.error("[Check]Invalid price_adjust: {}.".format(self.option.price_adjust))
            return False

        # check robot count
        robot_count = self.option.robot_count
        if robot_count < 1:
            logging.error("[Check]Invalid robot_count: {}.".format(self.option.robot_count))
            return False

        # check transaction count
        transaction_count = self.option.transaction_count
        if transaction_count < 0:
            logging.error("[Check]Invalid transaction_count is: {}.".format(self.option.transaction_count))
        elif transaction_count == 0:
            logging.warning("[Check]Current transaction_count is: {}, and will be overwrite to {}.".format(
                self.option.transaction_count, sys.maxsize))

        return self.robot.validate_args(self.option)

    def _buy(self):
        order = None
        if self.robot.can_buy(self.option, self._params):
            buy_count = 0
            while buy_count < XController.BUY_TIMES:
                order = self.robot.buy(self._params.symbol, self._params.quantity, self._params.buy_price)

                if order is not None:
                    break

                buy_count += 1
        return order

    def _sell(self):
        order = None
        if self.robot.can_sell(self._params):
            sell_count = 0

            while sell_count < XController.SELL_TIMES:
                order = self.robot.sell(self._params.symbol, self._params.quantity, self._params.sell_price)

                if order is not None:
                    break

                sell_count += 1
        return order
