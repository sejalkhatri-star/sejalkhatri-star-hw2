import unittest
import sys
import os

# Add the api directory to the path so we can import the converter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from index import convert_number

class TestNumericConverter(unittest.TestCase):
    
    def test_decimal_to_binary(self):
        """Test decimal to binary conversion"""
        self.assertEqual(convert_number("42", "decimal", "binary"), "101010")
        self.assertEqual(convert_number("0", "decimal", "binary"), "0")
        self.assertEqual(convert_number("255", "decimal", "binary"), "11111111")
    
    def test_decimal_to_octal(self):
        """Test decimal to octal conversion"""
        self.assertEqual(convert_number("42", "decimal", "octal"), "52")
        self.assertEqual(convert_number("0", "decimal", "octal"), "0")
        self.assertEqual(convert_number("64", "decimal", "octal"), "100")
    
    def test_decimal_to_hexadecimal(self):
        """Test decimal to hexadecimal conversion"""
        self.assertEqual(convert_number("42", "decimal", "hexadecimal"), "2a")
        self.assertEqual(convert_number("0", "decimal", "hexadecimal"), "0")
        self.assertEqual(convert_number("255", "decimal", "hexadecimal"), "ff")
    
    def test_decimal_to_base64(self):
        """Test decimal to base64 conversion (little-endian)"""
        self.assertEqual(convert_number("42", "decimal", "base64"), "KgA=")  # 42 in little-endian bytes
        self.assertEqual(convert_number("0", "decimal", "base64"), "AA==")   # 0 as single byte
        self.assertEqual(convert_number("256", "decimal", "base64"), "AAE=") # 256 in little-endian
    
    def test_decimal_to_text(self):
        """Test decimal to text conversion"""
        self.assertEqual(convert_number("42", "decimal", "text"), "forty-two")
        self.assertEqual(convert_number("0", "decimal", "text"), "zero")
        self.assertEqual(convert_number("123", "decimal", "text"), "one hundred and twenty-three")
    
    def test_binary_to_decimal(self):
        """Test binary to decimal conversion"""
        self.assertEqual(convert_number("101010", "binary", "decimal"), "42")
        self.assertEqual(convert_number("0", "binary", "decimal"), "0")
        self.assertEqual(convert_number("11111111", "binary", "decimal"), "255")
    
    def test_binary_to_octal(self):
        """Test binary to octal conversion"""
        self.assertEqual(convert_number("101010", "binary", "octal"), "52")
        self.assertEqual(convert_number("0", "binary", "octal"), "0")
    
    def test_binary_to_hexadecimal(self):
        """Test binary to hexadecimal conversion"""
        self.assertEqual(convert_number("101010", "binary", "hexadecimal"), "2a")
        self.assertEqual(convert_number("0", "binary", "hexadecimal"), "0")
    
    def test_binary_to_base64(self):
        """Test binary to base64 conversion"""
        self.assertEqual(convert_number("101010", "binary", "base64"), "KgA=")
        self.assertEqual(convert_number("0", "binary", "base64"), "AA==")
    
    def test_binary_to_text(self):
        """Test binary to text conversion"""
        self.assertEqual(convert_number("101010", "binary", "text"), "forty-two")
        self.assertEqual(convert_number("0", "binary", "text"), "zero")
    
    def test_octal_to_decimal(self):
        """Test octal to decimal conversion"""
        self.assertEqual(convert_number("52", "octal", "decimal"), "42")
        self.assertEqual(convert_number("0", "octal", "decimal"), "0")
        self.assertEqual(convert_number("100", "octal", "decimal"), "64")
    
    def test_octal_to_binary(self):
        """Test octal to binary conversion"""
        self.assertEqual(convert_number("52", "octal", "binary"), "101010")
        self.assertEqual(convert_number("0", "octal", "binary"), "0")
    
    def test_octal_to_hexadecimal(self):
        """Test octal to hexadecimal conversion"""
        self.assertEqual(convert_number("52", "octal", "hexadecimal"), "2a")
        self.assertEqual(convert_number("0", "octal", "hexadecimal"), "0")
    
    def test_octal_to_base64(self):
        """Test octal to base64 conversion"""
        self.assertEqual(convert_number("52", "octal", "base64"), "KgA=")
        self.assertEqual(convert_number("0", "octal", "base64"), "AA==")
    
    def test_octal_to_text(self):
        """Test octal to text conversion"""
        self.assertEqual(convert_number("52", "octal", "text"), "forty-two")
        self.assertEqual(convert_number("0", "octal", "text"), "zero")
    
    def test_hexadecimal_to_decimal(self):
        """Test hexadecimal to decimal conversion"""
        self.assertEqual(convert_number("2a", "hexadecimal", "decimal"), "42")
        self.assertEqual(convert_number("0", "hexadecimal", "decimal"), "0")
        self.assertEqual(convert_number("ff", "hexadecimal", "decimal"), "255")
    
    def test_hexadecimal_to_binary(self):
        """Test hexadecimal to binary conversion"""
        self.assertEqual(convert_number("2a", "hexadecimal", "binary"), "101010")
        self.assertEqual(convert_number("0", "hexadecimal", "binary"), "0")
    
    def test_hexadecimal_to_octal(self):
        """Test hexadecimal to octal conversion"""
        self.assertEqual(convert_number("2a", "hexadecimal", "octal"), "52")
        self.assertEqual(convert_number("0", "hexadecimal", "octal"), "0")
    
    def test_hexadecimal_to_base64(self):
        """Test hexadecimal to base64 conversion"""
        self.assertEqual(convert_number("2a", "hexadecimal", "base64"), "KgA=")
        self.assertEqual(convert_number("0", "hexadecimal", "base64"), "AA==")
    
    def test_hexadecimal_to_text(self):
        """Test hexadecimal to text conversion"""
        self.assertEqual(convert_number("2a", "hexadecimal", "text"), "forty-two")
        self.assertEqual(convert_number("0", "hexadecimal", "text"), "zero")
    
    def test_base64_to_decimal(self):
        """Test base64 to decimal conversion"""
        self.assertEqual(convert_number("KgA=", "base64", "decimal"), "42")
        self.assertEqual(convert_number("AA==", "base64", "decimal"), "0")
        self.assertEqual(convert_number("AAE=", "base64", "decimal"), "256")
    
    def test_base64_to_binary(self):
        """Test base64 to binary conversion"""
        self.assertEqual(convert_number("KgA=", "base64", "binary"), "101010")
        self.assertEqual(convert_number("AA==", "base64", "binary"), "0")
    
    def test_base64_to_octal(self):
        """Test base64 to octal conversion"""
        self.assertEqual(convert_number("KgA=", "base64", "octal"), "52")
        self.assertEqual(convert_number("AA==", "base64", "octal"), "0")
    
    def test_base64_to_hexadecimal(self):
        """Test base64 to hexadecimal conversion"""
        self.assertEqual(convert_number("KgA=", "base64", "hexadecimal"), "2a")
        self.assertEqual(convert_number("AA==", "base64", "hexadecimal"), "0")
    
    def test_base64_to_text(self):
        """Test base64 to text conversion"""
        self.assertEqual(convert_number("KgA=", "base64", "text"), "forty-two")
        self.assertEqual(convert_number("AA==", "base64", "text"), "zero")
    
    def test_text_to_decimal(self):
        """Test text to decimal conversion"""
        self.assertEqual(convert_number("forty two", "text", "decimal"), "42")
        self.assertEqual(convert_number("zero", "text", "decimal"), "0")
        self.assertEqual(convert_number("one hundred twenty three", "text", "decimal"), "123")
    
    def test_text_to_binary(self):
        """Test text to binary conversion"""
        self.assertEqual(convert_number("forty two", "text", "binary"), "101010")
        self.assertEqual(convert_number("zero", "text", "binary"), "0")
    
    def test_text_to_octal(self):
        """Test text to octal conversion"""
        self.assertEqual(convert_number("forty two", "text", "octal"), "52")
        self.assertEqual(convert_number("zero", "text", "octal"), "0")
    
    def test_text_to_hexadecimal(self):
        """Test text to hexadecimal conversion"""
        self.assertEqual(convert_number("forty two", "text", "hexadecimal"), "2a")
        self.assertEqual(convert_number("zero", "text", "hexadecimal"), "0")
    
    def test_text_to_base64(self):
        """Test text to base64 conversion"""
        self.assertEqual(convert_number("forty two", "text", "base64"), "KgA=")
        self.assertEqual(convert_number("zero", "text", "base64"), "AA==")
    
    def test_error_handling_invalid_decimal(self):
        """Test error handling for invalid decimal input"""
        with self.assertRaises(ValueError):
            convert_number("abc", "decimal", "binary")
        with self.assertRaises(ValueError):
            convert_number("-1", "decimal", "binary")
    
    def test_error_handling_invalid_binary(self):
        """Test error handling for invalid binary input"""
        with self.assertRaises(ValueError):
            convert_number("102", "binary", "decimal")  # Invalid binary digit
        with self.assertRaises(ValueError):
            convert_number("abc", "binary", "decimal")
    
    def test_error_handling_invalid_octal(self):
        """Test error handling for invalid octal input"""
        with self.assertRaises(ValueError):
            convert_number("89", "octal", "decimal")  # Invalid octal digit
        with self.assertRaises(ValueError):
            convert_number("abc", "octal", "decimal")
    
    def test_error_handling_invalid_hexadecimal(self):
        """Test error handling for invalid hexadecimal input"""
        with self.assertRaises(ValueError):
            convert_number("xyz", "hexadecimal", "decimal")
    
    def test_error_handling_invalid_base64(self):
        """Test error handling for invalid base64 input"""
        with self.assertRaises(ValueError):
            convert_number("invalid!", "base64", "decimal")
    
    def test_error_handling_invalid_text(self):
        """Test error handling for invalid text input"""
        with self.assertRaises(ValueError):
            convert_number("invalid text", "text", "decimal")

if __name__ == '__main__':
    unittest.main()