import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'tradingeconomics'
    config_data = load_info(name.upper())
    to = rand_timeout()
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto(f"https://{name}.com/")
    await page.wait_for_timeout(to)
    await page.locator("#ctl00_NavigationUC1_ctl00_menuGuest").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("link", name="Already a user? Login").click()
    await page.wait_for_timeout(to)
    await page.get_by_placeholder("Email").click()
    await page.wait_for_timeout(to)
    await page.get_by_placeholder("Email").fill(config_data['username'])
    await page.wait_for_timeout(to)
    await page.locator("#nextActiveButton").click()
    await page.wait_for_timeout(to)
    await page.locator("#ToLogin_Password").click()
    await page.wait_for_timeout(to)
    await page.locator("#ToLogin_Password").fill(config_data['password'])
    await page.wait_for_timeout(to)
    await page.locator("#logInActiveButton").click()
    await page.wait_for_timeout(to)
    # await page.locator("#ctl00_NavigationUC1_ctl00_menu").get_by_role("link", name="Calendar").click()
    # await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())