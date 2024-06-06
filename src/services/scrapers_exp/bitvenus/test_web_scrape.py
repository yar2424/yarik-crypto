# %%
import asyncio

import playwright
import playwright.async_api
from playwright.async_api import async_playwright


async def scrape_example():
    async with async_playwright() as p:
        # Use the browser as a context manager
        async with await p.chromium.launch(headless=False) as browser:
            # Use the page as a context manager
            async with await browser.new_page() as page:
                # Open the page
                url = "https://futures.bitvenus.com/en-US/contract/BTCUSDT"
                await page.goto(url)

                last_price_xpath = (
                    "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[1]/p"
                )
                locator = page.locator(f"xpath=/{last_price_xpath}")

                # Wait for the element matching the XPath to appear
                await locator.wait_for()

                # Get the (first) element using XPath
                element_handle = locator.first

                # Retrieve the text content, ID, and class name
                text_content = await element_handle.text_content()
                element_id = await element_handle.get_attribute("id")
                class_name = await element_handle.get_attribute("class")

                # Print the retrieved values
                print(f"Text Content: {text_content}")
                print(f"ID: {element_id}")
                print(f"Class Name: {class_name}")


async def scrape_last_price(page: playwright.async_api.Page):
    last_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[1]/p"
    locator = page.locator(f"xpath=/{last_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for()

    # Get the (first) element using XPath
    element_handle = locator.first

    # Retrieve the text content, ID, and class name
    text_content: str = await element_handle.text_content()  # type: ignore

    price_str_clean = text_content.replace(",", "")
    price = float(price_str_clean)

    return price


async def scrape_index_price(page: playwright.async_api.Page):
    index_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/ul/li[2]/p[2]"
    locator = page.locator(f"xpath=/{index_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for()

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

    return price


async def scrape_mark_price(page: playwright.async_api.Page):
    mark_price_xpath = "/html/body/main/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/ul/li[3]/p[2]"
    locator = page.locator(f"xpath=/{mark_price_xpath}")

    # Wait for the element matching the XPath to appear
    await locator.wait_for()

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

    return price


async def scrape_page_main():
    async with async_playwright() as p:
        # Use the browser as a context manager
        async with await p.chromium.launch(headless=False) as browser:
            # Use the page as a context manager
            async with await browser.new_page() as page:
                # Open the page
                url = "https://futures.bitvenus.com/en-US/contract/BTCUSDT"
                await page.goto(url)

                scraped = {}
                # pass page to handlers
                scraped["index_price"] = await scrape_index_price(page)
                scraped["mark_price"] = await scrape_mark_price(page)
                scraped["last_price"] = await scrape_last_price(page)
                print(scraped)


# Run the async function
# asyncio.run(scrape())

# %%
# await scrape_page_main()
# %%
