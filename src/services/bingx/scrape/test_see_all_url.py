import asyncio
from datetime import datetime, timedelta

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )  # Set headless=True if you don't want the browser window to open
        context = await browser.new_context()
        page = await context.new_page()

        should_finish_before = datetime.now() + timedelta(seconds=10)  # for timeout
        should_finish = False  # flip when time to finish (timeout)
        result = {}  # request response data will be stored here

        async def looped_check_update_should_finish():
            "checking until time to update flag and exit"
            while True:
                now = datetime.now()
                if now > should_finish_before:
                    nonlocal should_finish
                    should_finish = True
                    break
                await asyncio.sleep(0.1)

        async def finisher():
            "clean up + return. could also raise error"
            while True:
                if should_finish == True:
                    nonlocal browser, result
                    await browser.close()
                    return result
                await asyncio.sleep(0.1)

        # Event listener to capture and analyze fetch requests
        async def handle_request(request):
            if request.resource_type in ["fetch", "xhr"]:
                print(f"Request: {request.url}")
                response = await request.response()
                if (
                    request.url
                    == "https://api-swap.qq-os.com/api/v1/quote/all/contracts/get?tradingUnit=COIN"
                ):
                    print(f"Response status: {response.status}")
                    try:
                        body = await response.json()
                        # print(f"Response body (JSON): {body}")
                        nonlocal should_finish, result
                        should_finish = True
                        result = body
                        # should return result or error
                    except:
                        text_body = await response.text()
                        print(f"Response body (Text): {text_body}")

        page.on("requestfinished", handle_request)

        # Open a webpage
        await page.goto("https://swap.bingx.com/en/BTC-USDT")

        # Start looper
        asyncio.create_task(looped_check_update_should_finish())

        return await finisher()


async def main_runner():
    result = await main()
    print(result.keys())


# Run the script
asyncio.run(main_runner())
