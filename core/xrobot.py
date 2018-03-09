#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from binance.client import Client

from .xconstants import *


class XRobot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_symbol_info(self, symbol):
        return self.client.get_symbol_info(symbol)

    def can_buy(self, data, strategy):
        return strategy.consult_buy_strategy(self.client, data)

    def buy(self, symbol, quantity, price):
        logging.info("[Buy]Order(symbol={}, quantity={:.8f}, price={}) will be submitted.".format(
            symbol, quantity, price))
        try:
            order = self.client.order_limit_buy(symbol=symbol, quantity=quantity, price=price,
                                                timeInForce=TIME_IN_FORCE_FOK)
            logging.info("[Buy]Order(orderId={}) is submitted.".format(order['orderId']))

            if order['status'] == ORDER_STATUS_FILLED:
                logging.info("[Buy]Order(orderId={}, status={}) is filled.".format(order['orderId'], order['status']))
                return order

            logging.info("[Buy]Order(orderId={}, status={}) is not filled.".format(order['orderId'], order['status']))
            return None
        except Exception as e:
            logging.error("[Buy Exception]={}".format(e))
            return None

    def can_sell(self, data, strategy):
        return strategy.consult_sell_strategy(self.client, data)

    def sell(self, symbol, quantity, price):
        logging.info("[Sell]Order(symbol={}, quantity={:.8f}, price={}) will be submitted.".format(
            symbol, quantity, price))
        try:
            order = self.client.order_limit_sell(symbol=symbol, quantity=quantity, price=price,
                                                 timeInForce=TIME_IN_FORCE_FOK)
            logging.info("[Sell]Order(orderId={}) is submitted.".format(order['orderId']))

            if order['status'] == ORDER_STATUS_FILLED:
                logging.info("[Sell]Order(orderId={}, status={}) is filled.".format(order['orderId'], order['status']))
                return order

            logging.info("[Sell]Order(orderId={}, status={}) is not filled.".format(order['orderId'], order['status']))
            return None
        except Exception as e:
            logging.error("[Sell Exception]={}".format(e))
            return None
