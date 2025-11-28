"""Tests for FIX message parser."""

import unittest
from fix_parser import FixParser


def test_parse_valid_message():
    """Test parsing a valid FIX message."""
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
    result = parser.parse(msg)
    
    assert result['55'] == 'AAPL'
    assert result['54'] == '1'
    assert result['38'] == '100'


def test_parse_missing_symbol():
    """Test that missing symbol raises ValueError."""
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|54=1|38=100|40=2|10=128"
    
    try:
        parser.parse(msg)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'Symbol' in str(e)


def test_parse_missing_side():
    """Test that missing side raises ValueError."""
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|55=AAPL|38=100|40=2|10=128"
    
    try:
        parser.parse(msg)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'Side' in str(e)


def test_parse_missing_quantity():
    """Test that missing quantity raises ValueError."""
    parser = FixParser()
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|40=2|10=128"
    
    try:
        parser.parse(msg)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'OrderQty' in str(e)


if __name__ == '__main__':
    test_parse_valid_message()
    test_parse_missing_symbol()
    test_parse_missing_side()
    test_parse_missing_quantity()
    print("All FIX parser tests passed!")

