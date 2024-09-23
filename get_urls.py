import requests

from config import url_cookies, url_headers, initial_url


def request_urls(page_number: int, refrence_numbers: list):
    updated_url = initial_url.format(page_number)
    response = requests.get(updated_url, cookies=url_cookies, headers=url_headers)
    data = response.json()
    refrence_numbers.extend([item["refnr"] for item in data["bewerber"]])


def build_url(refrence_number):
    return (
        f"https://www.arbeitsagentur.de/bewerberboerse/bewerberdetail/{refrence_number}"
    )


def get_urls():
    refrence_numbers = []

    for page_number in range(1, 11):
        request_urls(page_number, refrence_numbers)

    urls = [build_url(refrence_number) for refrence_number in refrence_numbers]
    return urls


# urls = get_urls()


# print(urls)

# print(f"Total urls: {len(urls)}")
