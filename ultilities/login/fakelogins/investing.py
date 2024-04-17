import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'investing'
    config_data = load_info(name.upper())
    to = rand_timeout()
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto("https://www.investing.com")
    await page.wait_for_timeout(rand_timeout(34, 55))
    await page.get_by_role("link", name="Sign In").click()
    
    # await page.goto("https://www.investing.com/login/")
    
    await page.wait_for_timeout(to)
    await page.get_by_placeholder("Email").fill(config_data['username'])
    await page.wait_for_timeout(to)
    await page.get_by_placeholder("Password").fill(config_data['password'])
    await page.wait_for_timeout(to)
    await page.get_by_placeholder("Password").press("Enter")
    await page.wait_for_timeout(to)
    await page.get_by_role("link", name="Investing.com - Financial Markets Worldwide").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
