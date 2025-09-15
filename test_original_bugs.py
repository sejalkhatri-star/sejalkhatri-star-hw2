import unittest
import sys
import os

# Add the api directory to the path so we can import the converter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

class TestOriginalBugs(unittest.TestCase):
    """
    Test cases that would have detected the original bugs in the implementation.
    These tests demonstrate the bugs that existed before fixes were applied.
    """
    
    def test_base64_zero_conversion_bug(self):
        """
        Original Bug: Converting 0 to base64 would crash with ValueError
        because 0.bit_length() returns 0, leading to 0.to_bytes(0, ...) which is invalid.
        """
        # Import here to test the current (fixed) implementation
        from index import convert_number
        
        # This should work now (after fix)
        result = convert_number("0", "decimal", "base64")
        self.assertEqual(result, "AA==")
        
        # Test that zero conversion works from all input formats
        self.assertEqual(convert_number("0", "binary", "base64"), "AA==")
        self.assertEqual(convert_number("0", "octal", "base64"), "AA==")
        self.assertEqual(convert_number("0", "hexadecimal", "base64"), "AA==")
        self.assertEqual(convert_number("zero", "text", "base64"), "AA==")
    
    def test_base64_endianness_bug(self):
        """
        Original Bug: Base64 conversion used big-endian byte order instead of little-endian.
        Requirements specify little-endian (default for Windows/Mac).
        """
        from index import convert_number
        
        # Test that we get little-endian results
        # 42 in little-endian bytes should be [42, 0] -> base64 "KgA="
        # 42 in big-endian bytes would be [0, 42] -> base64 "ACo="
        result = convert_number("42", "decimal", "base64")
        self.assertEqual(result, "KgA=")  # Little-endian (correct)
        self.assertNotEqual(result, "ACo=")  # Big-endian (incorrect)
        
        # Test with a larger number to make endianness more obvious
        # 256 = 0x0100, little-endian: [0, 1], big-endian: [1, 0]
        result = convert_number("256", "decimal", "base64")
        self.assertEqual(result, "AAE=")  # Little-endian [0, 1]
        self.assertNotEqual(result, "AQA=")  # Big-endian [1, 0]
    
    def test_limited_text_recognition_bug(self):
        """
        Original Bug: Text conversion only handled very basic numbers (1-10, zero, nil).
        This severely limited the converter's usefulness.
        """
        from index import convert_number
        
        # These should work now (after fix)
        self.assertEqual(convert_number("twenty", "text", "decimal"), "20")
        self.assertEqual(convert_number("thirty", "text", "decimal"), "30")
        self.assertEqual(convert_number("forty", "text", "decimal"), "40")
        self.assertEqual(convert_number("fifty", "text", "decimal"), "50")
        
        # Compound numbers should also work
        self.assertEqual(convert_number("twenty one", "text", "decimal"), "21")
        self.assertEqual(convert_number("forty two", "text", "decimal"), "42")
        self.assertEqual(convert_number("ninety nine", "text", "decimal"), "99")
        
        # Larger numbers
        self.assertEqual(convert_number("one hundred", "text", "decimal"), "100")
        self.assertEqual(convert_number("one hundred twenty three", "text", "decimal"), "123")

if __name__ == '__main__':
    unittest.main()