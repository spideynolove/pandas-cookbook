# # ---------------------------- babypips ----------------------------
# import asyncio
from playwright.async_api import async_playwright


# async def run(playwright):
#     browser = playwright.chromium.launch(headless=False)

#     context = browser.new_context(storage_state=f"saved-states/forexlive.json")
#     page = context.new_page()
#     page.wait_for_timeout(500)
#     page.goto("https://www.financemagnates.com/")
#     page.wait_for_timeout(5000)
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)

import cloudscraper
import asyncio
from playwright.async_api import async_playwright, expect
from pathlib import Path
parent_folder = Path(__file__).parent.resolve().parent

async def run(playwright):
    scraper = cloudscraper.create_scraper()  
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    context = await browser.new_context()
    page.goto("https://www.forexfactory.com/")
    page.wait_for_timeout(1000)
    scraper.get("https://www.forexfactory.com/")
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Login").click()
    page.wait_for_timeout(1000)
    page.get_by_label("User/Email:").click()
    page.wait_for_timeout(1000)
    page.get_by_label("User/Email:").fill("marika16792.gamer@gmail.com")
    page.wait_for_timeout(1000)
    page.get_by_label("Password:").click()
    page.wait_for_timeout(1000)
    page.get_by_label("Password:").fill("Blockch@in91")
    page.wait_for_timeout(1000)
    page.get_by_label("Live (temporarily disabled)").check()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(1000)
    # page.get_by_role("banner").get_by_role("link", name="Calendar").click()
    # page.wait_for_timeout(1000)
    context.storage_state(path=f"{parent_folder}/_login_tasks/saved-states/fxfactory.json")

    # ---------------------
    context.close()
    browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
