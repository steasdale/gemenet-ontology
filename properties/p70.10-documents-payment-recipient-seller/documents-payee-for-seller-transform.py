# Python Additions for P70.10 Documents Payment Recipient for Seller
# Ready-to-copy Python code for gmn_to_cidoc_transform.py

# ============================================================================
# AAT CONSTANTS
# ============================================================================
# Add these to the constants section at the top of the file (if not already present)

AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/aat/300417629"
AAT_PAYEE = "http://vocab.getty.edu/aat/300025555"

# ============================================================================
# MAIN TRANSFORMATION FUNCTION
# ============================================================================
# Add this function after transform_p70_9_documents_payment_provider_for_buyer

def transform_p70_10_documents_payment_recipient_for_seller(data):
    """
    Transform gmn:P70_10_documents_payment_recipient_for_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    
    Creates an E7_Activity node for each payment recipient, representing the payment receipt
    activity. The activity is typed as a financial transaction and links the recipient
    as the actor carrying out the activity in the role of "payee".
    
    The transformation handles:
    - Single or multiple payment recipients
    - Both URI strings and object dictionaries as input
    - Integration with existing E8_Acquisition structures
    - Unique activity URI generation using hash
    
    Args:
        data (dict): Dictionary containing the GMN item data with the simplified property
        
    Returns:
        dict: Transformed data dictionary with P70.10 converted to full CIDOC-CRM structure
        
    Raises:
        None: Function handles missing properties gracefully by returning unchanged data
        
    Example:
        Input:
            {
                '@id': 'contract:123',
                '@type': 'gmn:E31_2_Sales_Contract',
                'gmn:P70_10_documents_payment_recipient_for_seller': [
                    {'@id': 'person:Antonio', '@type': 'cidoc:E21_Person'}
                ]
            }
            
        Output:
            {
                '@id': 'contract:123',
                '@type': 'gmn:E31_2_Sales_Contract',
                'cidoc:P70_documents': [{
                    '@id': 'contract:123/acquisition',
                    '@type': 'cidoc:E8_Acquisition',
                    'cidoc:P9_consists_of': [{
                        '@id': 'contract:123/activity/payment_abc123',
                        '@type': 'cidoc:E7_Activity',
                        'cidoc:P2_has_type': {
                            '@id': 'http://vocab.getty.edu/aat/300417629',
                            '@type': 'cidoc:E55_Type'
                        },
                        'cidoc:P14_carried_out_by': [
                            {'@id': 'person:Antonio', '@type': 'cidoc:E21_Person'}
                        ],
                        'cidoc:P14.1_in_the_role_of': {
                            '@id': 'http://vocab.getty.edu/aat/300025555',
                            '@type': 'cidoc:E55_Type'
                        }
                    }]
                }]
            }
    
    Notes:
        - Each payment recipient creates a separate E7_Activity node
        - Activity URIs are generated with hash for uniqueness
        - Original simplified property is removed after transformation
        - Supports multiple recipients by creating multiple activities
        - Integrates with existing acquisition if present
    """
    # Check if the property exists in the data
    if 'gmn:P70_10_documents_payment_recipient_for_seller' not in data:
        return data
    
    # Get the list of payment recipients
    payees = data['gmn:P70_10_documents_payment_recipient_for_seller']
    
    # Get the subject URI, generate one if not present
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    # If no acquisition exists, create one
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition (assume first one)
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of array if not present
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Create an E7_Activity for each payment recipient
    for payee_obj in payees:
        # Handle both URI strings and object dictionaries
        if isinstance(payee_obj, dict):
            # Object dictionary format
            payee_uri = payee_obj.get('@id', '')
            payee_data = payee_obj.copy()
        else:
            # Simple URI string format
            payee_uri = str(payee_obj)
            payee_data = {
                '@id': payee_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash of recipient URI
        # The hash ensures uniqueness while being deterministic
        activity_hash = str(hash(payee_uri + 'payment_recipient'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        # Create the payment receipt activity node
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            # Type the activity as a financial transaction
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            # Link to the payment recipient who carries out the activity
            'cidoc:P14_carried_out_by': [payee_data],
            # Specify the role as payee
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYEE,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Add the activity to the acquisition's constituent activities
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the simplified property after transformation
    del data['gmn:P70_10_documents_payment_recipient_for_seller']
    
    return data


# ============================================================================
# REGISTRATION IN TRANSFORM_ITEM FUNCTION
# ============================================================================
# Add this line in the transform_item() function in the P70 sales contract section
# Place it after transform_p70_9_documents_payment_provider_for_buyer

"""
Example placement in transform_item():

def transform_item(item, include_internal=False):
    # ... other transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)
    item = transform_p70_10_documents_payment_recipient_for_seller(item)  # ADD THIS LINE
    item = transform_p70_11_documents_referenced_person(item)
    # ... rest of transformations ...
"""

# ============================================================================
# HELPER FUNCTION (OPTIONAL)
# ============================================================================
# Optional helper to validate payment recipient data before transformation

def validate_payment_recipient(data):
    """
    Validate payment recipient data before transformation.
    
    Args:
        data (dict): Contract data to validate
        
    Returns:
        tuple: (bool, list) - (is_valid, list_of_errors)
        
    Example:
        >>> is_valid, errors = validate_payment_recipient(contract_data)
        >>> if not is_valid:
        ...     for error in errors:
        ...         print(f"Validation error: {error}")
    """
    errors = []
    
    # Check if property exists
    if 'gmn:P70_10_documents_payment_recipient_for_seller' not in data:
        return True, []  # Not an error if property not present
    
    payees = data['gmn:P70_10_documents_payment_recipient_for_seller']
    
    # Check that payees is a list
    if not isinstance(payees, list):
        errors.append("Payment recipients must be provided as a list")
        return False, errors
    
    # Check that list is not empty
    if len(payees) == 0:
        errors.append("Payment recipient list cannot be empty")
        return False, errors
    
    # Validate each recipient
    for idx, payee in enumerate(payees):
        if isinstance(payee, dict):
            # Check for @id
            if '@id' not in payee:
                errors.append(f"Payment recipient {idx} missing @id field")
            # Check for @type (optional but recommended)
            if '@type' not in payee:
                # Not critical, but could warn
                pass
        elif not isinstance(payee, str):
            errors.append(f"Payment recipient {idx} must be string URI or object with @id")
    
    # Check for duplicate recipients (optional validation)
    recipient_ids = []
    for payee in payees:
        payee_id = payee.get('@id') if isinstance(payee, dict) else payee
        if payee_id in recipient_ids:
            errors.append(f"Duplicate payment recipient: {payee_id}")
        recipient_ids.append(payee_id)
    
    return len(errors) == 0, errors


# ============================================================================
# TESTING CODE
# ============================================================================
# Use this code to test the transformation function

def test_p70_10_transformation():
    """
    Test function for P70.10 transformation.
    Run this to verify the transformation works correctly.
    """
    from uuid import uuid4
    import json
    
    print("Testing P70.10 Transformation")
    print("=" * 60)
    
    # Test 1: Single payment recipient
    print("\nTest 1: Single Payment Recipient")
    print("-" * 60)
    test_data_1 = {
        '@id': 'contract:test_001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_10_documents_payment_recipient_for_seller': [
            {
                '@id': 'person:Antonio_Rossi',
                '@type': 'cidoc:E21_Person'
            }
        ]
    }
    
    result_1 = transform_p70_10_documents_payment_recipient_for_seller(test_data_1.copy())
    print("Input:", json.dumps(test_data_1, indent=2))
    print("\nOutput:", json.dumps(result_1, indent=2))
    
    # Assertions for Test 1
    assert 'cidoc:P70_documents' in result_1, "Missing P70_documents"
    assert len(result_1['cidoc:P70_documents']) > 0, "Empty P70_documents"
    acquisition = result_1['cidoc:P70_documents'][0]
    assert 'cidoc:P9_consists_of' in acquisition, "Missing P9_consists_of"
    assert len(acquisition['cidoc:P9_consists_of']) == 1, "Wrong number of activities"
    activity = acquisition['cidoc:P9_consists_of'][0]
    assert activity['@type'] == 'cidoc:E7_Activity', "Wrong activity type"
    assert 'cidoc:P14_carried_out_by' in activity, "Missing P14_carried_out_by"
    print("\n✓ Test 1 passed!")
    
    # Test 2: Multiple payment recipients
    print("\n\nTest 2: Multiple Payment Recipients")
    print("-" * 60)
    test_data_2 = {
        '@id': 'contract:test_002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_10_documents_payment_recipient_for_seller': [
            {'@id': 'person:Recipient_A', '@type': 'cidoc:E21_Person'},
            {'@id': 'person:Recipient_B', '@type': 'cidoc:E21_Person'},
            {'@id': 'person:Recipient_C', '@type': 'cidoc:E21_Person'}
        ]
    }
    
    result_2 = transform_p70_10_documents_payment_recipient_for_seller(test_data_2.copy())
    print("Input: 3 recipients")
    print("\nOutput:", json.dumps(result_2, indent=2))
    
    # Assertions for Test 2
    acquisition_2 = result_2['cidoc:P70_documents'][0]
    assert len(acquisition_2['cidoc:P9_consists_of']) == 3, "Wrong number of activities"
    print("\n✓ Test 2 passed!")
    
    # Test 3: String URI format
    print("\n\nTest 3: String URI Format")
    print("-" * 60)
    test_data_3 = {
        '@id': 'contract:test_003',
        'gmn:P70_10_documents_payment_recipient_for_seller': [
            'person:Simple_URI'
        ]
    }
    
    result_3 = transform_p70_10_documents_payment_recipient_for_seller(test_data_3.copy())
    print("Input: String URI")
    print("\nOutput:", json.dumps(result_3, indent=2))
    
    # Assertions for Test 3
    acquisition_3 = result_3['cidoc:P70_documents'][0]
    activity_3 = acquisition_3['cidoc:P9_consists_of'][0]
    assert activity_3['cidoc:P14_carried_out_by'][0]['@id'] == 'person:Simple_URI'
    print("\n✓ Test 3 passed!")
    
    # Test 4: Integration with existing acquisition
    print("\n\nTest 4: Integration with Existing Acquisition")
    print("-" * 60)
    test_data_4 = {
        '@id': 'contract:test_004',
        'cidoc:P70_documents': [{
            '@id': 'contract:test_004/acquisition',
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P23_transferred_title_from': [{'@id': 'person:Seller'}]
        }],
        'gmn:P70_10_documents_payment_recipient_for_seller': [
            {'@id': 'person:Recipient'}
        ]
    }
    
    result_4 = transform_p70_10_documents_payment_recipient_for_seller(test_data_4.copy())
    print("Input: Existing acquisition with seller")
    print("\nOutput:", json.dumps(result_4, indent=2))
    
    # Assertions for Test 4
    acquisition_4 = result_4['cidoc:P70_documents'][0]
    assert 'cidoc:P23_transferred_title_from' in acquisition_4, "Lost existing seller"
    assert 'cidoc:P9_consists_of' in acquisition_4, "Missing consists_of"
    print("\n✓ Test 4 passed!")
    
    # Test 5: No property present (should return unchanged)
    print("\n\nTest 5: No Property Present")
    print("-" * 60)
    test_data_5 = {
        '@id': 'contract:test_005',
        '@type': 'gmn:E31_2_Sales_Contract'
    }
    
    result_5 = transform_p70_10_documents_payment_recipient_for_seller(test_data_5.copy())
    assert result_5 == test_data_5, "Data should be unchanged"
    print("✓ Test 5 passed! (no changes when property absent)")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
Example 1: Basic usage in transformation pipeline
------------------------------------------------

from gmn_to_cidoc_transform import transform_item

contract_data = {
    '@id': 'contract:12345',
    '@type': 'gmn:E31_2_Sales_Contract',
    'gmn:P70_1_documents_seller': [{'@id': 'person:Giovanni'}],
    'gmn:P70_2_documents_buyer': [{'@id': 'person:Marco'}],
    'gmn:P70_10_documents_payment_recipient_for_seller': [
        {'@id': 'person:Antonio'}
    ]
}

transformed = transform_item(contract_data)
print(json.dumps(transformed, indent=2))


Example 2: Processing batch of contracts
---------------------------------------

contracts = load_contracts_from_database()

for contract in contracts:
    if 'gmn:P70_10_documents_payment_recipient_for_seller' in contract:
        # Validate before transformation
        is_valid, errors = validate_payment_recipient(contract)
        if is_valid:
            transformed = transform_p70_10_documents_payment_recipient_for_seller(contract)
            save_to_triplestore(transformed)
        else:
            log_errors(contract['@id'], errors)


Example 3: Integration with other transformations
------------------------------------------------

def transform_complete_sales_contract(contract):
    # Transform all properties in sequence
    contract = transform_p70_1_documents_seller(contract)
    contract = transform_p70_2_documents_buyer(contract)
    contract = transform_p70_3_documents_transfer_of(contract)
    # ... other transformations ...
    contract = transform_p70_10_documents_payment_recipient_for_seller(contract)
    # ... more transformations ...
    return contract
"""

# ============================================================================
# DEBUGGING UTILITIES
# ============================================================================

def debug_print_p70_10_structure(data):
    """
    Print the P70.10 structure for debugging.
    Useful for understanding the transformation output.
    """
    print("P70.10 Structure Debug Output")
    print("=" * 60)
    
    if 'cidoc:P70_documents' not in data:
        print("No P70_documents found")
        return
    
    for idx, acquisition in enumerate(data['cidoc:P70_documents']):
        print(f"\nAcquisition {idx}: {acquisition.get('@id')}")
        
        if 'cidoc:P9_consists_of' in acquisition:
            for act_idx, activity in enumerate(acquisition['cidoc:P9_consists_of']):
                if activity.get('@type') == 'cidoc:E7_Activity':
                    # Check if this is a payment activity
                    activity_type = activity.get('cidoc:P2_has_type', {}).get('@id')
                    if activity_type == AAT_FINANCIAL_TRANSACTION:
                        print(f"  Payment Activity {act_idx}:")
                        print(f"    URI: {activity.get('@id')}")
                        
                        recipients = activity.get('cidoc:P14_carried_out_by', [])
                        for rec in recipients:
                            print(f"    Recipient: {rec.get('@id')}")
                        
                        role = activity.get('cidoc:P14.1_in_the_role_of', {})
                        print(f"    Role: {role.get('@id')}")


# ============================================================================
# END OF PYTHON ADDITIONS
# ============================================================================

"""
IMPLEMENTATION CHECKLIST:
□ Add AAT constants to top of file
□ Add transform_p70_10_documents_payment_recipient_for_seller function
□ Add function call in transform_item()
□ Test with test_p70_10_transformation()
□ Verify integration with existing transformations
□ Run validation on sample data
□ Check output in triplestore
"""
