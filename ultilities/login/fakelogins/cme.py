import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'cme'
    config_data = load_info(name.upper())
    to = rand_timeout()

    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto("https://www.cmegroup.com/")
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="Log In").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("EMAIL / USER ID").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("EMAIL / USER ID").fill(config_data['username'])
    await page.wait_for_timeout(to)
    await page.locator("#pwd").click()
    await page.wait_for_timeout(to)
    await page.locator("#pwd").fill(config_data['password'])
    await page.wait_for_timeout(to)
    await page.get_by_text("Remember my email/user ID next time").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="LOG IN").click()
    await page.wait_for_timeout(to)
    # await page.get_by_role("button", name="Close").filter(has_text="Close").click()
    # await page.wait_for_timeout(to)
    await page.locator("#collapsibleNavbarMenu").get_by_role("link", name="Markets").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("link", name="FX").nth(1).click()
    await page.wait_for_timeout(to)
    await page.goto("https://www.cmegroup.com/markets/fx.html#products")
    await page.wait_for_timeout(to)
    await page.goto("https://www.cmegroup.com/markets/fx.html#overview")
    await page.wait_for_timeout(to)
    await page.goto("https://www.cmegroup.com/markets/fx.html#products")
    await page.wait_for_timeout(to)
    await page.goto("https://www.cmegroup.com/markets/fx.html#tools")
    await page.wait_for_timeout(to)
    await page.get_by_role("link", name="Commitment of Traders Tool View FX market open interest reports based on CFTC reports in a comprehensive graph format. ").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
