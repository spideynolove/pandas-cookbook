import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'fxstreet'
    config_data = load_info(name.upper())
    to = rand_timeout()
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto("https://www.fxstreet.com/")
    await page.wait_for_timeout(to)
    await page.get_by_text("CONTINUE TO SITE").click()
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="Log in").click()
    await page.wait_for_timeout(to)

    # page.get_by_role("button", name="Continue w/ email address").click()
    # page.wait_for_timeout(to)

    # page.get_by_placeholder("youremail@example.com").click()
    # page.wait_for_timeout(to)
    
    await page.get_by_placeholder("youremail@example.com").fill(config_data['username'])
    await page.wait_for_timeout(to)
    
    # page.get_by_placeholder("Your password").click()
    # page.wait_for_timeout(to)
    
    await page.get_by_placeholder("Your password").fill(config_data['password'])
    await page.wait_for_timeout(to)
    
    await page.get_by_role("button", name="Log in").click()
    
    # page.wait_for_timeout(5000)
    # page.get_by_role("button", name="Cancel").click()
    
    await page.wait_for_timeout(to)
    await page.locator("#fxs_socialLogo_header").get_by_role("link", name="FXStreet - The forex market").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())



