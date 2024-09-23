import logging
import json
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from config import (
    playwright_cookies,
    playwright_login_url,
    login_email,
    login_password,
)
from get_urls import get_urls

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def initialize_browser(playwright) -> tuple[Browser, BrowserContext]:
    """Initialize the browser and context."""
    logger.info("Initializing browser and context.")
    browser = playwright.chromium.launch(headless=True, channel="chrome")
    context = browser.new_context(storage_state="state.json")
    context.add_cookies(playwright_cookies)
    return browser, context


def perform_login(page: Page) -> None:
    """Perform the login operation."""
    logger.info("Performing login.")
    page.locator("text=Anmelden/Registrieren").nth(1).click()
    page.fill("#benutzername-input", login_email)
    page.fill("#passwort-input", login_password)
    page.click("text=Anmelden")
    page.wait_for_load_state("networkidle")


def capture_request_data(page: Page, url: str) -> Dict[str, Any]:
    """Capture the request data during page navigation."""
    logger.info(f"Capturing request data for URL: {url}")

    data = {"personal_details": None, "general_details": None, "response_text": []}

    def handle_response(response):
        if response.request.method == "GET" and any(
            endpoint in response.url
            for endpoint in ["/pc/v1/bewerberdetails/", "/pd/v1/kontaktdaten/"]
        ):
            logger.info(f"Processing response from URL: {response.url}")
            try:
                json_response = response.json()
                if json_response.get("anrede"):
                    logger.info("Personal details found")
                    data["personal_details"] = json_response
                elif json_response.get("refnr"):
                    logger.info("General details found")
                    data["general_details"] = json_response
            except json.JSONDecodeError:
                logger.warning(f"Non-JSON response received from {response.url}")
                data["response_text"].append(response.text())

    page.on("response", handle_response)
    page.goto(url)
    page.wait_for_load_state("networkidle")

    return data


def process_url(page: Page, url: str) -> Dict[str, Any]:
    """Process a single URL, handling login if necessary."""
    logger.info(f"Processing URL: {url}")
    page.goto(url)
    page.wait_for_load_state("networkidle")

    if page.locator("button:has-text('Anmelden')").is_visible():
        logger.info("Login required. Initiating login process.")
        page.locator("button:has-text('Anmelden')").click()
        page.wait_for_load_state("networkidle")
        if "sso.arbeitsagentur.de/auth" in page.url:
            perform_login(page)
            page.context.storage_state(path="state.json")
        else:
            logger.warning("Unexpected login page encountered.")

    return capture_request_data(page, url)


def get_request_data(urls: List[str]) -> List[Dict[str, Any]]:
    """Main function to get request data for multiple URLs."""
    logger.info(f"Starting data collection for {len(urls)} URLs.")
    data_list = []

    with sync_playwright() as p:
        browser, context = initialize_browser(p)
        try:
            page = context.new_page()
            for url in urls:
                data = process_url(page, url)
                data_list.append({url: data})
        finally:
            browser.close()
            logger.info("Browser closed.")

    return data_list


def save_data(data: List[Dict[str, Any]], filename: str = "data.json") -> None:
    """Save the collected data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Data saved in {filename}.")


if __name__ == "__main__":
    # urls = get_urls()  # Uncomment this line to use the actual URL fetching function
    urls = [
        "https://www.arbeitsagentur.de/bewerberboerse/bewerberdetail/10000-1200186703-B",
        "https://www.arbeitsagentur.de/bewerberboerse/bewerberdetail/10000-1200186273-B",
    ]
    collected_data = get_request_data(urls)
    save_data(collected_data)
