import sys
import os

# This line tells Python to look in the parent directory so it can find 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transformer import validate_records

def test_validate_records_logic():
    # 1. Setup: Create "dirty" mock data
    mock_data = [
        {'user_id': 1, 'email': 'valid@test.com', 'city': 'London', 'zipcode': '12345'}, # OK
        {'user_id': 1, 'email': 'dup@test.com', 'city': 'London', 'zipcode': '12345'},   # Fail: Duplicate ID
        {'user_id': 2, 'email': 'no_at_sign.com', 'city': 'Paris', 'zipcode': '54321'},  # Fail: Email
        {'user_id': 3, 'email': 'city@test.com', 'city': None, 'zipcode': '54321'},     # Fail: City
        {'user_id': 4, 'email': 'zip@test.com', 'city': 'Berlin', 'zipcode': '12'},      # Fail: Zip
    ]
    
    # 2. Execute
    valid, rejected = validate_records(mock_data)
    
    # 3. Assert (The "Checks")
    assert len(valid) == 1, "Should only have 1 valid record"
    assert len(rejected) == 4, "Should have 4 rejected records"
    
    # Verify specific rejection reasons
    reasons = [r['reject_reason'] for r in rejected]
    assert "Duplicate ID" in reasons
    assert "Invalid Email" in reasons
    assert "City Null" in reasons
    assert "Zipcode < 5" in reasons

    print("\n All validation rules passed the test!")