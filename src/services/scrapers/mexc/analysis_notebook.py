# %%

from typing_extensions import List

from services.scrapers.mexc.types_ import TickerAnalyticsDataPoint

# %%


data = [{}, {}, {}]
deltas = ["d1", "d2", "d3"]
# %%
# logic with the array of past deltas
# send notif


# %%
"""
table to store events (in timeseries)

get timeseries object locally (array + step(time delta))
logic that works with this dt
    e.g. how long is the time window inspected
    get some alnalytics, metric
    modify it somehow (add record, add field)
"""
# %%


class TickerTimeseriesAnalysis_NotifSender:
    def __init__(self):
        self.timeseries: List[TickerAnalyticsDataPoint] = []

    @classmethod
    def load(cls, symbol: str):
        "loads from db using repository methods"
        pass

    def check_notification_1_should_fire(self) -> bool:
        "check if notification should fire"
        return False

    def fire_notification_1(self):
        """"""


class TickerAnalyticsDataPointCreator:
    "new TickerAnalyticsDataPoint creator"

    def __init__(self):
        self.timeseries: List[TickerAnalyticsDataPoint] = []

    @classmethod
    def load(cls):
        "loads from db using repository methods"
        pass

    def sync_push(self):
        "sync/push state of the timeseries into db (some records are updated (last n?))"
        pass

    def populate_last_div_fair(self):
        pass

    def populate_delta_div_avg(self):
        pass

    def main(self):
        self.load()
        self.populate_last_div_fair()
        self.populate_delta_div_avg()
        self.sync_push()


# %%
"db + api -> get historic data"
# %%
"update db and google sheets every timestamp"
