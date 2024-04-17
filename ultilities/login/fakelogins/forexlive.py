import asyncio
from playwright.async_api import async_playwright
from loginhelpers import *


async def run(playwright):
    config_data = load_info("FOREXLIVE")
    to = rand_timeout(10, 30)
        
    chromium = playwright.chromium
    # browser = await chromium.launch(headless=False)
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    page.wait_for_timeout(to)
    page.goto("https://www.financemagnates.com/")
    page.wait_for_timeout(to)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_timeout(to)
    page.get_by_role("button", name="Email login").click()
    page.wait_for_timeout(to)
    page.locator("#sign-in-email-form input[type=\"text\"]").click()
    page.wait_for_timeout(to)
    page.locator("#sign-in-email-form input[type=\"text\"]").fill(config_data['username'])
    page.wait_for_timeout(to)
    page.locator("input[type=\"password\"]").click()
    page.wait_for_timeout(to)
    page.locator("input[type=\"password\"]").fill(config_data['password'])
    page.wait_for_timeout(to)
    page.locator("#sign-in-email-form").get_by_role("button", name="SIGN IN").click()
    page.wait_for_timeout(to)
    page.get_by_role("link", name="Financial and Business News").click()
    page.wait_for_timeout(to)
    context.storage_state(path=f"{parent_folder}/saved-states/fxlivestate.json")
    page.wait_for_timeout(to)
    context.close()
    browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
