# Job Data Scraper

This project is a job data scraper that extracts job applicant details from the German Federal Employment Agency's website. The data is fetched, parsed, and saved in both JSON and Excel formats.

## Table of Contents

- Prerequisites
- Installation
- Configuration
- Usage
- Logging
- Contributing
- License

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Chrome browser

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/faisal-fida/job-data-scraper.git
    cd job-data-scraper
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Update the 

config.py

 file with your login credentials and other necessary configurations:

```python
login_email = "your_email@example.com"
login_password = "your_password"
playwright_login_url = "https://web.arbeitsagentur.de/profil/profil-ui/pd/"
playright_homepage_url = "https://www.arbeitsagentur.de/"

playwright_cookies = [
    {
        "name": "cookie_consent",
        "value": "accepted",
        "domain": ".arbeitsagentur.de",
        "path": "/",
    },
    {
        "name": "personalization_consent",
        "value": "accepted",
        "domain": ".arbeitsagentur.de",
        "path": "/",
    },
    {
        "name": "marketing_consent",
        "value": "accepted",
        "domain": ".arbeitsagentur.de",
        "path": "/",
    },
]

initial_url = "https://rest.arbeitsagentur.de/jobboerse/bewerbersuche-service/pc/v1/bewerber?angebotsart=1&veroeffentlichtseit=7&erreichbarkeit=E-Mail&page={}&size=25&facetten=veroeffentlichtseit,arbeitszeit,erreichbarkeit"

url_cookies = {
    "cookie_consent": "accepted",
    "personalization_consent": "accepted",
    "marketing_consent": "accepted",
}
url_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Origin": "https://www.arbeitsagentur.de",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "X-API-Key": "jobboerse-bewerbersuche-ui",
    "correlation-id": "84bd5b61-77e0-45cc-9583-a977b697bef8",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
```

## Usage

1. Fetch URLs and extract data:

    ```sh
    python app.py
    ```

2. The extracted data will be saved in the 

output

 directory as [`data.json`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2FFaisal%2FVideos%2FScraping%2Fapp.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A81%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FFaisal%2FVideos%2FScraping%2Furl_fetcher.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A49%2C%22character%22%3A4%7D%7D%5D%2C%228d9c31d0-373c-4bcf-a8dc-56852e9e4a36%22%5D "Go to definition") and `parsed_data.xlsx`.

## Logging

The application logs its activities, which can be helpful for debugging and monitoring. The logs are printed to the console.