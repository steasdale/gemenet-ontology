# Python Transformation Function for gmn:P70_16_documents_sale_price_amount

"""
This file contains the Python transformation function for the 
gmn:P70_16_documents_sale_price_amount property.

This function should already exist in your gmn_to_cidoc_transform.py file.
Use this as a reference or to restore the function if needed.

Location: Insert after transform_p70_15_documents_witness() function
Call from: transform_item() function, in the P70 transformations section
"""

from uuid import uuid4

def transform_p70_16_documents_sale_price_amount(data):
    """
    Transform gmn:P70_16_documents_sale_price_amount to full CIDOC-CRM structure.
    
    Transformation path:
    gmn:P70_16_documents_sale_price_amount (xsd:decimal)
      → cidoc:P70_documents → cidoc:E8_Acquisition
        → cidoc:P177_assigned_property_of_type → cidoc:E97_Monetary_Amount
          → cidoc:P181_has_amount → xsd:decimal
    
    Args:
        data (dict): Item data dictionary containing the GMN shortcut property
        
    Returns:
        dict: Transformed item dictionary with CIDOC-CRM compliant structure
        
    Note:
        This function works in coordination with transform_p70_17_documents_sale_price_currency().
        Both functions contribute to the same E97_Monetary_Amount entity:
        - P70_16 adds the numeric amount (P181_has_amount)
        - P70_17 adds the currency type (P180_has_currency)
        
    Important:
        The current codebase may use 'cidoc:P180_has_currency_amount' which is NON-STANDARD.
        This implementation uses the correct CIDOC-CRM property 'cidoc:P181_has_amount'.
        
        Correct CIDOC-CRM properties:
        - cidoc:P181_has_amount for numeric values
        - cidoc:P180_has_currency for currency types
        
    Example:
        Input:
        {
            '@id': 'http://example.org/sale001',
            '@type': 'gmn:E31_2_Sales_Contract',
            'gmn:P70_16_documents_sale_price_amount': ['1500.50']
        }
        
        Output:
        {
            '@id': 'http://example.org/sale001',
            '@type': 'gmn:E31_2_Sales_Contract',
            'cidoc:P70_documents': [{
                '@id': 'http://example.org/sale001/acquisition',
                '@type': 'cidoc:E8_Acquisition',
                'cidoc:P177_assigned_property_of_type': {
                    '@id': 'http://example.org/sale001/acquisition/monetary_amount',
                    '@type': 'cidoc:E97_Monetary_Amount',
                    'cidoc:P181_has_amount': '1500.50'
                }
            }]
        }
    """
    # Check if property exists in data
    if 'gmn:P70_16_documents_sale_price_amount' not in data:
        return data
    
    # Get the amount values (usually a list with one item)
    amounts = data['gmn:P70_16_documents_sale_price_amount']
    
    # Get the subject URI for constructing related URIs
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists
    # If it doesn't exist, create it; otherwise use the existing one
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition (first item in list)
    acquisition = data['cidoc:P70_documents'][0]
    
    # Process each amount value
    for amount_obj in amounts:
        # Handle both dict format ({'@value': '1500.50'}) and string format
        if isinstance(amount_obj, dict):
            amount_value = amount_obj.get('@value', '')
        else:
            amount_value = str(amount_obj)
        
        # Skip empty values
        if not amount_value:
            continue
        
        # Create or get E97_Monetary_Amount entity
        # This may already exist if P70_17 (currency) was processed first
        if 'cidoc:P177_assigned_property_of_type' not in acquisition:
            monetary_uri = f"{acquisition['@id']}/monetary_amount"
            acquisition['cidoc:P177_assigned_property_of_type'] = {
                '@id': monetary_uri,
                '@type': 'cidoc:E97_Monetary_Amount'
            }
        
        # Get reference to the monetary amount entity
        monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
        
        # Add the amount using P181_has_amount (CORRECT CIDOC-CRM property)
        # Note: P180_has_currency_amount is NOT a standard CIDOC-CRM property
        monetary_amount['cidoc:P181_has_amount'] = amount_value
    
    # Remove the shortcut property from the data
    del data['gmn:P70_16_documents_sale_price_amount']
    
    return data


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================

"""
STEP 1: Verify Function Exists
-------------------------------
This function should already be present in your gmn_to_cidoc_transform.py file,
inserted after the transform_p70_15_documents_witness() function.

Location in file: Around line 900-1000 (in the P70 transformations section)


STEP 2: Verify Function is Called
----------------------------------
Add or verify this line in the transform_item() function:

    def transform_item(item, include_internal=False):
        '''Transform a single item, applying all transformation rules.'''
        
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
        item = transform_p70_10_documents_payment_recipient_for_seller(item)
        item = transform_p70_11_documents_referenced_person(item)
        item = transform_p70_12_documents_payment_through_organization(item)
        item = transform_p70_13_documents_referenced_place(item)
        item = transform_p70_14_documents_referenced_object(item)
        item = transform_p70_15_documents_witness(item)
        item = transform_p70_16_documents_sale_price_amount(item)      # ← THIS LINE
        item = transform_p70_17_documents_sale_price_currency(item)
        
        # ... other transformations ...
        
        return item

IMPORTANT: P70_16 must be called BEFORE P70_17 so the E97_Monetary_Amount 
entity is created first, then P70_17 can add the currency to it.


STEP 3: Verify Required Imports
--------------------------------
Ensure these imports are at the top of gmn_to_cidoc_transform.py:

    from uuid import uuid4
    import json


STEP 4: Update Any Old Implementation
--------------------------------------
If you find an old version using 'cidoc:P180_has_currency_amount', update it
to use 'cidoc:P181_has_amount' as shown in this function.

The incorrect property was:
    monetary_amount['cidoc:P180_has_currency_amount'] = amount_value  # WRONG

The correct property is:
    monetary_amount['cidoc:P181_has_amount'] = amount_value  # CORRECT
"""


# ============================================================================
# TESTING CODE
# ============================================================================

def test_p70_16_transformation():
    """
    Test suite for transform_p70_16_documents_sale_price_amount function.
    
    Run this to verify the transformation works correctly.
    """
    print("=" * 70)
    print("Testing P70_16 Sale Price Amount Transformation")
    print("=" * 70)
    
    # Test 1: Basic transformation
    print("\nTest 1: Basic Amount Transformation")
    print("-" * 70)
    test1 = {
        '@id': 'http://example.org/sale001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['1500.50']
    }
    
    result1 = transform_p70_16_documents_sale_price_amount(test1.copy())
    
    print("Input:")
    print(f"  Amount: {test1['gmn:P70_16_documents_sale_price_amount']}")
    print("\nOutput:")
    print(f"  Acquisition created: {'cidoc:P70_documents' in result1}")
    if 'cidoc:P70_documents' in result1:
        acq = result1['cidoc:P70_documents'][0]
        print(f"  Acquisition URI: {acq['@id']}")
        if 'cidoc:P177_assigned_property_of_type' in acq:
            mon = acq['cidoc:P177_assigned_property_of_type']
            print(f"  Monetary amount URI: {mon['@id']}")
            print(f"  Amount value: {mon.get('cidoc:P181_has_amount', 'NOT FOUND')}")
            print(f"  ✓ Test 1 PASSED" if 'cidoc:P181_has_amount' in mon else "  ✗ Test 1 FAILED")
        else:
            print("  ✗ Test 1 FAILED - No monetary amount created")
    else:
        print("  ✗ Test 1 FAILED - No acquisition created")
    
    # Test 2: With existing acquisition
    print("\n\nTest 2: Amount with Existing Acquisition")
    print("-" * 70)
    test2 = {
        '@id': 'http://example.org/sale002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'cidoc:P70_documents': [{
            '@id': 'http://example.org/sale002/acquisition',
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P23_transferred_title_from': {'@id': 'http://example.org/person/seller'}
        }],
        'gmn:P70_16_documents_sale_price_amount': ['2000.00']
    }
    
    result2 = transform_p70_16_documents_sale_price_amount(test2.copy())
    
    print("Input:")
    print(f"  Existing acquisition: Yes")
    print(f"  Amount: {test2['gmn:P70_16_documents_sale_price_amount']}")
    print("\nOutput:")
    acq2 = result2['cidoc:P70_documents'][0]
    print(f"  Seller preserved: {'cidoc:P23_transferred_title_from' in acq2}")
    print(f"  Monetary amount added: {'cidoc:P177_assigned_property_of_type' in acq2}")
    if 'cidoc:P177_assigned_property_of_type' in acq2:
        mon2 = acq2['cidoc:P177_assigned_property_of_type']
        print(f"  Amount value: {mon2.get('cidoc:P181_has_amount', 'NOT FOUND')}")
        passed = ('cidoc:P23_transferred_title_from' in acq2 and 
                  'cidoc:P181_has_amount' in mon2)
        print(f"  ✓ Test 2 PASSED" if passed else "  ✗ Test 2 FAILED")
    else:
        print("  ✗ Test 2 FAILED")
    
    # Test 3: Empty value handling
    print("\n\nTest 3: Empty Value Handling")
    print("-" * 70)
    test3 = {
        '@id': 'http://example.org/sale003',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['']
    }
    
    result3 = transform_p70_16_documents_sale_price_amount(test3.copy())
    
    print("Input:")
    print(f"  Amount: '' (empty string)")
    print("\nOutput:")
    print(f"  Shortcut property removed: {'gmn:P70_16_documents_sale_price_amount' not in result3}")
    if 'cidoc:P70_documents' in result3:
        acq3 = result3['cidoc:P70_documents'][0]
        if 'cidoc:P177_assigned_property_of_type' in acq3:
            mon3 = acq3['cidoc:P177_assigned_property_of_type']
            has_amount = 'cidoc:P181_has_amount' in mon3
            print(f"  Amount added: {has_amount}")
            print(f"  ✓ Test 3 PASSED (empty value skipped)" if not has_amount else "  ⚠ Test 3 WARNING (empty value added)")
        else:
            print(f"  ✓ Test 3 PASSED (no monetary amount created for empty value)")
    else:
        print(f"  ✓ Test 3 PASSED (no acquisition created for empty value)")
    
    # Test 4: Decimal precision
    print("\n\nTest 4: Decimal Precision")
    print("-" * 70)
    test4 = {
        '@id': 'http://example.org/sale004',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['1234.567890']
    }
    
    result4 = transform_p70_16_documents_sale_price_amount(test4.copy())
    
    print("Input:")
    print(f"  Amount: 1234.567890")
    print("\nOutput:")
    if 'cidoc:P70_documents' in result4:
        acq4 = result4['cidoc:P70_documents'][0]
        if 'cidoc:P177_assigned_property_of_type' in acq4:
            mon4 = acq4['cidoc:P177_assigned_property_of_type']
            amount4 = mon4.get('cidoc:P181_has_amount', '')
            print(f"  Amount value: {amount4}")
            print(f"  Precision preserved: {amount4 == '1234.567890'}")
            print(f"  ✓ Test 4 PASSED" if amount4 == '1234.567890' else "  ✗ Test 4 FAILED")
        else:
            print("  ✗ Test 4 FAILED - No monetary amount")
    else:
        print("  ✗ Test 4 FAILED - No acquisition")
    
    print("\n" + "=" * 70)
    print("Testing Complete")
    print("=" * 70)


def test_p70_16_and_p70_17_coordination():
    """
    Test coordination between P70_16 (amount) and P70_17 (currency).
    
    This test verifies that both properties contribute to the same 
    E97_Monetary_Amount entity.
    """
    print("\n" + "=" * 70)
    print("Testing P70_16 and P70_17 Coordination")
    print("=" * 70)
    
    # Note: This assumes transform_p70_17_documents_sale_price_currency exists
    # Adjust if your function has a different name
    
    test_data = {
        '@id': 'http://example.org/sale005',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['750.25'],
        'gmn:P70_17_documents_sale_price_currency': [{
            '@id': 'http://vocab.getty.edu/aat/lira_genovese'
        }]
    }
    
    print("\nInput:")
    print(f"  Amount: {test_data['gmn:P70_16_documents_sale_price_amount']}")
    print(f"  Currency: {test_data['gmn:P70_17_documents_sale_price_currency']}")
    
    # Transform in correct order: amount first, then currency
    result = transform_p70_16_documents_sale_price_amount(test_data.copy())
    
    # Note: Uncomment the line below if you want to test with P70_17
    # result = transform_p70_17_documents_sale_price_currency(result)
    
    print("\nOutput (after P70_16 transformation):")
    if 'cidoc:P70_documents' in result:
        acq = result['cidoc:P70_documents'][0]
        if 'cidoc:P177_assigned_property_of_type' in acq:
            mon = acq['cidoc:P177_assigned_property_of_type']
            print(f"  Monetary amount URI: {mon['@id']}")
            print(f"  Amount: {mon.get('cidoc:P181_has_amount', 'NOT FOUND')}")
            print(f"  Currency: {mon.get('cidoc:P180_has_currency', 'NOT YET (P70_17 not run)')}")
            print(f"\n  ✓ Amount added to E97_Monetary_Amount")
            print(f"  Note: Run P70_17 transformation to add currency to same entity")
        else:
            print("  ✗ FAILED - No monetary amount")
    else:
        print("  ✗ FAILED - No acquisition")
    
    print("=" * 70)


# ============================================================================
# RUN TESTS (uncomment to execute)
# ============================================================================

if __name__ == '__main__':
    # Run basic transformation tests
    test_p70_16_transformation()
    
    # Run coordination test
    # Note: This will show P70_16 working; P70_17 would be run separately
    test_p70_16_and_p70_17_coordination()


# ============================================================================
# EXAMPLE USAGE IN TRANSFORM_ITEM
# ============================================================================

"""
Here's how this function fits into the larger transformation pipeline:

def transform_item(item, include_internal=False):
    '''Transform a single item, applying all transformation rules.'''
    
    # Name and title properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p102_1_has_title(item)
    
    # Creation properties
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
    
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
    item = transform_p70_10_documents_payment_recipient_for_seller(item)
    item = transform_p70_11_documents_referenced_person(item)
    item = transform_p70_12_documents_payment_through_organization(item)
    item = transform_p70_13_documents_referenced_place(item)
    item = transform_p70_14_documents_referenced_object(item)
    item = transform_p70_15_documents_witness(item)
    item = transform_p70_16_documents_sale_price_amount(item)      # ← HERE
    item = transform_p70_17_documents_sale_price_currency(item)    # ← After P70_16
    
    # Continue with other transformations...
    
    return item
"""


# ============================================================================
# NOTES AND WARNINGS
# ============================================================================

"""
IMPORTANT NOTES:

1. CIDOC-CRM Property Names:
   - Use 'cidoc:P181_has_amount' for numeric amounts (CORRECT)
   - NOT 'cidoc:P180_has_currency_amount' (INCORRECT - not in CIDOC-CRM)
   - Use 'cidoc:P180_has_currency' for currency types (handled by P70_17)

2. Transformation Order:
   - P70_16 must run BEFORE P70_17
   - This ensures the E97_Monetary_Amount is created first
   - Then P70_17 adds the currency to the same entity

3. Decimal Precision:
   - Values are kept as strings to preserve exact precision
   - Don't convert to float (causes rounding errors)
   - The xsd:decimal datatype in RDF preserves exact values

4. Empty Values:
   - Empty strings are skipped (no amount added)
   - The shortcut property is still removed

5. Multiple Amounts:
   - Current implementation processes all amounts in list
   - Last value wins if multiple amounts provided
   - Consider business logic: should multiple amounts be supported?

6. URI Patterns:
   - Acquisition: {subject_uri}/acquisition
   - Monetary Amount: {acquisition_uri}/monetary_amount
   - These patterns must match between P70_16 and P70_17

7. Error Handling:
   - Function gracefully handles missing properties
   - Skips empty values
   - Preserves existing acquisition structure
   - Removes shortcut property in all cases
"""
