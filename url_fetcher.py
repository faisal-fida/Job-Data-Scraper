import os
import logging
from typing import List
from config import initial_url, url_cookies, url_headers

import requests

logger = logging.getLogger(__name__)


def build_url(refrence_number):
    return (
        f"https://www.arbeitsagentur.de/bewerberboerse/bewerberdetail/{refrence_number}"
    )


def fetch_urls(file_path: str):
    refrence_numbers = []
    logger.info("Starting to get URLs")

    if os.path.exists(file_path):
        logger.info("Reference numbers file is already present. Reading from it.")
        with open(file_path, "r") as file:
            refrence_numbers = [line.strip() for line in file]

        if not refrence_numbers or len(refrence_numbers) < 100:
            logger.info(
                "No reference numbers found or less than 100. Fetching new ones."
            )
            refrence_numbers = fetch_new_references()
            save_references(file_path, refrence_numbers)
    else:
        refrence_numbers = fetch_new_references()
        save_references(file_path, refrence_numbers)

    urls = [build_url(refrence_number) for refrence_number in refrence_numbers]
    logger.info(f"Retrieved {len(urls)} URLs")
    return urls


def fetch_new_references():
    refrence_numbers = []
    for page_number in range(1, 11):
        request_urls(page_number, refrence_numbers)
    return refrence_numbers


def request_urls(page_number: int, refrence_numbers: list):
    updated_url = initial_url.format(page_number)
    response = requests.get(updated_url, cookies=url_cookies, headers=url_headers)
    data = response.json()
    new_references = [item["refnr"] for item in data["bewerber"]]
    refrence_numbers.extend(new_references)
    logging.info(
        f"Retrieved {len(new_references)} reference numbers from page {page_number}"
    )


def save_references(file_path: str, refrence_numbers: List[str]):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        for refrence_number in refrence_numbers:
            file.write(f"{refrence_number}\n")
    logger.info(f"Saved {len(refrence_numbers)} reference numbers to {file_path}")
