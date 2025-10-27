# GMN P70.11 Documents Referenced Person - Python Transformation Function
# Ready-to-copy code for gmn_to_cidoc_transform.py

# ==============================================================================
# INSERTION LOCATION
# ==============================================================================
# Insert after: def transform_p70_10_documents_payment_recipient_for_seller(data)
#               (around line 803)
# Insert before: def transform_p70_12_documents_payment_through_organization(data)
#
# Make sure there are blank lines before and after the function.
# ==============================================================================

def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    
    This property creates a direct reference from the document to persons mentioned
    in the text who do not have specific transactional roles.
    
    Unlike other P70 properties that model participation in E8_Acquisition events,
    this property represents simple documentary reference: the document refers to
    the person without implying their participation in the documented transaction.
    
    Transformation Pattern:
        Input:  E31_Document > gmn:P70_11_documents_referenced_person > E21_Person
        Output: E31_Document > cidoc:P67_refers_to > E21_Person
    
    Args:
        data (dict): Document data dictionary potentially containing 
                     gmn:P70_11_documents_referenced_person property
        
    Returns:
        dict: Transformed data with cidoc:P67_refers_to property,
              original P70.11 property removed
    
    Examples:
        >>> # Single person as URI
        >>> data = {
        ...     '@id': 'contract:001',
        ...     '@type': 'gmn:E31_2_Sales_Contract',
        ...     'gmn:P70_11_documents_referenced_person': ['person:giovanni']
        ... }
        >>> result = transform_p70_11_documents_referenced_person(data)
        >>> 'cidoc:P67_refers_to' in result
        True
        >>> result['cidoc:P67_refers_to'][0]['@type']
        'cidoc:E21_Person'
        
        >>> # Multiple persons, mixed format
        >>> data = {
        ...     '@id': 'contract:002',
        ...     '@type': 'gmn:E31_2_Sales_Contract',
        ...     'gmn:P70_11_documents_referenced_person': [
        ...         {'@id': 'person:marco', '@type': 'cidoc:E21_Person'},
        ...         'person:pietro'
        ...     ]
        ... }
        >>> result = transform_p70_11_documents_referenced_person(data)
        >>> len(result['cidoc:P67_refers_to'])
        2
        
        >>> # No property present - data unchanged
        >>> data = {'@id': 'contract:003'}
        >>> result = transform_p70_11_documents_referenced_person(data)
        >>> result == data
        True
    
    Notes:
        - If cidoc:P67_refers_to already exists (from other properties like P70.13
          or P70.14), new persons are appended to the existing array
        - Person objects are preserved with all their properties
        - URI-only references are expanded to minimal person objects with type
        - The @type is added/preserved as cidoc:E21_Person for all persons
        - Original gmn:P70_11 property is always removed after transformation
    """
    # Check if property exists in data
    if 'gmn:P70_11_documents_referenced_person' not in data:
        return data
    
    # Get the list of referenced persons
    persons = data['gmn:P70_11_documents_referenced_person']
    
    # Initialize P67_refers_to array if it doesn't exist
    # (It might already exist from P70.13 or P70.14 transformations)
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    # Process each referenced person
    for person_obj in persons:
        if isinstance(person_obj, dict):
            # Person is already a full object with properties
            person_data = person_obj.copy()
            
            # Ensure it has E21_Person type
            # (preserve existing type if present, add if missing)
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            # Person is just a URI string
            # Create minimal person object
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add person to P67_refers_to array
        data['cidoc:P67_refers_to'].append(person_data)
    
    # Remove the simplified GMN property
    del data['gmn:P70_11_documents_referenced_person']
    
    return data


# ==============================================================================
# FUNCTION REGISTRATION IN TRANSFORM PIPELINE
# ==============================================================================
# Add this line to the transform_item() function (around line 2350):
#
#     item = transform_p70_11_documents_referenced_person(item)
#
# It should be placed after transform_p70_10 and before transform_p70_12:
#
#     item = transform_p70_10_documents_payment_recipient_for_seller(item)
#     item = transform_p70_11_documents_referenced_person(item)  # ADD THIS
#     item = transform_p70_12_documents_payment_through_organization(item)
# ==============================================================================


# ==============================================================================
# UNIT TESTS
# ==============================================================================
# Copy these tests to your test file or run them separately

def test_p70_11_single_person_uri():
    """Test transformation with single person as URI string"""
    data = {
        '@id': 'contract:test001',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_11_documents_referenced_person': ['person:giovanni_deceased']
    }
    
    result = transform_p70_11_documents_referenced_person(data)
    
    # Verify transformation
    assert 'gmn:P70_11_documents_referenced_person' not in result, \
        "Original property should be removed"
    assert 'cidoc:P67_refers_to' in result, \
        "P67_refers_to should be created"
    assert len(result['cidoc:P67_refers_to']) == 1, \
        "Should have exactly one person"
    assert result['cidoc:P67_refers_to'][0]['@id'] == 'person:giovanni_deceased', \
        "Person URI should match"
    assert result['cidoc:P67_refers_to'][0]['@type'] == 'cidoc:E21_Person', \
        "Person should have E21_Person type"
    
    print("✓ Test passed: Single person URI")


def test_p70_11_multiple_persons_mixed():
    """Test transformation with multiple persons in different formats"""
    data = {
        '@id': 'contract:test002',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_11_documents_referenced_person': [
            {
                '@id': 'person:marco',
                '@type': 'cidoc:E21_Person',
                'rdfs:label': 'Marco (neighbor)'
            },
            'person:pietro',
            {
                '@id': 'person:antonio',
                'rdfs:label': 'Antonio (previous owner)'
            }
        ]
    }
    
    result = transform_p70_11_documents_referenced_person(data)
    
    # Verify transformation
    assert 'gmn:P70_11_documents_referenced_person' not in result
    assert 'cidoc:P67_refers_to' in result
    assert len(result['cidoc:P67_refers_to']) == 3, \
        "Should have three persons"
    
    # Verify all have E21_Person type
    for person in result['cidoc:P67_refers_to']:
        assert person['@type'] == 'cidoc:E21_Person', \
            f"Person {person['@id']} should have E21_Person type"
    
    # Verify properties preserved
    marco = [p for p in result['cidoc:P67_refers_to'] if p['@id'] == 'person:marco'][0]
    assert 'rdfs:label' in marco, "Properties should be preserved"
    
    # Verify type added to person without type
    antonio = [p for p in result['cidoc:P67_refers_to'] if p['@id'] == 'person:antonio'][0]
    assert antonio['@type'] == 'cidoc:E21_Person', "Type should be added"
    
    print("✓ Test passed: Multiple persons mixed format")


def test_p70_11_no_property():
    """Test that function handles absence of property gracefully"""
    data = {
        '@id': 'contract:test003',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_1_documents_seller': ['person:seller001']
    }
    
    result = transform_p70_11_documents_referenced_person(data)
    
    # Verify no changes
    assert result == data, "Data should be unchanged"
    assert 'cidoc:P67_refers_to' not in result, \
        "P67_refers_to should not be created"
    
    print("✓ Test passed: No property present")


def test_p70_11_existing_p67_refers_to():
    """Test integration with existing P67_refers_to from other properties"""
    data = {
        '@id': 'contract:test004',
        '@type': 'gmn:E31_2_Sales_Contract',
        'cidoc:P67_refers_to': [
            {
                '@id': 'place:venice',
                '@type': 'cidoc:E53_Place'
            }
        ],
        'gmn:P70_11_documents_referenced_person': ['person:lorenzo']
    }
    
    result = transform_p70_11_documents_referenced_person(data)
    
    # Verify both place and person in P67_refers_to
    assert len(result['cidoc:P67_refers_to']) == 2, \
        "Should have both place and person"
    
    # Check that place is preserved
    places = [e for e in result['cidoc:P67_refers_to'] 
              if e['@type'] == 'cidoc:E53_Place']
    assert len(places) == 1, "Place should be preserved"
    
    # Check that person is added
    persons = [e for e in result['cidoc:P67_refers_to'] 
               if e['@type'] == 'cidoc:E21_Person']
    assert len(persons) == 1, "Person should be added"
    
    print("✓ Test passed: Existing P67_refers_to integration")


def test_p70_11_person_with_properties():
    """Test that person properties are fully preserved"""
    data = {
        '@id': 'contract:test005',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_11_documents_referenced_person': [
            {
                '@id': 'person:detailed',
                '@type': 'cidoc:E21_Person',
                'gmn:P1_1_has_name': 'Giovanni Rossi',
                'rdfs:label': 'Giovanni Rossi (deceased father)',
                'rdfs:comment': 'Mentioned in patronymic'
            }
        ]
    }
    
    result = transform_p70_11_documents_referenced_person(data)
    
    person = result['cidoc:P67_refers_to'][0]
    
    # Verify all properties preserved
    assert person['gmn:P1_1_has_name'] == 'Giovanni Rossi', \
        "Name property should be preserved"
    assert person['rdfs:label'] == 'Giovanni Rossi (deceased father)', \
        "Label should be preserved"
    assert person['rdfs:comment'] == 'Mentioned in patronymic', \
        "Comment should be preserved"
    assert person['@type'] == 'cidoc:E21_Person', \
        "Type should be preserved"
    
    print("✓ Test passed: Person properties preserved")


def run_all_tests():
    """Run all P70.11 tests"""
    print("Running P70.11 Test Suite...")
    print("=" * 60)
    
    try:
        test_p70_11_single_person_uri()
        test_p70_11_multiple_persons_mixed()
        test_p70_11_no_property()
        test_p70_11_existing_p67_refers_to()
        test_p70_11_person_with_properties()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        return True
    except AssertionError as e:
        print(f"✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

def example_usage():
    """Demonstrate various usage patterns"""
    
    print("Example 1: Single referenced person")
    print("-" * 40)
    data1 = {
        '@id': 'contract:001',
        'gmn:P70_11_documents_referenced_person': ['person:giovanni']
    }
    result1 = transform_p70_11_documents_referenced_person(data1)
    print(f"Input:  {data1}")
    print(f"Output: {result1}")
    print()
    
    print("Example 2: Multiple referenced persons")
    print("-" * 40)
    data2 = {
        '@id': 'contract:002',
        'gmn:P70_11_documents_referenced_person': [
            {'@id': 'person:marco', 'rdfs:label': 'Marco'},
            'person:pietro'
        ]
    }
    result2 = transform_p70_11_documents_referenced_person(data2)
    print(f"Input:  {data2}")
    print(f"Output: {result2}")
    print()
    
    print("Example 3: No property (pass-through)")
    print("-" * 40)
    data3 = {
        '@id': 'contract:003',
        'gmn:P70_1_documents_seller': ['person:seller']
    }
    result3 = transform_p70_11_documents_referenced_person(data3)
    print(f"Input:  {data3}")
    print(f"Output: {result3}")
    print()


# ==============================================================================
# INTEGRATION TEST WITH FULL PIPELINE
# ==============================================================================

def test_full_pipeline_integration():
    """
    Test P70.11 integration with complete transformation pipeline
    
    This test verifies that P70.11 works correctly alongside other
    property transformations in the full transform_item() pipeline.
    """
    from gmn_to_cidoc_transform import transform_item
    
    data = {
        '@id': 'contract:full_test',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P1_1_has_name': 'Test Contract',
        'gmn:P70_1_documents_seller': ['person:seller'],
        'gmn:P70_2_documents_buyer': ['person:buyer'],
        'gmn:P70_11_documents_referenced_person': [
            'person:deceased_father',
            'person:neighbor'
        ],
        'gmn:P70_13_documents_referenced_place': ['place:venice']
    }
    
    result = transform_item(data)
    
    # Verify P70.11 was transformed
    assert 'gmn:P70_11_documents_referenced_person' not in result, \
        "P70.11 should be removed"
    assert 'cidoc:P67_refers_to' in result, \
        "P67_refers_to should exist"
    
    # Verify persons are in P67_refers_to
    persons = [e for e in result['cidoc:P67_refers_to'] 
               if e['@type'] == 'cidoc:E21_Person']
    assert len(persons) == 2, "Should have two persons"
    
    # Verify place is also in P67_refers_to (from P70.13)
    places = [e for e in result['cidoc:P67_refers_to'] 
              if e['@type'] == 'cidoc:E53_Place']
    assert len(places) == 1, "Should have one place"
    
    # Verify other transformations still work
    assert 'cidoc:P70_documents' in result, \
        "P70_documents should exist (from P70.1 and P70.2)"
    
    print("✓ Full pipeline integration test passed")


# ==============================================================================
# DEBUGGING UTILITIES
# ==============================================================================

def debug_transformation(data, verbose=True):
    """
    Debug helper to show step-by-step transformation
    
    Args:
        data: Input data dictionary
        verbose: If True, print detailed information
    """
    if verbose:
        print("=" * 60)
        print("DEBUG: P70.11 Transformation")
        print("=" * 60)
        print("\n1. Input data:")
        import json
        print(json.dumps(data, indent=2))
    
    # Check if property exists
    if 'gmn:P70_11_documents_referenced_person' not in data:
        if verbose:
            print("\n2. No P70.11 property found - skipping transformation")
        return data
    
    if verbose:
        print("\n2. P70.11 property found:")
        print(f"   Persons: {data['gmn:P70_11_documents_referenced_person']}")
        print(f"   Count: {len(data['gmn:P70_11_documents_referenced_person'])}")
    
    # Perform transformation
    result = transform_p70_11_documents_referenced_person(data)
    
    if verbose:
        print("\n3. Transformation complete:")
        print(f"   P67_refers_to created: {'cidoc:P67_refers_to' in result}")
        if 'cidoc:P67_refers_to' in result:
            print(f"   P67_refers_to count: {len(result['cidoc:P67_refers_to'])}")
        print(f"   P70.11 removed: {'gmn:P70_11_documents_referenced_person' not in result}")
        
        print("\n4. Output data:")
        print(json.dumps(result, indent=2))
        print("=" * 60)
    
    return result


# ==============================================================================
# PERFORMANCE BENCHMARKING
# ==============================================================================

def benchmark_transformation(num_persons=100, iterations=1000):
    """
    Benchmark transformation performance
    
    Args:
        num_persons: Number of persons to include in test
        iterations: Number of times to run transformation
    """
    import time
    
    # Create test data with many persons
    data = {
        '@id': 'contract:benchmark',
        'gmn:P70_11_documents_referenced_person': [
            f'person:{i}' for i in range(num_persons)
        ]
    }
    
    # Run benchmark
    start_time = time.time()
    for _ in range(iterations):
        # Reset data for each iteration
        test_data = data.copy()
        transform_p70_11_documents_referenced_person(test_data)
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    avg_time = total_time / iterations
    persons_per_sec = (num_persons * iterations) / total_time
    
    print(f"Benchmark Results:")
    print(f"  Persons per document: {num_persons}")
    print(f"  Iterations: {iterations}")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average per iteration: {avg_time*1000:.3f}ms")
    print(f"  Persons processed per second: {persons_per_sec:.0f}")


# ==============================================================================
# MAIN EXECUTION (for testing)
# ==============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Run tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == 'examples':
        # Show examples
        example_usage()
    elif len(sys.argv) > 1 and sys.argv[1] == 'benchmark':
        # Run benchmark
        benchmark_transformation()
    else:
        # Default: show usage
        print("Usage:")
        print("  python documents-referenced-person-transform.py test       # Run tests")
        print("  python documents-referenced-person-transform.py examples   # Show examples")
        print("  python documents-referenced-person-transform.py benchmark  # Run benchmark")


# End of Python Additions File
