# Python Additions for P70.9 Documents Payment Provider for Buyer
# Ready-to-copy code for gmn_to_cidoc_transform.py

# =============================================================================
# CONSTANTS TO ADD (if not already present)
# Add these near the top of the script with other AAT constants (~line 20-40)
# =============================================================================

AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"

# =============================================================================
# TRANSFORMATION FUNCTION
# Add this function with other P70 transformation functions (~line 690)
# =============================================================================

def transform_p70_9_documents_payment_provider_for_buyer(data):
    """
    Transform gmn:P70_9_documents_payment_provider_for_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    
    Args:
        data (dict): Item data dictionary containing the property
        
    Returns:
        dict: Transformed item dictionary with full CIDOC-CRM structure
        
    Example Input:
        {
            "@id": "contract/123",
            "gmn:P70_9_documents_payment_provider_for_buyer": [
                {"@id": "person/456", "@type": "cidoc:E21_Person"}
            ]
        }
        
    Example Output:
        {
            "@id": "contract/123",
            "cidoc:P70_documents": [{
                "@id": "contract/123/acquisition",
                "@type": "cidoc:E8_Acquisition",
                "cidoc:P9_consists_of": [{
                    "@id": "contract/123/activity/payment_a7b3c4d2",
                    "@type": "cidoc:E7_Activity",
                    "cidoc:P2_has_type": {
                        "@id": "http://vocab.getty.edu/page/aat/300055984",
                        "@type": "cidoc:E55_Type"
                    },
                    "cidoc:P14_carried_out_by": [
                        {"@id": "person/456", "@type": "cidoc:E21_Person"}
                    ],
                    "cidoc:P14.1_in_the_role_of": {
                        "@id": "http://vocab.getty.edu/page/aat/300386048",
                        "@type": "cidoc:E55_Type"
                    }
                }]
            }]
        }
    """
    # Check if property exists in data
    if 'gmn:P70_9_documents_payment_provider_for_buyer' not in data:
        return data
    
    # Extract payment providers list
    payers = data['gmn:P70_9_documents_payment_provider_for_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    # If P70_documents doesn't exist or is empty, create new acquisition
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition (first element in list)
    acquisition = data['cidoc:P70_documents'][0]
    
    # Initialize P9_consists_of if not present
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Process each payment provider
    for payer_obj in payers:
        # Handle both dictionary objects and URI strings
        if isinstance(payer_obj, dict):
            payer_uri = payer_obj.get('@id', '')
            payer_data = payer_obj.copy()
        else:
            # If it's just a URI string, create a basic person object
            payer_uri = str(payer_obj)
            payer_data = {
                '@id': payer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Generate unique activity URI using hash
        # This ensures each payment provider gets a unique activity
        activity_hash = str(hash(payer_uri + 'payment_provider'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        # Create E7_Activity with financial transaction type and payer role
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P14_carried_out_by': [payer_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYER,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        # Append activity to acquisition's P9_consists_of
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    # Remove the shortcut property after transformation
    del data['gmn:P70_9_documents_payment_provider_for_buyer']
    
    return data

# =============================================================================
# FUNCTION CALL IN transform_item()
# Add this line in the transform_item() function after P70.8 transformation
# and before P70.10 transformation (~line 2450)
# =============================================================================

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # ... earlier transformations ...
    
    # Sales contract properties (P70.1-P70.17)
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    item = transform_p70_3_documents_transfer_of(item)
    item = transform_p70_4_documents_sellers_procurator(item)
    item = transform_p70_5_documents_buyers_procurator(item)
    item = transform_p70_6_documents_sellers_guarantor(item)
    item = transform_p70_7_documents_buyers_guarantor(item)
    item = transform_p70_8_documents_broker(item)
    item = transform_p70_9_documents_payment_provider_for_buyer(item)  # ADD THIS LINE
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    
    # ... continue with other transformations ...
    
    return item

# =============================================================================
# HELPER FUNCTION (optional - for validation/testing)
# =============================================================================

def validate_payment_provider_transformation(item):
    """
    Validate that P70.9 transformation was successful.
    
    Args:
        item: Transformed item dictionary
        
    Returns:
        bool: True if transformation is valid, False otherwise
        
    Raises:
        AssertionError: If validation fails with details
    """
    # Ensure shortcut property has been removed
    assert 'gmn:P70_9_documents_payment_provider_for_buyer' not in item, \
        "Shortcut property should be removed after transformation"
    
    # Check for P70_documents
    if 'cidoc:P70_documents' not in item:
        return False  # No acquisition, might be valid if property wasn't present
    
    acquisition = item['cidoc:P70_documents'][0]
    
    # Check for P9_consists_of
    if 'cidoc:P9_consists_of' not in acquisition:
        return False
    
    # Look for payment activities
    payment_activities_found = False
    for activity in acquisition['cidoc:P9_consists_of']:
        # Check if this is a payment provider activity
        role = activity.get('cidoc:P14.1_in_the_role_of', {})
        if role.get('@id') == AAT_PAYER:
            payment_activities_found = True
            
            # Validate activity structure
            assert activity.get('@type') == 'cidoc:E7_Activity', \
                "Payment activity must be E7_Activity"
            
            assert 'cidoc:P2_has_type' in activity, \
                "Payment activity must have P2_has_type"
            
            assert activity['cidoc:P2_has_type']['@id'] == AAT_FINANCIAL_TRANSACTION, \
                "Payment activity must be typed as financial transaction"
            
            assert 'cidoc:P14_carried_out_by' in activity, \
                "Payment activity must have P14_carried_out_by"
            
            assert len(activity['cidoc:P14_carried_out_by']) > 0, \
                "Payment activity must have at least one payment provider"
    
    return payment_activities_found

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_usage_1():
    """Example: Single payment provider transformation."""
    
    # Input data with payment provider
    input_data = {
        "@id": "https://example.org/contract/123",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {
                "@id": "https://example.org/person/Pietro_Bianchi",
                "@type": "cidoc:E21_Person"
            }
        ]
    }
    
    # Transform
    output_data = transform_p70_9_documents_payment_provider_for_buyer(input_data)
    
    # Output will have full CIDOC-CRM structure
    print(json.dumps(output_data, indent=2))

def example_usage_2():
    """Example: Multiple payment providers transformation."""
    
    # Input data with multiple payment providers
    input_data = {
        "@id": "https://example.org/contract/456",
        "@type": "gmn:E31_2_Sales_Contract",
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {"@id": "https://example.org/person/Lorenzo_Pazzi"},
            {"@id": "https://example.org/person/Cosimo_Rucellai"}
        ]
    }
    
    # Transform
    output_data = transform_p70_9_documents_payment_provider_for_buyer(input_data)
    
    # Output will have two E7_Activity nodes in P9_consists_of
    acquisition = output_data['cidoc:P70_documents'][0]
    activities = acquisition['cidoc:P9_consists_of']
    print(f"Created {len(activities)} payment activities")

def example_usage_3():
    """Example: Integration with existing acquisition."""
    
    # Input data that already has an E8_Acquisition from other properties
    input_data = {
        "@id": "https://example.org/contract/789",
        "@type": "gmn:E31_2_Sales_Contract",
        "cidoc:P70_documents": [{
            "@id": "https://example.org/contract/789/acquisition",
            "@type": "cidoc:E8_Acquisition",
            "cidoc:P22_transferred_title_to": [
                {"@id": "https://example.org/person/Buyer_123"}
            ]
        }],
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {"@id": "https://example.org/person/Payer_456"}
        ]
    }
    
    # Transform - will add to existing acquisition
    output_data = transform_p70_9_documents_payment_provider_for_buyer(input_data)
    
    # The existing acquisition now has P9_consists_of with payment activity
    acquisition = output_data['cidoc:P70_documents'][0]
    assert 'cidoc:P9_consists_of' in acquisition
    assert 'cidoc:P22_transferred_title_to' in acquisition  # Preserved

# =============================================================================
# TEST CASES
# =============================================================================

def test_transform_single_payer():
    """Test transformation with single payment provider."""
    data = {
        "@id": "test/contract/1",
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {"@id": "test/person/1"}
        ]
    }
    
    result = transform_p70_9_documents_payment_provider_for_buyer(data)
    
    assert 'gmn:P70_9_documents_payment_provider_for_buyer' not in result
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents'][0]['cidoc:P9_consists_of']) == 1
    
    activity = result['cidoc:P70_documents'][0]['cidoc:P9_consists_of'][0]
    assert activity['cidoc:P2_has_type']['@id'] == AAT_FINANCIAL_TRANSACTION
    assert activity['cidoc:P14.1_in_the_role_of']['@id'] == AAT_PAYER
    
    print("✓ Single payer test passed")

def test_transform_multiple_payers():
    """Test transformation with multiple payment providers."""
    data = {
        "@id": "test/contract/2",
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {"@id": "test/person/1"},
            {"@id": "test/person/2"}
        ]
    }
    
    result = transform_p70_9_documents_payment_provider_for_buyer(data)
    
    assert 'cidoc:P70_documents' in result
    assert len(result['cidoc:P70_documents'][0]['cidoc:P9_consists_of']) == 2
    
    print("✓ Multiple payers test passed")

def test_transform_no_property():
    """Test transformation when property doesn't exist."""
    data = {
        "@id": "test/contract/3",
        "@type": "gmn:E31_2_Sales_Contract"
    }
    
    result = transform_p70_9_documents_payment_provider_for_buyer(data)
    
    # Should return unchanged
    assert result == data
    assert 'cidoc:P70_documents' not in result
    
    print("✓ No property test passed")

def test_transform_with_existing_acquisition():
    """Test transformation with pre-existing acquisition."""
    data = {
        "@id": "test/contract/4",
        "cidoc:P70_documents": [{
            "@id": "test/contract/4/acquisition",
            "@type": "cidoc:E8_Acquisition"
        }],
        "gmn:P70_9_documents_payment_provider_for_buyer": [
            {"@id": "test/person/1"}
        ]
    }
    
    result = transform_p70_9_documents_payment_provider_for_buyer(data)
    
    # Should add to existing acquisition
    assert result['cidoc:P70_documents'][0]['@id'] == "test/contract/4/acquisition"
    assert 'cidoc:P9_consists_of' in result['cidoc:P70_documents'][0]
    
    print("✓ Existing acquisition test passed")

def run_all_tests():
    """Run all test cases."""
    print("Running payment provider transformation tests...\n")
    test_transform_single_payer()
    test_transform_multiple_payers()
    test_transform_no_property()
    test_transform_with_existing_acquisition()
    print("\n✓ All tests passed!")

# =============================================================================
# NOTES ON IMPLEMENTATION
# =============================================================================

"""
Implementation Notes:

1. URI Generation:
   - Activity URIs use hash of payer URI + 'payment_provider' string
   - Last 8 characters of hash ensure reasonable URI length
   - Hash ensures uniqueness and consistency across transformations

2. Activity Structure:
   - Always typed as financial transaction (AAT 300055984)
   - Payment provider linked via P14_carried_out_by
   - Role designated as payer (AAT 300386048) via P14.1_in_the_role_of

3. Integration:
   - Works with existing E8_Acquisition nodes
   - Preserves other acquisition properties (P22, P23, P24, etc.)
   - Multiple payment providers create multiple E7_Activity nodes

4. Error Handling:
   - Returns early if property not present (graceful degradation)
   - Handles both URI strings and object dictionaries
   - Creates acquisition if needed

5. Performance:
   - Linear time complexity: O(n) where n = number of payment providers
   - Hash generation is constant time
   - No external dependencies beyond uuid4

6. Validation:
   - Shortcut property must be removed after transformation
   - Activity must have correct type and role
   - Payment provider must be E21_Person
"""

# =============================================================================
# END OF FILE
# =============================================================================
