import functools as ft
import typing as t

import pandas as pd
import numpy as np
from numba import njit

from .report import Report


def simulate(available_fiat: float, target: pd.DataFrame,
             velocity: t.Union[pd.DataFrame, pd.Series],
             price: pd.DataFrame, fee: float,
             buy_expiration: int = 10, sell_expiration: int = 10,
             target_periods: int = 86400) -> Report:
    target = _limit_row_sum(target).fillna(0.)
    target, velocity, price = _align_labels(target,
                                            velocity, price)
    costs, proceeds, holdings = _simulate(available_fiat, target.values,
                                          velocity.values, price.values, fee,
                                          buy_expiration=buy_expiration,
                                          sell_expiration=sell_expiration,
                                          target_periods=target_periods)
    holdings = pd.DataFrame(holdings, target.index, ['$', *target.columns])
    return Report(initial_aum=available_fiat,
                  final_aum=holdings.iloc[-1].sum(),
                  max_aum=holdings.sum(axis=1).max(),
                  holdings=holdings,
                  costs=pd.Series(costs, target.columns),
                  proceeds=pd.Series(proceeds, target.columns))


def _limit_row_sum(df: pd.DataFrame, to: float = 1.) -> pd.DataFrame:
    """
    Ensure each row sums to no more than one.
    :param df: the DataFrame to limit
    :return: the limited DataFrame
    """
    denominator = np.maximum(df.sum(axis=1), to)
    limited_fraction = (df.transpose() / denominator * to).transpose()
    return limited_fraction


def _align_labels(target: pd.DataFrame,
                  velocity: t.Union[pd.DataFrame, pd.Series],
                  price: pd.DataFrame):
    if isinstance(velocity, pd.DataFrame):
        target, velocity, price = _align_columns(target,
                                                 velocity, price)
    else:
        target, price = _align_columns(target, price)
    target, velocity, price = _align_index(target,
                                           velocity, price)
    return target, velocity, price


def _align_columns(*args: pd.DataFrame):
    columns = ft.reduce(lambda a, v: a.intersection(v),
                        map(lambda df: df.columns, args))
    return tuple(map(lambda df: df[columns], args))


def _align_index(buy_fraction: pd.DataFrame,
                 sell_fraction: pd.DataFrame,
                 price: pd.DataFrame):
    buy_fraction = buy_fraction.resample('S').ffill()
    sell_fraction = sell_fraction.resample('S').ffill()
    price = price.resample('S').asfreq()
    max_min = max(buy_fraction.index.min(), sell_fraction.index.min(),
                  price.index.min())
    min_max = min(buy_fraction.index.max(), sell_fraction.index.max(),
                  price.index.max())
    buy_fraction = buy_fraction.loc[max_min:min_max]
    sell_fraction = sell_fraction.loc[max_min:min_max]
    price = price.loc[max_min:min_max]
    return buy_fraction, sell_fraction, price


# Grandchild of np.deg2rad

@njit
def nan2zero(x: np.ndarray) -> np.ndarray:
    return np.where(np.isnan(x) | np.isinf(x), 0., x)


@njit
def _determine_weights(current: np.array, target: np.array,
                       velocity: np.ndarray, p: int) -> np.array:
    """
    Determines how much to spend on/of each asset instantaneously
    :param current: the current allocations
    :param target: the target allocation
    :param velocity: edge - risk level a la Kelly Criterion
    :param p: the number of periods over which to reach the target
    :returns: fraction of portfolio to spend on each asset
    :returns: fraction of asset to sell
    """
    over_allocation = np.maximum(current - target, 0.)
    total_over = over_allocation.sum()
    if total_over:
        avg_over_velocity = (over_allocation * velocity).sum() / total_over
    else:
        avg_over_velocity = 0.
    under_allocation = np.maximum(target - current, 0.)
    total_under = under_allocation.sum()
    if total_under:
        avg_under_velocity = (under_allocation * velocity).sum() / total_under
    else:
        avg_under_velocity = 0.
    total_allocation = np.abs(current).sum()
    cc = nan2zero(total_allocation * over_allocation / total_over)
    v_sell = cc * avg_under_velocity - velocity
    ccc = nan2zero(total_allocation * under_allocation / total_under)
    v_buy = velocity - ccc * avg_over_velocity
    sell_delta = np.maximum(current - target, 0.)
    sell = sell_delta * _compute_step_length(p, v_sell)
    buy_delta = np.maximum(target - current, 0.)
    buy = buy_delta * _compute_step_length(p, v_buy)
    return buy, sell


@njit
def _compute_step_length(p: int, velocity: np.ndarray) -> np.ndarray:
    return (1 - ((p - 1) / p) ** np.exp(velocity)) * np.e


@njit
def _simulate(starting_fiat: float, target: np.array, velocity: np.array,
              price: np.array, fee: float, buy_expiration: int,
              sell_expiration: int, target_periods: int) -> np.array:
    """
    Simulate a portfolio's trading activity + returns
    :param target_periods:
    :param starting_fiat: the starting fiat balance
    :param target: [t, m] = fraction of fiat to spend on m at t
    :param velocity: [t, m] = fraction of balance[m] to sell at t
    :param price: [t, m] = price of m at t
    :param fee: fee paid to exchange as fraction of spending amount
    :param buy_expiration: the number of periods after which the buy expires
    :param sell_expiration: the number of periods after which the sell expires
    :return: the final market value of the portfolio
    """
    m = target.shape[1]
    buy_sizes = np.zeros((buy_expiration, m))
    buy_prices = np.zeros((buy_expiration, m))
    sell_sizes = np.zeros((sell_expiration, m))
    sell_prices = np.zeros((sell_expiration, m))
    available_balance = np.zeros(m)
    total_balance = np.zeros(m)
    pending_buy_size = np.zeros(m)
    available_fiat = starting_fiat
    total_fiat = starting_fiat
    most_recent_price = price[0]
    cost_tracker, proceeds_tracker = np.zeros(m), np.zeros(m)
    holdings_tracker = np.zeros((target.shape[0], m + 1))
    for i in range(target.shape[0]):
        most_recent_price = np.where(np.isnan(price[i]),
                                     most_recent_price, price[i])
        # holds -> balance
        buy_fills = buy_prices > price[i]  # filled if market moves below price
        pw_fills_cost = (buy_sizes * buy_fills * buy_prices).sum(axis=0)
        fiat_fill_total = pw_fills_cost.sum()
        available_fiat -= fiat_fill_total * fee
        cost_tracker += pw_fills_cost * (1 + fee)
        total_fiat -= fiat_fill_total * (1 + fee)
        filled_size = (buy_sizes * buy_fills).sum(axis=0)
        pending_buy_size -= filled_size
        available_balance += filled_size
        total_balance += filled_size
        buy_sizes = np.where(buy_fills, 0., buy_sizes)
        # holds -> fiat
        sell_fills = sell_prices < price[i]
        total_balance -= (sell_sizes * sell_fills).sum(axis=0)
        pw_proceeds = (sell_sizes * sell_fills * sell_prices).sum(axis=0)
        proceeds = pw_proceeds.sum()
        proceeds_tracker += pw_proceeds * (1 - fee)
        net_proceeds = proceeds * (1 - fee)
        available_fiat += net_proceeds
        total_fiat += net_proceeds
        sell_sizes = np.where(sell_fills, 0., sell_sizes)
        # weight computation
        m2mv = total_balance * nan2zero(most_recent_price)
        aum = m2mv.sum() + total_fiat
        current_allocation = m2mv / aum
        buy_delta, sell_delta = _determine_weights(current_allocation,
                                                   target[i], velocity[i],
                                                   target_periods)
        # expiration
        sell_retry = sell_delta > 0.
        buy_retry = buy_delta > 0.
        buy_offset, sell_offset = i % buy_expiration, i % sell_expiration
        retry_base_amount = sell_retry * sell_sizes[sell_offset]
        available_balance += sell_sizes[sell_offset] - retry_base_amount
        retry_buy_size = buy_retry * buy_sizes[buy_offset]
        retry_buy_amount = retry_buy_size * buy_prices[buy_offset]
        release_buy_size = (buy_sizes[buy_offset] - retry_buy_size)
        available_fiat += release_buy_size @ buy_prices[buy_offset]
        pending_buy_size -= buy_sizes[buy_offset]
        # buys -> holds
        fiat_spend_fraction = nan2zero(buy_delta * aum / available_fiat)
        if fiat_spend_fraction.sum() > 1:
            fiat_spend_fraction /= fiat_spend_fraction.sum()
        new_buy_amount = available_fiat * fiat_spend_fraction
        buy_quote_amount = new_buy_amount + retry_buy_amount
        available_fiat -= buy_quote_amount.sum()
        buy_base_amount = nan2zero(buy_quote_amount / most_recent_price)
        buy_sizes[buy_offset] = buy_base_amount
        pending_buy_size += buy_base_amount
        buy_prices[buy_offset] = nan2zero(most_recent_price)
        # sells -> holds
        sell_fraction = nan2zero(sell_delta / current_allocation)
        sell_base_amount = available_balance * sell_fraction
        available_balance -= sell_base_amount
        sell_sizes[sell_offset] = sell_base_amount + retry_base_amount
        sell_prices[sell_offset] = nan2zero(most_recent_price)
        holdings_tracker[i, 0] = total_fiat
        holdings_tracker[i, 1:] = total_balance * nan2zero(most_recent_price)
        continue
    m2m_final = total_balance * most_recent_price
    proceeds_tracker += nan2zero(m2m_final)
    return cost_tracker, proceeds_tracker, holdings_tracker


__all__ = ['simulate']
