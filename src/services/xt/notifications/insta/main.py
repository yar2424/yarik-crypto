# run notifs entrypoints
from datetime import datetime, timedelta

from src.config import config
from src.db.repositories.telegram.NotifsRateLimiting import (
    get_last_sent,
    update_last_sent_now,
)
from src.services.xt.notifications.insta.notifications.funding_rate_neg_1 import (
    get_notif_to_fire as get_notif_to_fire_funding_rate_neg,
)
from src.services.xt.notifications.insta.notifications.index_mark import (
    get_notif_to_fire as get_notif_to_fire_index_mark,
)
from src.services.xt.notifications.insta.notifications.mark_last import (
    get_notif_to_fire as get_notif_to_fire_mark_last,
)
from src.services.xt.types_ import TickerAnalyticsDataPoint
from src.utils.telegram import (
    send_message,
    send_message_broadcast,
    send_message_broadcast_chats,
)

notif_prefix = "xt"


def last_30_ticks_table_url_template(symbol: str):
    return f"{config['back_url']}/xt/n_last_ticks_table?symbol={symbol}&n=30"


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


def main(data_point: TickerAnalyticsDataPoint, symbol: str):
    handle_mark_last(data_point, symbol)
    handle_index_mark(data_point, symbol)


# handlers


def handle_mark_last(data_point: TickerAnalyticsDataPoint, symbol: str):
    value = data_point["mark_last_delta_div_mark"]
    notif_to_fire = get_notif_to_fire_mark_last(value)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire}"

    print(f"wanna fire: {full_notif_name} with current value: {value}")

    message_to_send = f"""
{full_notif_name}
Last value: {value:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast_chats(message_to_send, ["all", "prior"])
        update_last_sent_now(full_notif_name)


def handle_index_mark(data_point: TickerAnalyticsDataPoint, symbol: str):
    value = data_point["index_mark_delta_div_index"]
    notif_to_fire = get_notif_to_fire_index_mark(value)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire}"

    print(f"wanna fire: {full_notif_name} with current value: {value}")

    message_to_send = f"""
{full_notif_name}
Last value: {value:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast(message_to_send)
        update_last_sent_now(full_notif_name)


def handle_funding_rate_neg(data_point: TickerAnalyticsDataPoint, symbol: str):
    value = data_point["funding_rate"]
    notif_to_fire = get_notif_to_fire_funding_rate_neg(value)
    if not notif_to_fire:
        return
    full_notif_name = f"{notif_prefix}-{symbol}-{notif_to_fire}"

    print(f"wanna fire: {full_notif_name} with current value: {value}")

    message_to_send = f"""
{full_notif_name}
Last value: {value:f}
Last 30 data points: {last_30_ticks_table_url_template(symbol)}
"""

    if should_send_notif_rate_limit(full_notif_name):
        send_message_broadcast(message_to_send)
        update_last_sent_now(full_notif_name)
