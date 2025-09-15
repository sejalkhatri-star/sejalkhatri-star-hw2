import pytest
import base64
from index import app, number_to_base64, base64_to_number

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# --- Helpers ---
def convert(client, input_value, input_type, output_type):
    return client.post("/convert", json={
        "input": input_value,
        "inputType": input_type,
        "outputType": output_type
    })

# --- Core Tests ---
@pytest.mark.parametrize("input_value,input_type,expected", [
    ("five", "text", 5),
    ("101", "binary", 5),
    ("5", "octal", 5),
    ("5", "decimal", 5),
    ("5", "hexadecimal", 5),
    (number_to_base64(5), "base64", 5),
])
def test_input_to_decimal(client, input_value, input_type, expected):
    res = convert(client, input_value, input_type, "decimal")
    data = res.get_json()
    assert data["error"] is None
    assert int(data["result"]) == expected

@pytest.mark.parametrize("output_type,expected", [
    ("text", "five"),
    ("binary", "101"),
    ("octal", "5"),
    ("decimal", "5"),
    ("hexadecimal", "5"),
    ("base64", number_to_base64(5)),
])
def test_decimal_to_all(client, output_type, expected):
    res = convert(client, "5", "decimal", output_type)
    data = res.get_json()
    assert data["error"] is None
    assert data["result"] == expected

# --- Error Handling ---
def test_invalid_input_type(client):
    res = convert(client, "5", "unknown", "decimal")
    data = res.get_json()
    assert data["error"] is not None

def test_invalid_output_type(client):
    res = convert(client, "5", "decimal", "unknown")
    data = res.get_json()
    assert data["error"] is not None

def test_invalid_binary(client):
    res = convert(client, "102", "binary", "decimal")  # invalid binary digit
    data = res.get_json()
    assert data["error"] is not None

def test_invalid_base64(client):
    res = convert(client, "!!!", "base64", "decimal")
    data = res.get_json()
    assert data["error"] is not None

def test_text_not_number(client):
    res = convert(client, "apple", "text", "decimal")
    data = res.get_json()
    assert data["error"] is not None

# --- Round Trip Base64 ---
def test_base64_round_trip():
    for num in [0, 1, 42, 999, 123456789]:
        b64 = number_to_base64(num)
        decoded = base64_to_number(b64)
        assert decoded == num