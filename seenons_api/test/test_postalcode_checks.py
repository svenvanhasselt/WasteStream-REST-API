import pytest
from flask import Flask
from seenons_api.utils.postalcode_checks import check_postcode_pattern, match_postcode, is_within_postalrange, get_postcode

def test_check_postcode_pattern():
    assert check_postcode_pattern('1234AB') == True
    assert check_postcode_pattern('1234') == False
    assert check_postcode_pattern('ABCD') == False
    assert check_postcode_pattern('1234ABC') == False
    assert check_postcode_pattern('1234A') == False

def test_match_postcode():
    assert match_postcode('1234AB', '1234AB') == True
    assert match_postcode('1234AB', '1234XX') == True
    assert match_postcode('1234AB', '12XXXX') == True
    assert match_postcode('1234AB', '1234AC') == False
    assert match_postcode('1234AB', '1234') == False
    assert match_postcode('1234AB', '1234ABC') == False

def test_is_within_postalrange():
    assert is_within_postalrange('1234', '1234-5678') == True
    assert is_within_postalrange('1000', '1234-5678') == False
    assert is_within_postalrange('6000', '1534-5678') == False

def test_get_postcode():
    app = Flask(__name__)
    with app.test_request_context('/?postalcode=1234AB'):
        assert get_postcode() == '1234'
    with app.test_request_context('/?postalcode=invalid'):
        with pytest.raises(ValueError) as e:
            get_postcode()
        assert str(e.value) == 'Invalid postal code provided'
    with app.test_request_context('/'):
        with pytest.raises(ValueError) as e:
            get_postcode()
        assert str(e.value) == 'No postal code provided'
