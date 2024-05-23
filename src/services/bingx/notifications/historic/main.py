# run notifs entrypoints
from datetime import datetime, timedelta

from typing_extensions import List

from src.config import config
from src.db.repositories.telegram.NotifsRateLimiting import (
    get_last_sent,
    update_last_sent_now,
)
from src.services.bingx.notifications.historic.notifications.fair_trade_3_ticks import (
    get_notif_to_fire as get_notif_to_fire_fair_trade_3_ticks,
)
from src.services.bingx.notifications.historic.notifications.funding_rate_neg_3_ticks import (
    get_notif_to_fire as get_notif_to_fire_funding_rate_neg_3_ticks,
)
from src.services.bingx.notifications.historic.notifications.index_fair_3_ticks import (
    get_notif_to_fire as get_notif_to_fire_index_fair_3_ticks,
)
from src.services.bingx.types_ import TickerAnalyticsDataPoint
from src.utils.telegram import send_message, send_message_broadcast

notif_prefix = "bingx"


def last_30_ticks_table_url_template(symbol: str):
    return f"{config['back_url']}/bingx/n_last_ticks_table?symbol={symbol}&n=30"


def should_send_notif_rate_limit(notif_name: str):
    "returns true if rate limit is not exceeded (if current notif is more than 1 hour apart from prev)"
    last_sent = get_last_sent(notif_name)
    if not last_sent:
        return False
    now = datetime.utcnow()
    delta = now - last_sent
    if delta > timedelta(hours=1):
        return True
    return False


def main(data_points: List[TickerAnalyticsDataPoint], symbol: str):
    handle_fair_trade(data_points, symbol)
    handle_index_fair(data_points, symbol)
    handle_funding_rate_neg(data_points, symbol)


# handle others


def handle_fair_trade(data_points: List[TickerAnalyticsDataPoint], symbol: str):
    notif_to_fire = get_notif_to_fire_fair_trade_3_ticks(data_points)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire['name']}"

    print(
        f"wanna fire: {full_notif_name} with current value: {notif_to_fire['last_value']}"
    )

    priority_visual = "❗" * notif_to_fire["priority"]

    message_to_send = f"""
{priority_visual}
{full_notif_name}
Last value: {notif_to_fire['last_value']:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast(message_to_send)
        update_last_sent_now(full_notif_name)


def handle_index_fair(data_points: List[TickerAnalyticsDataPoint], symbol: str):
    notif_to_fire = get_notif_to_fire_index_fair_3_ticks(data_points)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire}"

    print(
        f"wanna fire: {full_notif_name} with current value: {notif_to_fire['last_value']}"
    )

    priority_visual = "❗" * notif_to_fire["priority"]

    message_to_send = f"""
{priority_visual}
{full_notif_name}
Last value: {notif_to_fire['last_value']:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast(message_to_send)
        update_last_sent_now(full_notif_name)


def handle_funding_rate_neg(data_points: List[TickerAnalyticsDataPoint], symbol: str):
    notif_to_fire = get_notif_to_fire_funding_rate_neg_3_ticks(data_points)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire}"

    print(
        f"wanna fire: {full_notif_name} with current value: {notif_to_fire['last_value']}"
    )

    priority_visual = "❗" * notif_to_fire["priority"]

    message_to_send = f"""
{priority_visual}
{full_notif_name}
Last value: {notif_to_fire['last_value']:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast(message_to_send)
        update_last_sent_now(full_notif_name)
