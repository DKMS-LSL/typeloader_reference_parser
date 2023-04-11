"""Tests for `typeloader_reference_parser` package."""

import pytest

from typeloader_reference_parser import typeloader_reference_parser_main


@pytest.mark.parametrize("exp", [(True)])
def test_typeloader_reference_parser(exp):
    result = typeloader_reference_parser_main.main()
    assert result == exp
