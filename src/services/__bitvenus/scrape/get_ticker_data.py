import asyncio
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta

import httpx
import playwright
import playwright.async_api
from playwright.async_api import async_playwright
from typing_extensions import List, cast

from src.services.bingx.types_ import ApiResponse, Contract
from src.services.bitvenus.types_ import ScrapingResult
from src.services.mexc.types_ import Ticker, TickersResponse
from src.utils.utils import split_list, timeit_context

TIMEOUT = 100000


async def scrape_last_price(page: playwright.async_api.Page):
    last_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[1]/p"
    locator = page.locator(f"xpath=/{last_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for(timeout=TIMEOUT)

    # Get the (first) element using XPath
    element_handle = locator.first

    # Retrieve the text content, ID, and class name
    text_content: str = await element_handle.text_content()  # type: ignore

    price_str_clean = text_content.replace(",", "")
    price = float(price_str_clean)
    print("finished last")
    return price


async def scrape_index_price(page: playwright.async_api.Page):
    print("started index")
    index_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/ul/li[2]/p[2]"
    locator = page.locator(f"xpath=/{index_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for(timeout=TIMEOUT)

    # Get the (first) element using XPath
    element_handle = locator.first

    # Continuously check the text content until it differs from the placeholder value "--"
    placeholder = "--"
    while True:
        text_content: str = await element_handle.text_content()  # type: ignore
        if text_content != placeholder:
            break
        await asyncio.sleep(0.1)

    # Retrieve the text content, ID, and class name
    text_content: str = await element_handle.text_content()  # type: ignore

    price_str_clean = text_content.replace(",", "")
    price = float(price_str_clean)
    print("finished index")
    return price


async def scrape_mark_price(page: playwright.async_api.Page):
    mark_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/ul/li[3]/p[2]"
    locator = page.locator(f"xpath=/{mark_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for(timeout=TIMEOUT)

    # Get the (first) element using XPath
    element_handle = locator.first

    # Continuously check the text content until it differs from the placeholder value "--"
    placeholder = "--"
    while True:
        text_content: str = await element_handle.text_content()  # type: ignore
        if text_content != placeholder:
            break
        await asyncio.sleep(0.1)

    # Retrieve the text content, ID, and class name
    text_content: str = await element_handle.text_content()  # type: ignore

    price_str_clean = text_content.replace(",", "")
    price = float(price_str_clean)

    print("finished mark")

    return price


async def scrape_page_main(
    url: str,
    symbol: str,
    page: playwright.async_api.Page,
) -> ScrapingResult:
    await page.goto(url)

    scraped: ScrapingResult = {
        "symbol": symbol,
        "index_price": await scrape_index_price(page),
        "mark_price": await scrape_mark_price(page),
        "last_price": await scrape_last_price(page),
    }

    return scraped


def get_tokens_list():
    funding_rates = httpx.get(
        "https://futures.bitvenus.com/api/contract/funding_rates?language=en-us"
    ).json()
    token_names = [fr["tokenId"] for fr in funding_rates]
    return token_names


def url_template(symbol: str):
    return f"https://futures.bitvenus.com/en-US/contract/{symbol}"


def process_wrapper(task_group: List[str]):
    asyncio.run(process_task_group(task_group))


async def process_task_group(task_group: List[str]) -> List[ScrapingResult]:
    async with async_playwright() as p:
        async with await p.chromium.launch(headless=True) as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    with timeit_context("no new pages"):
                        scraping_results: List[ScrapingResult] = []
                        for task in task_group:
                            url = url_template(task)
                            scraping_results.append(
                                await scrape_page_main(url, task, page)
                            )
    return scraping_results


async def get_tickers_data() -> List[ScrapingResult]:
    # split work horizon into parallelism_level (list of list of tasks (symbols))
    # for each list of tasks - start process that will sequentially do tasks
    # gather results from processes

    symbols = get_tokens_list()[:20]
    symbols_clean = [s.replace("-SWAP-", "") for s in symbols]

    urls = [url_template(s) for s in symbols_clean]

    parallelism_level = 10  # number of processes/browsers/tabs/sessions

    task_groups = split_list(urls, parallelism_level)

    with ProcessPoolExecutor(max_workers=parallelism_level) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_wrapper, task_group)
            for task_group in task_groups
        ]
        tasks_outs = await asyncio.gather(*tasks)

    print(tasks_outs)
