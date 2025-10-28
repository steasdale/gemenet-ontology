# ============================================================================
# Python Additions for gmn:P70_17_documents_sale_price_currency
# ============================================================================
#
# INSTRUCTIONS:
# 1. Copy the transform_p70_17_documents_sale_price_currency() function below
# 2. Paste into gmn_to_cidoc_transform.py after transform_p70_16_documents_sale_price_amount()
# 3. Add function call in transform_item() (see details below)
# 4. Verify uuid4 is imported at top of file
# 5. Run tests to verify implementation
#
# LOCATION: Insert after transform_p70_16_documents_sale_price_amount() function
#
# ============================================================================

def transform_p70_17_documents_sale_price_currency(data):
    """
    Transform gmn:P70_17_documents_sale_price_currency to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency > E98_Currency
    
    This function coordinates with transform_p70_16_documents_sale_price_amount() to build
    a complete E97_Monetary_Amount entity with both amount and currency information.
    
    Args:
        data: Item data dictionary containing potential currency information
        
    Returns:
        Transformed data dictionary with currency moved to CIDOC-CRM structure
        
    Example Input:
        {
            '@id': 'http://example.org/contract001',
            '@type': 'gmn:E31_2_Sales_Contract',
            'gmn:P70_17_documents_sale_price_currency': ['http://vocab.example.org/currency/lira_genovese']
        }
        
    Example Output:
        {
            '@id': 'http://example.org/contract001',
            '@type': 'gmn:E31_2_Sales_Contract',
            'cidoc:P70_documents': [{
                '@id': 'http://example.org/contract001/acquisition',
                '@type': 'cidoc:E8_Acquisition',
                'cidoc:P177_assigned_property_of_type': {
                    '@id': 'http://example.org/contract001/acquisition/monetary_amount',
                    '@type': 'cidoc:E97_Monetary_Amount',
                    'cidoc:P180_has_currency': {
                        '@id': 'http://vocab.example.org/currency/lira_genovese',
                        '@type': 'cidoc:E98_Currency'
                    }
                }
            }]
        }
    """
    # Check if the property exists in the data
    if 'gmn:P70_17_documents_sale_price_currency' not in data:
        return data
    
    # Get the currency values (should be a list)
    currencies = data['gmn:P70_17_documents_sale_price_currency']
    
    # Get the subject URI (the contract document)
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure E8_Acquisition exists (may have been created by P70.16 or other properties)
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure E97_Monetary_Amount exists (may have been created by P70.16)
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        monetary_uri = f"{acquisition['@id']}/monetary_amount"
        acquisition['cidoc:P177_assigned_property_of_type'] = {
            '@id': monetary_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
    
    # Get reference to the monetary amount
    monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
    
    # Process each currency (typically only one)
    for currency_obj in currencies:
        # Handle different currency formats
        if isinstance(currency_obj, dict):
            # Currency is already a structured object
            currency_data = currency_obj.copy()
            # Ensure it has the E98_Currency type
            if '@type' not in currency_data:
                currency_data['@type'] = 'cidoc:E98_Currency'
        else:
            # Currency is a simple URI or string
            currency_uri = str(currency_obj)
            currency_data = {
                '@id': currency_uri,
                '@type': 'cidoc:E98_Currency'
            }
        
        # Add currency to the monetary amount
        monetary_amount['cidoc:P180_has_currency'] = currency_data
    
    # Remove the simplified property from the data
    del data['gmn:P70_17_documents_sale_price_currency']
    
    return data

# ============================================================================
# INTEGRATION INTO TRANSFORM_ITEM()
# ============================================================================
#
# Add this function call in the transform_item() function in the sales 
# contract properties section, immediately after the P70.16 call:
#
# def transform_item(item, include_internal=False):
#     """Transform a single item, applying all transformation rules."""
#     
#     # ... existing code ...
#     
#     # Sales contract properties (P70.1-P70.17)
#     item = transform_p70_1_documents_seller(item)
#     item = transform_p70_2_documents_buyer(item)
#     item = transform_p70_3_documents_transfer_of(item)
#     item = transform_p70_4_documents_sellers_procurator(item)
#     item = transform_p70_5_documents_buyers_procurator(item)
#     item = transform_p70_6_documents_sellers_guarantor(item)
#     item = transform_p70_7_documents_buyers_guarantor(item)
#     item = transform_p70_8_documents_broker(item)
#     item = transform_p70_9_documents_payment_provider_for_buyer(item)
#     item = transform_p70_10_documents_payment_recipient_for_seller(item)
#     item = transform_p70_11_documents_referenced_person(item)
#     item = transform_p70_12_documents_payment_through_organization(item)
#     item = transform_p70_13_documents_referenced_place(item)
#     item = transform_p70_14_documents_referenced_object(item)
#     item = transform_p70_15_documents_witness(item)
#     item = transform_p70_16_documents_sale_price_amount(item)
#     item = transform_p70_17_documents_sale_price_currency(item)  # ADD THIS LINE
#     
#     # ... rest of transform_item() ...
#
# ============================================================================

# ============================================================================
# REQUIRED IMPORTS
# ============================================================================
# Ensure these imports are at the top of gmn_to_cidoc_transform.py:
#
# from uuid import uuid4
#
# ============================================================================

# ============================================================================
# TESTING CODE
# ============================================================================

def test_p70_17_transformation():
    """Test cases for P70.17 transformation."""
    
    print("Testing P70.17 documents sale price currency transformation...\n")
    
    # Test 1: Simple currency reference
    print("Test 1: Simple currency reference")
    test_data_1 = {
        '@id': 'http://example.org/contract001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_17_documents_sale_price_currency': ['http://vocab.example.org/currency/lira_genovese']
    }
    result_1 = transform_p70_17_documents_sale_price_currency(test_data_1)
    assert 'cidoc:P70_documents' in result_1
    assert result_1['cidoc:P70_documents'][0]['cidoc:P177_assigned_property_of_type']['cidoc:P180_has_currency']['@id'] == 'http://vocab.example.org/currency/lira_genovese'
    print("✓ Test 1 passed\n")
    
    # Test 2: Currency with amount (integration test)
    print("Test 2: Currency with amount")
    test_data_2 = {
        '@id': 'http://example.org/contract002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['250.00'],
        'gmn:P70_17_documents_sale_price_currency': ['http://vocab.example.org/currency/florin']
    }
    # Simulate transformation order
    result_2 = transform_p70_16_documents_sale_price_amount(test_data_2)
    result_2 = transform_p70_17_documents_sale_price_currency(result_2)
    monetary = result_2['cidoc:P70_documents'][0]['cidoc:P177_assigned_property_of_type']
    assert 'cidoc:P180_has_currency_amount' in monetary
    assert 'cidoc:P180_has_currency' in monetary
    print("✓ Test 2 passed\n")
    
    # Test 3: Structured currency object
    print("Test 3: Structured currency object")
    test_data_3 = {
        '@id': 'http://example.org/contract003',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_17_documents_sale_price_currency': [{
            '@id': 'http://vocab.example.org/currency/ducat',
            'rdfs:label': 'Venetian Ducat'
        }]
    }
    result_3 = transform_p70_17_documents_sale_price_currency(test_data_3)
    currency = result_3['cidoc:P70_documents'][0]['cidoc:P177_assigned_property_of_type']['cidoc:P180_has_currency']
    assert currency['@id'] == 'http://vocab.example.org/currency/ducat'
    assert currency['rdfs:label'] == 'Venetian Ducat'
    assert currency['@type'] == 'cidoc:E98_Currency'
    print("✓ Test 3 passed\n")
    
    # Test 4: No currency (no-op)
    print("Test 4: No currency property (no-op)")
    test_data_4 = {
        '@id': 'http://example.org/contract004',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_16_documents_sale_price_amount': ['100.00']
    }
    result_4 = transform_p70_17_documents_sale_price_currency(test_data_4)
    # Should return unchanged (except for any keys already present)
    assert 'gmn:P70_17_documents_sale_price_currency' not in result_4
    print("✓ Test 4 passed\n")
    
    # Test 5: Complete sales contract with multiple properties
    print("Test 5: Complete sales contract")
    test_data_5 = {
        '@id': 'http://example.org/contract005',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_1_documents_seller': ['http://example.org/person/giovanni'],
        'gmn:P70_2_documents_buyer': ['http://example.org/person/antonio'],
        'gmn:P70_3_documents_transfer_of': ['http://example.org/building/house001'],
        'gmn:P70_16_documents_sale_price_amount': ['1500.00'],
        'gmn:P70_17_documents_sale_price_currency': ['http://vocab.example.org/currency/lira_genovese']
    }
    # Note: In real usage, all transformation functions would be called in sequence
    # Here we just test P70.17
    result_5 = transform_p70_17_documents_sale_price_currency(test_data_5)
    assert 'cidoc:P70_documents' in result_5
    assert 'gmn:P70_17_documents_sale_price_currency' not in result_5
    print("✓ Test 5 passed\n")
    
    print("All tests passed! ✓")

# Uncomment to run tests:
# test_p70_17_transformation()

# ============================================================================
# IMPLEMENTATION NOTES
# ============================================================================
#
# 1. COORDINATION WITH P70.16:
#    This function must coordinate with transform_p70_16_documents_sale_price_amount()
#    to ensure both contribute to the same E97_Monetary_Amount entity.
#    
#    - Both functions check for existing E8_Acquisition
#    - Both functions check for existing E97_Monetary_Amount
#    - Both functions use the same URI pattern for consistency
#    - P70.16 adds: cidoc:P180_has_currency_amount
#    - P70.17 adds: cidoc:P180_has_currency
#
# 2. TRANSFORMATION ORDER:
#    The order doesn't matter because both functions check for existing nodes.
#    However, conventionally P70.16 (amount) should be processed before P70.17 (currency).
#
# 3. URI PATTERN:
#    Monetary Amount URI: {acquisition_uri}/monetary_amount
#    Example: http://example.org/contract001/acquisition/monetary_amount
#
# 4. CURRENCY FORMATS:
#    The function handles three formats:
#    a) Simple URI string: 'http://vocab.example.org/currency/lira'
#    b) Structured object: {'@id': 'http://...', 'rdfs:label': 'Lira', ...}
#    c) Blank node: [a cidoc:E98_Currency; rdfs:label "Lira"]
#
# 5. TYPE ASSIGNMENT:
#    Always ensures currency has @type: cidoc:E98_Currency
#
# 6. MULTIPLE CURRENCIES:
#    If multiple currencies are provided (unusual), the last one in the list
#    will be assigned. Consider adding validation for this edge case.
#
# 7. ERROR HANDLING:
#    Consider adding validation for:
#    - Empty currency values
#    - Invalid URI formats
#    - Missing required fields in structured objects
#
# ============================================================================

# ============================================================================
# VALIDATION HELPER FUNCTION (OPTIONAL)
# ============================================================================

def validate_p70_17_output(data):
    """
    Validate that P70.17 transformation produced correct structure.
    
    Args:
        data: Transformed data dictionary
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check that simplified property was removed
    if 'gmn:P70_17_documents_sale_price_currency' in data:
        errors.append("Simplified property 'gmn:P70_17_documents_sale_price_currency' was not removed")
    
    # Check E8_Acquisition exists
    if 'cidoc:P70_documents' not in data:
        errors.append("E8_Acquisition not created (cidoc:P70_documents missing)")
        return errors  # Can't continue validation
    
    acquisition = data['cidoc:P70_documents'][0]
    
    # Check E97_Monetary_Amount exists
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        errors.append("E97_Monetary_Amount not created (cidoc:P177_assigned_property_of_type missing)")
        return errors  # Can't continue validation
    
    monetary = acquisition['cidoc:P177_assigned_property_of_type']
    
    # Check currency was added
    if 'cidoc:P180_has_currency' not in monetary:
        errors.append("Currency not added to monetary amount (cidoc:P180_has_currency missing)")
        return errors
    
    currency = monetary['cidoc:P180_has_currency']
    
    # Check currency has required fields
    if '@type' not in currency:
        errors.append("Currency missing @type")
    elif currency['@type'] != 'cidoc:E98_Currency':
        errors.append(f"Currency has incorrect type: {currency['@type']}")
    
    if '@id' not in currency:
        errors.append("Currency missing @id")
    
    return errors

# Usage:
# errors = validate_p70_17_output(transformed_data)
# if errors:
#     print("Validation errors:", errors)
# else:
#     print("Validation passed!")

# ============================================================================
# DEBUGGING HELPER FUNCTION (OPTIONAL)
# ============================================================================

def debug_p70_17_transformation(data):
    """
    Print detailed debug information about P70.17 transformation.
    
    Args:
        data: Data dictionary to inspect
    """
    print("=" * 60)
    print("P70.17 TRANSFORMATION DEBUG INFO")
    print("=" * 60)
    
    print(f"\nDocument URI: {data.get('@id', 'N/A')}")
    print(f"Document Type: {data.get('@type', 'N/A')}")
    
    if 'gmn:P70_17_documents_sale_price_currency' in data:
        print(f"\n✓ Has P70.17 property")
        print(f"  Value: {data['gmn:P70_17_documents_sale_price_currency']}")
    else:
        print("\n✗ No P70.17 property found")
    
    if 'cidoc:P70_documents' in data:
        print(f"\n✓ Has E8_Acquisition")
        acquisition = data['cidoc:P70_documents'][0]
        print(f"  URI: {acquisition.get('@id', 'N/A')}")
        
        if 'cidoc:P177_assigned_property_of_type' in acquisition:
            print(f"\n✓ Has E97_Monetary_Amount")
            monetary = acquisition['cidoc:P177_assigned_property_of_type']
            print(f"  URI: {monetary.get('@id', 'N/A')}")
            
            if 'cidoc:P180_has_currency' in monetary:
                print(f"\n✓ Has currency")
                currency = monetary['cidoc:P180_has_currency']
                print(f"  URI: {currency.get('@id', 'N/A')}")
                print(f"  Type: {currency.get('@type', 'N/A')}")
                if 'rdfs:label' in currency:
                    print(f"  Label: {currency['rdfs:label']}")
            else:
                print(f"\n✗ No currency in monetary amount")
        else:
            print(f"\n✗ No E97_Monetary_Amount")
    else:
        print(f"\n✗ No E8_Acquisition")
    
    print("\n" + "=" * 60)

# Usage:
# debug_p70_17_transformation(my_data)

# ============================================================================
# END OF PYTHON ADDITIONS
# ============================================================================
