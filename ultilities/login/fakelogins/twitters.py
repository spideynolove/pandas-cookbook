import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    name = 'twitter'
    config_data = load_info(name.upper())
    to = rand_timeout(10, 20)
        
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    # browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    await page.wait_for_timeout(to)
    await page.goto("https://twitter.com/")
    await page.wait_for_timeout(to)
    # await page.get_by_test_id("login").click()
    await page.get_by_test_id("loginButton").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("Phone, email, or username").fill(config_data['username'])
    await page.wait_for_timeout(to)
    await page.get_by_role("button", name="Next").click()
    await page.wait_for_timeout(to)
    await page.get_by_test_id("ocfEnterTextTextInput").fill("spideynolove")
    await page.wait_for_timeout(to)
    await page.get_by_test_id("ocfEnterTextNextButton").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("Password", exact=True).fill(config_data['password'])
    await page.wait_for_timeout(to)
    await page.get_by_test_id("LoginForm_Login_Button").click()
    await page.wait_for_timeout(to)
    await page.get_by_label("X", exact=True).click()
    await page.wait_for_timeout(to)
    await page.goto("https://twitter.com/search?q=%24GBPUSD&src=cashtag_click")
    await page.wait_for_timeout(to)
    await page.get_by_role("tab", name="Latest").click()
    await page.wait_for_timeout(to)
    await context.storage_state(path=f"{grandparent_folder}/{name.upper()}/{name}.json")
    await page.wait_for_timeout(to)
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())