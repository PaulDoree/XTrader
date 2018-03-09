#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def consult_buy_strategy(self, client, data):
        pass

    @abstractmethod
    def consult_sell_strategy(self, client, data):
        pass
