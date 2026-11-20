# County Record Browser Automation POC

An isolated browser automation and web scraping demonstration. It opens a public website, searches its available tags, extracts matching quotes into structured records, and prints them in the terminal.

This is only a demonstration of the browser automation component. It is not the complete client automation system and does not include county integrations, UiPath, Digital Dell, order processing, CAPTCHA handling, OCR, PDF processing, APIs, or databases.

## Technologies

- Python 3.9+
- Playwright
- Quotes to Scrape, a public website made for scraping practice

## Installation

From the project directory, create and activate a virtual environment, then install the dependency and browser:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run

Search the default `humor` tag. The browser window is visible by default:

```powershell
python main.py
```

Search another tag shown in the site's Top Ten tags (for example `life`):

```powershell
python main.py --tag life
```

To run without displaying the browser window:

```powershell
python main.py --headless
```

## Example terminal output

The matching quote text and authors are retrieved from the site at runtime, so the exact records may differ. The JSON below is shortened to one record for readability.

```text
Starting Browser Automation POC...
Launching browser...
Opening website...
Performing search for tag 'humor'...
Extracting records...
Search completed successfully.
Records found: 10
[
  {
    "quote": "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.",
    "author": "Jane Austen",
    "tags": ["aliteracy", "books", "classic", "humor"]
  },
  ... 9 more records
]
---
Automation completed successfully.
```

## Limitations

- Demonstrates one site's tag search and extracts the results on that result page only.
- Requires an internet connection and an installed Playwright Chromium browser.
- Website layout and availability may change; this is not intended for production use.
- Does not bypass authentication, CAPTCHA, access restrictions, or other website security controls.
- Contains no integrations or workflow features from the larger client system.
