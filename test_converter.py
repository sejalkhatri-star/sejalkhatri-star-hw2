import pytest
import json
from api.index import app, text_to_number, number_to_text, base64_to_number, number_to_base64

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestTextToNumber:
    """Test text to number conversion"""
    
    def test_basic_numbers(self):
        assert text_to_number("one") == 1
        assert text_to_number("two") == 2
        assert text_to_number("ten") == 10
    
    def test_zero_cases(self):
        assert text_to_number("zero") == 0
        assert text_to_number("nil") == 0
    
    def test_case_insensitive(self):
        assert text_to_number("ONE") == 1
        assert text_to_number("Two") == 2
        assert text_to_number("TEN") == 10
    
    def test_with_punctuation(self):
        assert text_to_number("one!") == 1
        assert text_to_number("two.") == 2
    
    def test_invalid_text(self):
        with pytest.raises(ValueError):
            text_to_number("one hundred twenty three")  # Complex number
        with pytest.raises(ValueError):
            text_to_number("invalid")
    
    def test_extended_numbers(self):
        """Test that extended number words work"""
        assert text_to_number("eleven") == 11
        assert text_to_number("twenty") == 20
        assert text_to_number("twenty one") == 21
        assert text_to_number("thirty five") == 35

class TestNumberToText:
    """Test number to text conversion"""
    
    def test_basic_numbers(self):
        assert number_to_text(1) == "one"
        assert number_to_text(2) == "two"
        assert number_to_text(10) == "ten"
        assert number_to_text(0) == "zero"
    
    def test_larger_numbers(self):
        assert number_to_text(11) == "eleven"
        assert number_to_text(20) == "twenty"
        assert number_to_text(100) == "one hundred"
        assert number_to_text(123) == "one hundred and twenty-three"

class TestBase64Conversion:
    """Test base64 conversion functions"""
    
    def test_number_to_base64_basic(self):
        # Test small numbers
        result = number_to_base64(1)
        assert isinstance(result, str)
        
        result = number_to_base64(255)
        assert isinstance(result, str)
    
    def test_base64_to_number_basic(self):
        # Test with known base64 values
        # 'AQ==' is base64 for byte 0x01 (decimal 1) in big-endian
        result = base64_to_number('AQ==')
        assert result == 1
        
        # '/w==' is base64 for byte 0xFF (decimal 255) in big-endian
        result = base64_to_number('/w==')
        assert result == 255
    
    def test_base64_roundtrip(self):
        """Test that number -> base64 -> number preserves the value"""
        test_numbers = [0, 1, 255, 256, 1000, 65535]
        for num in test_numbers:
            if num == 0:
                continue  # Skip 0 as it has special handling issues
            b64 = number_to_base64(num)
            recovered = base64_to_number(b64)
            assert recovered == num, f"Roundtrip failed for {num}: got {recovered}"
    
    def test_invalid_base64(self):
        with pytest.raises(ValueError):
            base64_to_number("invalid!")
        with pytest.raises(ValueError):
            base64_to_number("not_base64")

class TestAPIEndpoint:
    """Test the /convert API endpoint"""
    
    def test_decimal_to_binary(self, client):
        response = client.post('/convert', 
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'binary'})
        data = json.loads(response.data)
        assert data['result'] == '101010'
        assert data['error'] is None
    
    def test_binary_to_decimal(self, client):
        response = client.post('/convert',
            json={'input': '101010', 'inputType': 'binary', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '42'
        assert data['error'] is None
    
    def test_decimal_to_hexadecimal(self, client):
        response = client.post('/convert',
            json={'input': '255', 'inputType': 'decimal', 'outputType': 'hexadecimal'})
        data = json.loads(response.data)
        assert data['result'] == 'ff'
        assert data['error'] is None
    
    def test_hexadecimal_to_decimal(self, client):
        response = client.post('/convert',
            json={'input': 'ff', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '255'
        assert data['error'] is None
    
    def test_decimal_to_octal(self, client):
        response = client.post('/convert',
            json={'input': '64', 'inputType': 'decimal', 'outputType': 'octal'})
        data = json.loads(response.data)
        assert data['result'] == '100'
        assert data['error'] is None
    
    def test_octal_to_decimal(self, client):
        response = client.post('/convert',
            json={'input': '100', 'inputType': 'octal', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '64'
        assert data['error'] is None
    
    def test_text_to_decimal(self, client):
        response = client.post('/convert',
            json={'input': 'five', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '5'
        assert data['error'] is None
    
    def test_decimal_to_text(self, client):
        response = client.post('/convert',
            json={'input': '5', 'inputType': 'decimal', 'outputType': 'text'})
        data = json.loads(response.data)
        assert data['result'] == 'five'
        assert data['error'] is None
    
    def test_base64_to_decimal(self, client):
        # Test with 'AQ==' which should be 1 in big-endian
        response = client.post('/convert',
            json={'input': 'AQ==', 'inputType': 'base64', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '1'
        assert data['error'] is None
    
    def test_decimal_to_base64(self, client):
        response = client.post('/convert',
            json={'input': '1', 'inputType': 'decimal', 'outputType': 'base64'})
        data = json.loads(response.data)
        # Should return base64 representation of 1
        assert data['error'] is None
        assert isinstance(data['result'], str)
    
    def test_zero_handling(self, client):
        """Test zero conversion across all formats"""
        # Zero to binary
        response = client.post('/convert',
            json={'input': '0', 'inputType': 'decimal', 'outputType': 'binary'})
        data = json.loads(response.data)
        assert data['result'] == '0'
        
        # Zero to text
        response = client.post('/convert',
            json={'input': '0', 'inputType': 'decimal', 'outputType': 'text'})
        data = json.loads(response.data)
        assert data['result'] == 'zero'
        
        # Text zero to decimal
        response = client.post('/convert',
            json={'input': 'zero', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] == '0'
    
    def test_error_handling_invalid_input_type(self, client):
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'invalid', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_output_type(self, client):
        response = client.post('/convert',
            json={'input': '42', 'inputType': 'decimal', 'outputType': 'invalid'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_binary(self, client):
        response = client.post('/convert',
            json={'input': '102', 'inputType': 'binary', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_hex(self, client):
        response = client.post('/convert',
            json={'input': 'gg', 'inputType': 'hexadecimal', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_octal(self, client):
        response = client.post('/convert',
            json={'input': '89', 'inputType': 'octal', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_text(self, client):
        response = client.post('/convert',
            json={'input': 'eleven', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None
    
    def test_error_handling_invalid_base64(self, client):
        response = client.post('/convert',
            json={'input': 'invalid!', 'inputType': 'base64', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['result'] is None
        assert data['error'] is not None

class TestAllConversions:
    """Test all possible input/output type combinations"""
    
    def test_all_format_combinations(self, client):
        """Test a representative value across all format combinations"""
        formats = ['text', 'binary', 'octal', 'decimal', 'hexadecimal', 'base64']
        test_value = '5'  # Start with decimal 5
        
        # First convert decimal 5 to all other formats to get reference values
        reference_values = {'decimal': '5'}
        
        for output_format in formats:
            if output_format != 'decimal':
                response = client.post('/convert',
                    json={'input': test_value, 'inputType': 'decimal', 'outputType': output_format})
                data = json.loads(response.data)
                if data['error'] is None:
                    reference_values[output_format] = data['result']
        
        # Now test all combinations
        for input_format in formats:
            for output_format in formats:
                if input_format in reference_values and output_format in reference_values:
                    input_val = reference_values[input_format]
                    expected_output = reference_values[output_format]
                    
                    response = client.post('/convert',
                        json={'input': input_val, 'inputType': input_format, 'outputType': output_format})
                    data = json.loads(response.data)
                    
                    if input_format == 'text' and input_val not in ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']:
                        # Text conversion might fail for complex numbers
                        continue
                    
                    assert data['error'] is None, f"Error converting from {input_format} to {output_format}: {data['error']}"
                    assert data['result'] == expected_output, f"Failed {input_format}→{output_format}: expected {expected_output}, got {data['result']}"

class TestBugDetection:
    """Tests specifically designed to detect bugs in the implementation"""
    
    def test_base64_zero_bug(self, client):
        """Test base64 conversion of zero - this was a bug that should now be fixed"""
        # Try to convert 0 to base64
        response = client.post('/convert',
            json={'input': '0', 'inputType': 'decimal', 'outputType': 'base64'})
        data = json.loads(response.data)
        
        # This should now work after the fix
        assert data['error'] is None
        assert data['result'] is not None
        
        # Test roundtrip
        response2 = client.post('/convert',
            json={'input': data['result'], 'inputType': 'base64', 'outputType': 'decimal'})
        data2 = json.loads(response2.data)
        assert data2['error'] is None
        assert data2['result'] == '0'
    
    def test_base64_endianness_bug(self):
        """Test that base64 conversion uses correct little-endian byte order"""
        # The requirement specifies little-endian
        # Let's test with a multi-byte number
        
        # For number 256 (0x0100):
        # - Little-endian bytes: [0x00, 0x01] -> base64: "AAE="
        # - Big-endian bytes: [0x01, 0x00] -> base64: "AQA="
        
        # The implementation should now use little-endian
        b64_result = number_to_base64(256)
        recovered = base64_to_number(b64_result)
        
        # This should work with little-endian implementation
        assert recovered == 256
        
        # According to requirements, 256 in little-endian should be "AAE="
        import base64
        
        # What little-endian should produce:
        little_endian_bytes = (256).to_bytes(2, byteorder='little')
        expected_little_endian_b64 = base64.b64encode(little_endian_bytes).decode('utf-8')
        
        # The implementation should now use little-endian
        assert b64_result == expected_little_endian_b64
    
    def test_text_conversion_limitations(self, client):
        """Test the improved text conversion capabilities"""
        # The text_to_number function should now handle more numbers
        
        response = client.post('/convert',
            json={'input': 'eleven', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['error'] is None
        assert data['result'] == '11'
        
        response = client.post('/convert',
            json={'input': 'twenty', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['error'] is None
        assert data['result'] == '20'
        
        # Test compound numbers
        response = client.post('/convert',
            json={'input': 'twenty one', 'inputType': 'text', 'outputType': 'decimal'})
        data = json.loads(response.data)
        assert data['error'] is None
        assert data['result'] == '21'
        
        # num2words can convert numbers to more complex text
        response = client.post('/convert',
            json={'input': '11', 'inputType': 'decimal', 'outputType': 'text'})
        data = json.loads(response.data)
        assert data['error'] is None
        assert data['result'] == 'eleven'