import logging
from playwright.sync_api import sync_playwright
from config import (
    playright_cookies,
    playright_login_url,
    playright_homepage_url,
    login_email,
    login_password,
)
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def initialize_browser(p):
    """Initialize the browser and context."""
    logging.info("Initializing browser and context.")
    browser = p.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context()
    context.add_cookies(playright_cookies)
    return browser, context


def perform_login(page):
    """Perform the login operation."""
    logging.info("Performing login operation.")
    page.goto(playright_login_url)
    page.click("text=Anmelden")
    page.locator("text=Anmelden/Registrieren").nth(1).click()
    page.fill("#benutzername-input", login_email)
    page.fill("#passwort-input", login_password)
    page.click("text=Anmelden")


def capture_request_data(page):
    """Capture the request data during login."""
    logging.info("Capturing request data during login.")

    login_data = {}

    def handle_request(request):
        if "openid-connect/token" in request.url and request.method == "POST":
            login_data["request_headers"] = request.all_headers()
            login_data["request_body"] = request.post_data_json

    def handle_response(response):
        if "openid-connect/token" in response.url and response.request.method == "POST":
            login_data["response_body"] = response.json() if response.ok else None

    page.on("request", handle_request)
    page.on("response", handle_response)

    perform_login(page)

    # Wait for navigation to complete after login
    page.wait_for_load_state("networkidle")

    return login_data


def get_request_data():
    logging.info("Starting to get request data.")
    with sync_playwright() as p:
        browser, context = initialize_browser(p)
        try:
            page = context.new_page()
            login_data = capture_request_data(page)

            logging.info("Visiting homepage.")
            page.goto(playright_homepage_url)
            homepage_data = {"cookies": page.context.cookies()}
        finally:
            browser.close()
            logging.info("Browser closed.")
    return homepage_data, login_data


homepage_data, login_data = get_request_data()

logging.info(f"Homepage data: {homepage_data}")
logging.info(f"Login data: {login_data}")

with open("data.json", "w") as f:
    json.dump({"homepage_data": homepage_data, "login_data": login_data}, f)

logging.info("Data captured successfully.")
