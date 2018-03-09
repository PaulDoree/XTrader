#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from .strategy import Strategy


class DefaultStrategy(Strategy):
    def consult_buy_strategy(self, client, data):
        try:
            ticker = client.get_ticker(symbol=data.symbol)
            data.last_ask = float(ticker['askPrice'])
            data.last_bid = float(ticker['bidPrice'])
            data.last_price = float(ticker['lastPrice'])

            notional = data.quantity * data.last_price
            if notional < data.min_notional:
                logging.error("[Buy Strategy]Invalid notional: current notional({:.8f}) < min notional({:.8f})".format(
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

            logging.info("[Buy Strategy]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, cbp:{}, cpp:{:.8f}, per:{:.2f}".format(
                data.last_price, data.last_ask, data.last_bid, data.buy_price, data.profitable_sell_price,
                spread_percentage))

            return data.last_ask >= data.breakeven_sell_price
        except Exception as e:
            logging.error("[Buy Strategy Exception]={}".format(e))
            return False

    def consult_sell_strategy(self, client, data):
        try:
            ticker = client.get_ticker(symbol=data.symbol)
            data.last_ask = float(ticker['askPrice'])
            data.last_bid = float(ticker['bidPrice'])
            data.last_price = float(ticker['lastPrice'])

            # calculate sell price
            data.sell_price = "{:.8f}".format(data.last_price - data.tick_size)

            # calculate spread percentage
            spread_percentage = (data.last_ask / data.last_bid - 1) * 100.0

            logging.info("[Sell Strategy]lp:{:.8f}, la:{:.8f}, lb:{:.8f}, csp:{}, cpp:{:.8f}, per:{:.2f}".format(
                data.last_price, data.last_ask, data.last_bid, data.sell_price, data.profitable_sell_price,
                spread_percentage))

            return data.last_price >= data.profitable_sell_price
        except Exception as e:
            logging.error("[Sell Strategy Exception]={}".format(e))
            return False
