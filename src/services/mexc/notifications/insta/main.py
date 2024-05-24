# run notifs entrypoints
from datetime import datetime, timedelta

from src.config import config
from src.db.repositories.telegram.NotifsRateLimiting import (
    get_last_sent,
    update_last_sent_now,
)
from src.services.mexc.notifications.insta.notifications.fair_last import (
    get_notif_to_fire as get_notif_to_fire_fair_last,
)
from src.services.mexc.notifications.insta.notifications.funding_rate_neg_1 import (
    get_notif_to_fire as get_notif_to_fire_funding_rate_neg,
)
from src.services.mexc.notifications.insta.notifications.index_fair import (
    get_notif_to_fire as get_notif_to_fire_index_fair,
)
from src.services.mexc.types_ import TickerAnalyticsDataPoint
from src.utils.telegram import (
    send_message,
    send_message_broadcast,
    send_message_broadcast_chats,
)

notif_prefix = "mexc"


def last_30_ticks_table_url_template(symbol: str):
    return f"{config['back_url']}/mexc/n_last_ticks_table?symbol={symbol}&n=30"


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
    handle_fair_last(data_point["fair_last_delta_div_fair"], symbol)
    handle_index_fair(data_point["index_fair_delta_div_index"], symbol)
    handle_funding_rate_neg(data_point["funding_rate"], symbol)


# handle others


def handle_fair_last(value: float, symbol: str):
    notif_to_fire = get_notif_to_fire_fair_last(value)
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


def handle_index_fair(value: float, symbol: str):
    notif_to_fire = get_notif_to_fire_index_fair(value)
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


def handle_funding_rate_neg(value: float, symbol: str):
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
