#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .strategy import Strategy


class TestStrategy(Strategy):
    def consult_buy_strategy(self, client, data):
        return False

    def consult_sell_strategy(self, client, data):
        return False
