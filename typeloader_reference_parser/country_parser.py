#!/usr/bin/env python3
"""Created on 2023-04-11.

This script conatains functionality to extract the countries listed on
https://www.insdc.org/submitting-standards/country-qualifier-vocabulary/
and write them to a controlled text file suitable for automated parsing.

@author: Bianca Schöne
"""

import logging

from pathlib import Path
from typing import List, Tuple

import requests

from bs4 import BeautifulSoup

try:
    from __init__ import __version__
except ImportError:
    from typeloader_reference_parser.__init__ import __version__

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler())

# ===========================================================
# parameters:

COUNTRY_URL = "https://www.insdc.org/submitting-standards/country-qualifier-vocabulary/"

OUTPUT_DIR = Path(__file__).parent.parent / "data"
COUNTRY_FILE = OUTPUT_DIR / "countries.csv"


# ===========================================================
# functions:


def _get_html_content(page_url: str, timeout: int = 10) -> Tuple[bool, str]:
    """Get html page content."""
    logger.info(f"\tRequesting page {page_url}...")
    try:
        result = requests.get(page_url, timeout=timeout)
    except requests.ConnectTimeout:
        logger.info("\t\tRequest failed: timeout, page busy or server down?")
        return False, "timeout"

    if result.ok:
        raw_text = result.text
        logger.info("\t=> success!")
        return True, raw_text

    else:
        logger.info(f"\t\tRequest failed: {result.text}")
        return False, result.text


def _parse_countries_from_html_content(raw_text: str) -> List[str]:
    """Parse list of countries from html text."""
    countries = []

    logger.info("\tParsing content...")
    doc = BeautifulSoup(raw_text, "html.parser")

    tags = doc.find_all("li")
    for tag in tags:
        if not tag.attrs or "first-country" in tag.attrs["class"]:
            countries.append(tag.string)

    countries = sorted(countries)
    logger.info(f"\t=> found {len(countries)} countries")
    return countries


def _write_country_file(countries: List[str], output_csv: Path) -> None:
    """Write list of countries to output csv file."""
    logger.info(f"Writing {len(countries)} to {output_csv}...")
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv, "w", encoding="utf-8") as g:
        for country in countries:
            g.write(f"{country}\n")

    logger.info("\t=> done")


# ===========================================================
# main:


def update_countries_file(country_url: str, country_file: Path) -> bool:
    """Get countries from $country_url and write them as a list to $country_file."""
    logger.info(f"<Start country_parser V{__version__}>")

    logger.info(f"Retrieving countries from {country_url}...")
    success, raw_text = _get_html_content(country_url)
    if success:
        countries = _parse_countries_from_html_content(raw_text)
        if not countries:
            logger.info("No countries found!")
            return False

        _write_country_file(countries, country_file)

    else:
        return False

    logger.info("<End country_parser>")
    return True


if __name__ == "__main__":  # pragma: nocover
    update_countries_file(COUNTRY_URL, COUNTRY_FILE)
