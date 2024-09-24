import logging
import json
from typing import List, Dict, Any
from playwright.sync_api import (
    sync_playwright,
    Page,
    Browser,
    BrowserContext,
    TimeoutError,
)
from config import (
    playwright_cookies,
    login_email,
    login_password,
)
from url_fetcher import fetch_urls
from data_parser import extract_and_save_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def initialize_browser(playwright) -> tuple[Browser, BrowserContext]:
    browser = playwright.chromium.launch(
        headless=False, channel="chrome", args=["--start-maximized"]
    )
    context = browser.new_context()
    context.add_cookies(playwright_cookies)
    return browser, context


def login_required(page: Page) -> bool:
    page.wait_for_load_state("networkidle")

    try:
        page.wait_for_selector("button:has-text('Anmelden')", timeout=2000)
    except TimeoutError:
        logger.warning("Login not required.")
        return False
    login_button = page.locator("button:has-text('Anmelden')")
    if login_button.is_visible():
        logger.info("Login button found. Clicking to proceed.")
        login_button.scroll_into_view_if_needed()
        login_button.click()
        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_selector("text=Anmelden/Registrieren", timeout=6000)
            register_button = page.locator("text=Anmelden/Registrieren").nth(1)
            if register_button.is_visible():
                logger.info("Login required.")
                register_button.click()
                return True
        except TimeoutError:
            logger.warning("Login not required.")
            return False
    else:
        logger.warning("Login not required.")
        return False


def perform_login(page: Page) -> None:
    logger.info("Performing login.")
    page.wait_for_load_state("networkidle")
    page.fill("#benutzername-input", login_email)
    page.fill("#passwort-input", login_password)
    page.click("text=Anmelden")
    page.wait_for_load_state("networkidle")


def process_url(page: Page, url: str) -> Dict[str, Any]:
    if login_required(page):
        perform_login(page)
    return


def capture_request_data(page: Page, url: str) -> Dict[str, Any]:
    url_id = url.split("/")[-1]
    logger.info(f"Processing URL ID: {url_id}")
    data = {
        "personal_details": None,
        "general_details": None,
        "response_text": [],
        "id": url_id,
    }
    max_retries = 5
    retries = 0

    def handle_response(response):
        nonlocal retries
        if response.request.method == "GET" and any(
            endpoint in response.url
            for endpoint in ["/pc/v1/bewerberdetails/", "/pd/v1/kontaktdaten/"]
        ):
            try:
                json_response = response.json()
                if json_response.get("anrede") and data["personal_details"] is None:
                    logger.info("Personal details found")
                    data["personal_details"] = json_response
                elif json_response.get("refnr") and data["general_details"] is None:
                    logger.info("General details found")
                    data["general_details"] = json_response
            except json.JSONDecodeError:
                logger.warning(f"Non-JSON response received from {response.url}")
                data["response_text"].append(response.text())

    while retries < max_retries and (
        data["personal_details"] is None or data["general_details"] is None
    ):
        if retries > 0:
            logger.info(f"Retrying request {retries}/{max_retries}")
            page.wait_for_timeout(5000)
        if retries > 1:
            page.wait_for_timeout(10000)

        page.on("response", handle_response)
        page.goto(url)
        if login_required(page):
            perform_login(page)
        page.wait_for_load_state("networkidle")
        page.remove_listener("response", handle_response)
        retries += 1
        if data["personal_details"] is None:
            logger.info("Personal details not found, retrying.")
        if data["general_details"] is None:
            logger.info("General details not found, retrying.")

    return data


def get_request_data(urls: List[str]) -> List[Dict[str, Any]]:
    logger.info(f"Starting data collection for {len(urls)} URLs.")
    data_list = []

    with sync_playwright() as p:
        browser, context = initialize_browser(p)
        try:
            page = context.new_page()
            for url in urls:
                data = capture_request_data(page, url)
                data_list.append(data)
                logger.info(f"Number of URLs processed: {len(data_list)}")
        finally:
            browser.close()
            logger.info("Browser closed.")

    return data_list


if __name__ == "__main__":
    urls = fetch_urls("input/refrence_numbers.txt")
    collected_data = get_request_data(urls)
    extract_and_save_data(collected_data, "output/data.json", "output/parsed_data.xlsx")
