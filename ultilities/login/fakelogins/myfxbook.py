import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'myfxbook'
    config_data = load_info(name.upper())
    to = rand_timeout()
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto(f"https://www.{name}.com/")
    await page.wait_for_timeout(to)
    await page.locator("#popupAdContainer").get_by_text("Continue to Myfxbook.com").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="Sign In").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("Email").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("Email").fill(config_data['username'])
    await page.wait_for_timeout(to)
    await page.get_by_label("Password").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("Password").fill(config_data['password'])
    await page.wait_for_timeout(to)
    await page.locator("label").filter(has_text="Remember").locator("span").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="Login").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("navigation", name="FX Tools").get_by_role("link", name="Sentiment").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())