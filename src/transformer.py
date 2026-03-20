import logging

def flatten_user(user):
    """Phase 2: Nested JSON to Flat Dict"""
    address = user.get('address', {})
    company = user.get('company', {})
    return {
        'user_id': user.get('id'),
        'name': user.get('name'),
        'email': user.get('email'),
        'city': address.get('city'),
        'zipcode': address.get('zipcode'),
        'company_name': company.get('name')
    }

def validate_records(flat_data):
    """Phase 3: Apply Business Rules"""
    valid, rejected = [], []
    seen_ids = set()

    for row in flat_data:
        uid = row.get('user_id')
        email = str(row.get('email', ''))
        city = row.get('city')
        zipcode = str(row.get('zipcode', ''))

        reason = None
        if uid in seen_ids: reason = "Duplicate ID"
        elif "@" not in email: reason = "Invalid Email"
        elif not city: reason = "City Null"
        elif len(zipcode) < 5: reason = "Zipcode < 5"

        if reason:
            row['reject_reason'] = reason
            rejected.append(row)
        else:
            seen_ids.add(uid)
            valid.append(row)
            
    return valid, rejected