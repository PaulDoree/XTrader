#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from .strategy import Strategy


class TestStrategy(Strategy):
    def consult_buy_strategy(self, client, data):
        logging.info("[TestStrategy]Consult buy strategy")
        return False

    def consult_sell_strategy(self, client, data):
        logging.info("TestStrategy]Consult sell strategy")
        return False
