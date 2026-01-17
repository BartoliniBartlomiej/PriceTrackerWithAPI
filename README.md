# Universal Price Tracker

An automated system for monitoring product prices built with **Python**, **Selenium (Safari)**, and **SQLAlchemy**.

## Features

* **Universal Scraping:** Uses metadata (Open Graph / Schema.org) to extract prices from various online stores.
* **Database:** Tracks and stores price changes in SQLite using the SQLAlchemy ORM.
* **Automation on macOS:** Native support for the Safari browser.

## Installation & Launch

1. Clone the repository:
   `git clone https://github.com/BartoliniBartlomiej/PriceTrackerWithAPI.git`
2. Create a virtual environment:
   `python3 -m venv venv && source venv/bin/activate`
3. Install required dependencies:
   `pip install -r requirements.txt`
4. **Important:** Enable *“Allow Remote Automation”* in Safari’s Develop menu.
5. Run the application:
   `python app/main.py`

## Technologies

* Python 3.12+
* Selenium (Safari Driver)
* SQLAlchemy (SQLite)
* BeautifulSoup4
