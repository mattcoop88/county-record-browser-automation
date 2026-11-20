import argparse
import json
import logging
import sys

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


HOME_URL = "https://quotes.toscrape.com/"
TIMEOUT_MS = 15_000

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


class AutomationError(Exception):
    """An expected failure while searching or extracting website data."""


def extract_quotes(page):
    quote_cards = page.locator(".quote")
    quotes = []

    for index in range(quote_cards.count()):
        card = quote_cards.nth(index)
        text = card.locator(".text").inner_text().strip()
        author = card.locator(".author").inner_text().strip()
        tags = card.locator(".tags a.tag").all_inner_texts()

        if not text or not author:
            raise AutomationError(f"Quote record {index + 1} is missing required data.")

        quotes.append(
            {
                "quote": text,
                "author": author,
                "tags": [tag.strip() for tag in tags],
            }
        )

    return quotes


def search_quotes(tag, headless):
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            try:
                page = browser.new_page()
                page.set_default_timeout(TIMEOUT_MS)

                logger.info("Opening website...")
                response = page.goto(HOME_URL, wait_until="domcontentloaded")
                if response is not None and response.status >= 400:
                    raise AutomationError(
                        f"The website returned HTTP {response.status}."
                    )

                logger.info("Performing search for tag '%s'...", tag)
                tag_link = page.locator("div.tags-box a.tag").filter(has_text=tag)
                matching_links = [
                    tag_link.nth(index)
                    for index in range(tag_link.count())
                    if tag_link.nth(index).inner_text().strip().casefold()
                    == tag.casefold()
                ]
                if not matching_links:
                    raise AutomationError(
                        f"Search tag '{tag}' was not found in the website's top tags."
                    )
                matching_links[0].click()

                logger.info("Extracting records...")
                return extract_quotes(page)
            finally:
                browser.close()
    except PlaywrightTimeoutError as error:
        raise AutomationError(
            f"The page or a search element did not respond within {TIMEOUT_MS // 1000} seconds."
        ) from error
    except PlaywrightError as error:
        raise AutomationError(f"Browser automation failed: {error}") from error


def main():
    parser = argparse.ArgumentParser(
        description="Search Quotes to Scrape for quotes with a selected tag."
    )
    parser.add_argument(
        "--tag",
        default="humor",
        help="tag to search (default: humor; choose one of the site's top tags)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="run the browser without displaying its window",
    )
    args = parser.parse_args()

    logger.info("Starting Browser Automation POC...")
    logger.info("Launching browser...")

    try:
        quotes = search_quotes(args.tag.strip(), args.headless)
    except (AutomationError, PlaywrightError) as error:
        logger.error("Automation failed: %s", error)
        return 1

    logger.info("Search completed successfully.")
    logger.info("Records found: %d", len(quotes))
    if quotes:
        print(json.dumps(quotes, indent=2, ensure_ascii=False))
    else:
        logger.info("No records matched the selected tag.")

    logger.info("---")
    logger.info("Automation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
