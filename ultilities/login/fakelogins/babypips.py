import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'babypips'
    config_data = load_info(name.upper())
    to = rand_timeout()
    
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto(f"https://www.{name}.com/account/sign-in")
    await page.wait_for_timeout(to)
    await page.click("[placeholder=\"Email or Username\"]")
    await page.wait_for_timeout(to)
    await page.fill("[placeholder=\"Email or Username\"]", config_data['username'])
    await page.wait_for_timeout(to)
    await page.click("[placeholder=\"Password\"]")
    await page.wait_for_timeout(to)
    await page.fill("[placeholder=\"Password\"]", config_data['password'])
    await page.wait_for_timeout(to)
    await page.click("button:has-text(\"Sign In\")")
    await page.wait_for_timeout(to)
    await page.get_by_role("navigation").get_by_role("link", name="MarketMilk™").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())