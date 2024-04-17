from playwright.sync_api import Playwright, sync_playwright
from loginhelpers import *


def run(playwright: Playwright) -> None:
    for i in range(1, 5):
        config_data = load_info(user=f'VIETSTOCK_{i}')
        print(config_data['username'])
        print(config_data['password'])
        to = rand_timeout(15, 25)
        browser = playwright.chromium.launch(headless=False)
        # browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.wait_for_timeout(to)
        page.goto("https://finance.vietstock.vn")
        page.wait_for_timeout(rand_timeout(55, 89))
        page.get_by_role("button", name="Đăng nhập").click()
        page.wait_for_timeout(to)
        page.get_by_role("textbox", name="Email").fill(config_data['username'])
        page.wait_for_timeout(to)
        page.get_by_role("textbox", name="Mật khẩu").fill(config_data['password'])
        page.wait_for_timeout(to)
        page.locator("#Remember").check()
        page.wait_for_timeout(to)
        with page.expect_navigation():
            page.get_by_role("button", name="Đăng nhập ").click()
        page.wait_for_timeout(to)
        page.locator(".col-xs-24 > .hidden-xs > a").click()
        page.wait_for_timeout(to)
        context.storage_state(path=f"{parent_folder}/saved-states/vietstock_{i}.json")
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
