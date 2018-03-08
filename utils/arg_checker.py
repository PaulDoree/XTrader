#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentTypeError


def quantity_float(value):
    quantity = float(value)
    if quantity <= 0:
        raise ArgumentTypeError("invalid quantity: {}, and quantity must be greater than 0!".format(quantity))
    return quantity


def profit_float(value):
    profit = float(value)
    if profit < 0.3:
        raise ArgumentTypeError("invalid profit: {}, and profit must be greater than or equal to 0.3!".format(profit))
    return profit


def fee_float(value):
    fee = float(value)
    if fee < 0:
        raise ArgumentTypeError("invalid fee: {}, and fee must be greater than or equal to 0!".format(fee))
    return fee


def price_adjust_int(value):
    price_adjust = int(value)
    if price_adjust < 1:
        raise ArgumentTypeError("invalid price_adjust: {}, and price_adjust must be greater than or equal to 1!".format(price_adjust))
    return price_adjust


def count_int(value):
    count = int(value)
    if count < 1:
        raise ArgumentTypeError("invalid count: {}, and count must be greater than or equal to 1!".format(count))
    return count
