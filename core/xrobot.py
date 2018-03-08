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

    def can_buy(self, data):
        try:
            ticker = self.client.get_ticker(symbol=data.symbol)
            data.last_ask = float(ticker['askPrice'])
            data.last_bid = float(ticker['bidPrice'])
            data.last_price = float(ticker['lastPrice'])

            notional = data.quantity * data.last_price
            if notional < data.min_notional:
                logging.error("[PreBuy]Invalid notional: current notional({:.8f}) < min notional({:.8f})".format(
                    notional, data.min_notional))

                return False

            # calculate buy price
            data.buy_price = "{:.8f}".format(data.last_bid + data.tick_size * data.price_adjust)

            # calculate breakeven sell price
            data.breakeven_sell_price = float(data.buy_price) * (1 + data.fee / 100)

            # calculate profitable sell price
            data.profitable_sell_price = float(data.buy_price) * (1 + (data.fee + data.profit) / 100)

            # calculate spread percentage
            spread_percentage = (data.last_ask / data.last_bid - 1) * 100.0

            logging.info("[PreBuy]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, cbp:{}, cpp:{:.8f}, per:{:.2f}".format(
                data.last_price, data.last_ask, data.last_bid, data.buy_price, data.profitable_sell_price,
                spread_percentage))

            return data.last_ask >= data.breakeven_sell_price
        except Exception as e:
            logging.error("[Can Buy Exception]={}".format(e))
            return False

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

    def can_sell(self, data):
        try:
            ticker = self.client.get_ticker(symbol=data.symbol)
            data.last_ask = float(ticker['askPrice'])
            data.last_bid = float(ticker['bidPrice'])
            data.last_price = float(ticker['lastPrice'])

            # calculate sell price
            data.sell_price = "{:.8f}".format(data.last_price - data.tick_size)

            # calculate spread percentage
            spread_percentage = (data.last_ask / data.last_bid - 1) * 100.0

            logging.info("[PreSell]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, csp:{}, cpp:{:.8f}, per:{:.2f}".format(
                data.last_price, data.last_ask, data.last_bid, data.sell_price, data.profitable_sell_price,
                spread_percentage))

            return data.last_price >= data.profitable_sell_price
        except Exception as e:
            logging.error("[Can Sell Exception]={}".format(e))
            return False

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
