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

5. Download the Playwright browser driver:

    ```sh
    python -m playwright install chrome
    ```

## Configuration

Copy the config.py file to the same directory as app.py and url_fetcher.py.


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