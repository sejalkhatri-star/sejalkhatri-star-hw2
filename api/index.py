from flask import Flask, render_template, request, jsonify
from num2words import num2words
from text2digits import text2digits
import base64
import re

app = Flask(__name__)

def text_to_number(text):
    """Convert English text number to integer"""
    # Remove any non-alphanumeric characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s-]', '', text.lower())
    
    # Special case for zero
    if text in ['zero', 'nil']:
        return 0
    
    # Extended dictionary for number words
    number_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
        'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
        'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000
    }
    
    if text in number_words:
        return number_words[text]
    
    # Try to handle compound numbers like "twenty one", "thirty five", etc.
    words = text.split()
    if len(words) == 2:
        if words[0] in number_words and words[1] in number_words:
            first_val = number_words[words[0]]
            second_val = number_words[words[1]]
            # Handle cases like "twenty one" (20 + 1)
            if first_val >= 20 and first_val <= 90 and second_val <= 9:
                return first_val + second_val
    
    # Try using text2digits as fallback for more complex cases
    try:
        t2d = text2digits.Text2Digits()
        converted = t2d.convert(text)
        # Extract numbers from the converted text
        numbers = re.findall(r'\d+', converted)
        if numbers:
            return int(numbers[0])
    except:
        pass
    
    raise ValueError("Unable to convert text to number")

def number_to_text(number):
    """Convert integer to English text"""
    try:
        return num2words(number)
    except:
        raise ValueError("Unable to convert number to text")

def base64_to_number(b64_str):
    """Convert base64 to integer"""
    try:
        # Decode base64 to bytes, then convert bytes to integer
        decoded_bytes = base64.b64decode(b64_str)
        return int.from_bytes(decoded_bytes, byteorder='little')
    except:
        raise ValueError("Invalid base64 input")

def number_to_base64(number):
    """Convert integer to base64"""
    try:
        # Handle zero case specially
        if number == 0:
            return base64.b64encode(b'\x00').decode('utf-8')
        
        # Convert integer to bytes, then encode to base64
        byte_count = (number.bit_length() + 7) // 8
        number_bytes = number.to_bytes(byte_count, byteorder='little')
        return base64.b64encode(number_bytes).decode('utf-8')
    except:
        raise ValueError("Unable to convert to base64")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_value = data['input']
        input_type = data['inputType']
        output_type = data['outputType']
        
        # Convert input to integer based on input type
        if input_type == 'text':
            number = text_to_number(input_value)
        elif input_type == 'binary':
            number = int(input_value, 2)
        elif input_type == 'octal':
            number = int(input_value, 8)
        elif input_type == 'decimal':
            number = int(input_value)
        elif input_type == 'hexadecimal':
            number = int(input_value, 16)
        elif input_type == 'base64':
            number = base64_to_number(input_value)
        else:
            raise ValueError("Invalid input type")
            
        # Convert integer to output type
        if output_type == 'text':
            result = number_to_text(number)
        elif output_type == 'binary':
            result = bin(number)[2:]  # Remove '0b' prefix
        elif output_type == 'octal':
            result = oct(number)[2:]  # Remove '0o' prefix
        elif output_type == 'decimal':
            result = str(number)
        elif output_type == 'hexadecimal':
            result = hex(number)[2:]  # Remove '0x' prefix
        elif output_type == 'base64':
            result = number_to_base64(number)
        else:
            raise ValueError("Invalid output type")
            
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
