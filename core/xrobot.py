#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import math

from binance.client import Client

from .xconstants import *


class XRobot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def validate_args(self, option):
        # validate symbol
        try:
            symbol_info = self.client.get_symbol_info(option.symbol)
            if symbol_info is None:
                logging.error("[Validate]Invalid symbol: {}".format(option.symbol))
                return False
        except Exception as e:
            logging.error("[Validate Exception]={}".format(e))
            return False

    def can_buy(self, option, params):
        try:
            params.fee = option.fee
            params.profit = option.profit
            params.price_adjust = option.price_adjust

            symbol_info = self.client.get_symbol_info(option.symbol)
            params.symbol = symbol_info['symbol']

            symbol_info['filters'] = {item['filterType']: item for item in symbol_info['filters']}
            params.min_qty = float(symbol_info['filters']['LOT_SIZE']['minQty'])
            params.min_price = float(symbol_info['filters']['PRICE_FILTER']['minPrice'])
            params.min_notional = float(symbol_info['filters']['MIN_NOTIONAL']['minNotional'])
            params.step_size = float(symbol_info['filters']['LOT_SIZE']['stepSize'])
            params.tick_size = float(symbol_info['filters']['PRICE_FILTER']['tickSize'])

            quantity = option.quantity
            quantity = params.min_qty if quantity < params.min_qty else quantity
            quantity = float(params.step_size * math.floor(quantity / params.step_size))
            params.quantity = quantity

            order_book_ticker = self.client.get_orderbook_ticker(symbol=params.symbol)
            last_ask = float(order_book_ticker['askPrice'])
            last_bid = float(order_book_ticker['bidPrice'])

            ticker = self.client.get_symbol_ticker(symbol=params.symbol)
            last_price = float(ticker['price'])

            notional = params.quantity * last_price
            if notional < params.min_notional:
                logging.error("[PreBuy]Invalid notional: current notional({:.8f}) < min notional({:.8f})".format(
                    notional, params.min_notional))

                return False

            # calculate buy price
            params.buy_price = "{:.8f}".format(last_bid + params.tick_size * params.price_adjust)

            # calculate breakeven sell price
            params.breakeven_sell_price = float(params.buy_price) * (1 + params.fee / 100)

            # calculate profitable sell price
            params.profitable_sell_price = float(params.buy_price) * (1 + (params.fee + params.profit) / 100)

            # calculate spread percentage
            spread_percentage = (last_ask / last_bid - 1) * 100.0

            logging.info("[PreBuy]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, cbp:{}, cpp:{:.8f}, per:{:.2f}".format(
                last_price, last_ask, last_bid, params.buy_price, params.profitable_sell_price, spread_percentage))

            return last_ask >= params.breakeven_sell_price
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
                logging.info("[Buy]Order(orderId={}, status={}) is filed.".format(order['orderId'], order['status']))
                return order

            logging.info("[Buy]Order(orderId={}, status={}) is not filed.".format(order['orderId'], order['status']))
            return None
        except Exception as e:
            logging.error("[Buy Exception]={}".format(e))
            return None

    def can_sell(self, params):
        try:
            order_book_ticker = self.client.get_orderbook_ticker(symbol=params.symbol)
            last_ask = float(order_book_ticker['askPrice'])
            last_bid = float(order_book_ticker['bidPrice'])

            ticker = self.client.get_symbol_ticker(symbol=params.symbol)
            last_price = float(ticker['price'])

            # calculate sell price
            params.sell_price = "{:.8f}".format(last_price - params.tick_size)

            # calculate spread percentage
            spread_percentage = (last_ask / last_bid - 1) * 100.0

            logging.info("[PreSell]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, csp:{}, cpp:{:.8f}, per:{:.2f}".format(
                last_price, last_ask, last_bid, params.sell_price, params.profitable_sell_price, spread_percentage))

            return last_price >= params.profitable_sell_price
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
                logging.info("[Sell]Order(orderId={}, status={}) is filed.".format(order['orderId'], order['status']))
                return order

            logging.info("[Sell]Order(orderId={}, status={}) is not filed.".format(order['orderId'], order['status']))
            return None
        except Exception as e:
            logging.error("[Sell]={}".format(e))
            return None
