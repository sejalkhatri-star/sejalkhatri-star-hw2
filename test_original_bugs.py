"""
Regression tests that demonstrate the original bugs in the implementation.
These tests show what would have failed with the original code.
"""
import pytest
import base64
from api.index import number_to_base64, base64_to_number

def test_original_zero_bug_simulation():
    """
    This test simulates the original bug with zero conversion.
    The original implementation would fail because:
    - number.bit_length() for 0 returns 0
    - (0 + 7) // 8 = 0 
    - 0.to_bytes(0, byteorder='big') raises ValueError
    """
    # This should work now with the fix
    result = number_to_base64(0)
    assert result is not None
    
    # Test roundtrip
    recovered = base64_to_number(result)
    assert recovered == 0

def test_original_endianness_bug_simulation():
    """
    This test demonstrates the original endianness bug.
    The original implementation used big-endian but requirements specify little-endian.
    """
    # Test with 256 (0x0100)
    # Little-endian: [0x00, 0x01] -> "AAE="
    # Big-endian: [0x01, 0x00] -> "AQA="
    
    result = number_to_base64(256)
    
    # What little-endian should produce
    little_endian_bytes = (256).to_bytes(2, byteorder='little')
    expected_b64 = base64.b64encode(little_endian_bytes).decode('utf-8')
    
    # The fixed implementation should match little-endian
    assert result == expected_b64
    
    # Verify roundtrip works
    recovered = base64_to_number(result)
    assert recovered == 256

def test_original_text_limitation_bug():
    """
    This test demonstrates the original limitation in text conversion.
    The original implementation only handled numbers 1-10, zero, nil.
    """
    from api.index import text_to_number
    
    # These should work now with the improved implementation
    assert text_to_number("eleven") == 11
    assert text_to_number("twenty") == 20
    assert text_to_number("twenty one") == 21

if __name__ == "__main__":
    pytest.main([__file__, "-v"])