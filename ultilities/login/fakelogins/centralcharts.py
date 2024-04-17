import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'centralcharts'
    config_data = load_info(name.upper())
    to = rand_timeout()
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto("https://www.centralcharts.com/en/login")
    await page.wait_for_timeout(to)
    await page.click("[placeholder=\"Email address or Username\"]")
    await page.wait_for_timeout(to)
    await page.fill("[placeholder=\"Email address or Username\"]", config_data['username'])
    await page.wait_for_timeout(to)
    await page.click("[placeholder=\"Password\"]")
    await page.wait_for_timeout(to)
    await page.fill("[placeholder=\"Password\"]", config_data['password'])
    await page.wait_for_timeout(to)
    await page.click("[id=\"submit\"]")
    await page.goto("https://www.centralcharts.com/en")
    await page.wait_for_timeout(to)
    await page.get_by_role("link", name="CentralCharts").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
