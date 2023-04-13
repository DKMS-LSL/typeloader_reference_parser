"""Tests for `country_parser.py` file."""
import itertools

from pathlib import Path

import pytest

from typeloader_reference_parser import country_parser

BAD_URL = "https://raw.githubusercontent.com/DKMS-LSL/typeloader/1"
DATA_DIR = Path(__file__).parent / "data"


def test_get_html_content_happy():
    test_url = (
        "https://raw.githubusercontent.com/DKMS-LSL/typeloader/master/typeloader2/__init__.py"
    )
    success, content = country_parser._get_html_content(test_url)
    assert success
    assert '__status__ = "productive"' in content


def test_get_html_content__sad__bad_url():
    success, content = country_parser._get_html_content(BAD_URL)
    assert not success
    assert content == "400: Invalid request"


def test_get_html_content__sad__timeout():
    test_url = (
        "https://raw.githubusercontent.com/DKMS-LSL/typeloader/master/typeloader2/__init__.py"
    )
    success, content = country_parser._get_html_content(test_url, timeout=0.00001)
    assert not success
    assert content == "timeout"


# ---


def test_parse_countries_from_html():
    raw_text = """<!DOCTYPE html>
<html lang="en-US">

<head>
    <title>International Nucleotide Sequence Database Collaboration</title>
</head>

<body class="page-template-default">
<p>COUNTRY LIST</p>
<ul>
<li class="first-country">Afghanistan</li>
<li>Albania</li>
</ul>
<h2>Historical Country Names</h2>
<ul>
<li>Zaire</li>
</ul>
</body>
</html>
    """
    countries = country_parser._parse_countries_from_html_content(raw_text)
    assert countries == ["Afghanistan", "Albania", "Zaire"]


def test_write_country_file():
    countries = ["Afghanistan", "Albania", "Zaire"]
    output_file = DATA_DIR / "temp.csv"
    country_parser._write_country_file(countries, output_file)

    with open(DATA_DIR / "ref.txt") as f_ref, open(output_file) as f_new:
        for l_ref, l_new in itertools.zip_longest(f_ref, f_new):
            assert l_new == l_ref

    output_file.unlink()


@pytest.mark.parametrize(
    ["url", "success_exp"],
    [
        (country_parser.COUNTRY_URL, True),
        (BAD_URL, False),
        (
            "https://raw.githubusercontent.com/DKMS-LSL/typeloader/master/typeloader2/__init__.py",
            False,
        ),
    ],
)
def test_main(url, success_exp):
    output_file = DATA_DIR / "temp.csv"
    success = country_parser.update_countries_file(url, output_file)
    assert success == success_exp
    output_file.unlink(missing_ok=True)
