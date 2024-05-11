import httpx
from typing_extensions import List

from src.config import config
from src.services.scrapers.mexc.types_ import TickerAnalyticsDataPoint
from src.utils.telegram import escape_markdown_v2


def check_notification_1_should_fire(
    ticker_timeseries: List[TickerAnalyticsDataPoint],
) -> bool:
    "check if notification should fire"
    return False


def fire_notification_1():
    """this notif is firing. here is data for last 15 mins. here is link to exchange"""
    message = escape_markdown_v2(
        """*bold text*
_italic text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```
>Block quotation started
>Block quotation continued
>The last line of the block quotation**
>The second block quotation started right after the previous\r
>The third block quotation started right after the previous"""
    )

    for chat_id in config["telegram_chat_ids"]:
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "MarkdownV2"}
        response = httpx.post(
            f"{config['telegram_bot_api_base_url']}/sendMessage", json=payload
        )
        if response.status_code != 200:
            print(response.text)


def fire_notification_2():
    """this notif is firing. here is data for last 15 mins. here is link to exchange"""
    message = """
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>"""

    for chat_id in config["telegram_chat_ids"]:
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        response = httpx.post(
            f"{config['telegram_bot_api_base_url']}/sendMessage", json=payload
        )
        if response.status_code != 200:
            print(response.text)


def fire_notification_3():
    """this notif is firing. here is data for last 15 mins. here is link to exchange"""
    message = """
BTC is going ±crazy!
https://futures.mexc.com/ru-RU/exchange/BTC_USDT
<link to table with last n steps>
"""

    for chat_id in config["telegram_chat_ids"]:
        payload = {
            "chat_id": chat_id,
            "text": message,
        }
        response = httpx.post(
            f"{config['telegram_bot_api_base_url']}/sendMessage", json=payload
        )
        if response.status_code != 200:
            print(response.text)


def check_run_notifications(ticker_timeseries: List[TickerAnalyticsDataPoint]):
    if check_notification_1_should_fire(ticker_timeseries):
        fire_notification_1()
