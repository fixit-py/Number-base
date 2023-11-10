import pytest
from baseconverteroop import Numberbase

@pytest.fixture
def nb():
    return Numberbase()

def test_decimal_to_base(nb):
    assert nb.decimal_to_base(-346.7, 36) == "-9M.P777777761"
    assert nb.decimal_to_base(-3466.9, 5) == "-102331.4222222222"
    assert nb.decimal_to_base(-836126, 15) == "-117B1B"
    assert nb.decimal_to_base(836126, 16) == "CC21E"
    assert nb.decimal_to_base(1.9789298498448, 14) == "1.D9C27D78DC"

def test_check(nb):
    with pytest.raises(ValueError, match="Invalid digit in the input"):
        nb.check("12345", 5)
    with pytest.raises(ValueError, match="Invalid digit in the input"):
        nb.check("1ABC", 10)
    nb.check("12345", 10)

def test_base_to_decimal(nb):
    assert nb.base_to_decimal("1101.001", 2) == 13.125
    assert nb.base_to_decimal("1A.2", 16) == 26.125
    assert nb.base_to_decimal("12345", 6) == 1865.0

def test_convert_base_to_base(nb):
    assert nb.convert_base_to_base("1101.001", 2, 16) == "D.2"
    assert nb.convert_base_to_base("1A.2", 16, 2) == "11010.001"
    assert nb.convert_base_to_base("12345", 6, 8) == "3511"

def test_perform_arithmetic_operation(nb):
    assert nb.perform_arithmetric_operation("101", "10", "+", 2) == "111"
    assert nb.perform_arithmetric_operation("1A", "2", "*", 16) == "34"
    assert nb.perform_arithmetric_operation("1101", "10", "/", 2) == "110.1"
    with pytest.raises(ValueError, match="Invalid Operation"):
        nb.perform_arithmetric_operation("123", "456", "&", 10)

def test_radixcomplement(nb):
    assert nb.radixcomplement("ABC", 16) == "544"
    assert nb.radixcomplement("10101", 2) == "1011"
    assert nb.radixcomplement("12345", 8) == "65433"

def test_diminishedradixcomplement(nb):
    assert nb.diminishedradixcomplement("ABC", 16) == "543"
    assert nb.diminishedradixcomplement("10101", 2) == "1010"
    assert nb.diminishedradixcomplement("12345", 8) == "65432"
    
if __name__ == "__main__":
    pytest.main()
