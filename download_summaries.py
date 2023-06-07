"""
This script downloads a web page using BeautifulSoup and saves it to a file.
It utilizes Selenium WebDriver with Chrome to retrieve the web page content.

Usage:
python script_name.py --url <web_page_url> --out-file <output_file_path>

Required Arguments:
--url           URL of the web page to download
--out-file      Path of the output file to save the downloaded content

Example:
python script_name.py --url https://example.com --out-file output.json
"""
import argparse
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def init_chrome_driver():
    """Initialize and return a Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    return webdriver.Chrome(options=chrome_options)


def download_url(url, chrome_driver):
    """Download the web page content using the provided Chrome WebDriver instance."""
    chrome_driver.get(url)

    wait = WebDriverWait(chrome_driver, 10)
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".session-block__title")))


def extract_session_summaries(html):
    """Extract session summaries from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    div_elements = soup.select('.session-block__content-row__block--description')
    summaries = []

    if div_elements:
        for div_element in div_elements:
            span_element = div_element.select_one('span')
            if span_element:
                span_text = span_element.get_text(strip=True)
                summaries.append(span_text)

    print(f"Found {len(summaries)} summaries.")
    return summaries


def main(url, out_file, chrome_driver):
    """Main function to download a web page using BeautifulSoup and save it to a file."""
    download_url(url, chrome_driver)
    summaries = extract_session_summaries(chrome_driver.page_source)

    with open(out_file, "w", encoding="utf-8") as file:
        json.dump(summaries, file)

    print(f"Web page downloaded and summaries saved to {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a web page using BeautifulSoup and save it to a file")
    parser.add_argument("--url", required=True, help="URL of the web page to download")
    parser.add_argument("--out-file", required=True, help="Path of the output file")

    args = parser.parse_args()
    driver = init_chrome_driver()

    main(args.url, args.out_file, driver)

    driver.quit()
