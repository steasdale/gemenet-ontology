# Python Additions for gmn:P70_8_documents_broker Transformation
# Ready-to-copy code for gmn_to_cidoc_transform.py

# =============================================================================
# CONSTANT DEFINITION
# =============================================================================
# Add this to the AAT constants section near the top of the file
# (if not already present)

AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"


# =============================================================================
# MAIN TRANSFORMATION FUNCTION
# =============================================================================
# Insert this function after transform_p70_7_documents_buyers_guarantor()

def transform_p70_8_documents_broker(data):
    """
    Transform gmn:P70_8_documents_broker to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person (with role)
    
    Args:
        data: Dictionary containing the item data with potential gmn:P70_8_documents_broker property
    
    Returns:
        Transformed data dictionary with broker information expanded to CIDOC-CRM structure
    
    The transformation creates this structure:
        E31_Document (Sales Contract)
          └─ P70_documents
              └─ E8_Acquisition
                  └─ P14_carried_out_by
                      └─ E21_Person (Broker)
                          └─ P14.1_in_the_role_of
                              └─ E55_Type (AAT: brokers)
    
    Example:
        Input:
            {
                "@id": "contract_001",
                "gmn:P70_8_documents_broker": [
                    {"@id": "person_giovanni", "rdfs:label": "Giovanni broker"}
                ]
            }
        
        Output:
            {
                "@id": "contract_001",
                "cidoc:P70_documents": [{
                    "@id": "contract_001/acquisition",
                    "@type": "cidoc:E8_Acquisition",
                    "cidoc:P14_carried_out_by": [{
                        "@id": "person_giovanni",
                        "@type": "cidoc:E21_Person",
                        "rdfs:label": "Giovanni broker",
                        "cidoc:P14.1_in_the_role_of": {
                            "@id": "http://vocab.getty.edu/page/aat/300025234",
                            "@type": "cidoc:E55_Type"
                        }
                    }]
                }]
            }
    
    Note:
        Unlike procurators and guarantors, brokers are attached directly to the
        acquisition via P14_carried_out_by without an intermediate E7_Activity
        or P17_was_motivated_by link, because brokers facilitate the transaction
        for both parties equally rather than representing one specific party.
    """
    # Check if the property exists in the data
    if 'gmn:P70_8_documents_broker' not in data:
        return data
    
    # Extract broker information
    brokers = data['gmn:P70_8_documents_broker']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Ensure P70_documents acquisition exists
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    # Get reference to the acquisition
    acquisition = data['cidoc:P70_documents'][0]
    
    # Ensure P14_carried_out_by list exists
    if 'cidoc:P14_carried_out_by' not in acquisition:
        acquisition['cidoc:P14_carried_out_by'] = []
    
    # Process each broker
    for broker_obj in brokers:
        # Handle both dictionary and string URI formats
        if isinstance(broker_obj, dict):
            broker_data = broker_obj.copy()
            # Ensure type is set
            if '@type' not in broker_data:
                broker_data['@type'] = 'cidoc:E21_Person'
        else:
            # String URI case
            broker_uri = str(broker_obj)
            broker_data = {
                '@id': broker_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add broker role from Getty AAT
        broker_data['cidoc:P14.1_in_the_role_of'] = {
            '@id': AAT_BROKER,
            '@type': 'cidoc:E55_Type'
        }
        
        # Add broker to acquisition
        acquisition['cidoc:P14_carried_out_by'].append(broker_data)
    
    # Remove the simplified property
    del data['gmn:P70_8_documents_broker']
    
    return data


# =============================================================================
# INTEGRATION INTO MAIN PIPELINE
# =============================================================================
# Add this line to the transform_item() function in the P70 transformations section
# (after transform_p70_7_documents_buyers_guarantor call)

# In the transform_item() function:
#
# def transform_item(item, include_internal=False):
#     """Transform all shortcut properties in an item to CIDOC-CRM structure."""
#     
#     # ... other transformations ...
#     
#     # Sales contract properties (P70.1-P70.17)
#     item = transform_p70_1_documents_seller(item)
#     item = transform_p70_2_documents_buyer(item)
#     item = transform_p70_3_documents_transfer_of(item)
#     item = transform_p70_4_documents_sellers_procurator(item)
#     item = transform_p70_5_documents_buyers_procurator(item)
#     item = transform_p70_6_documents_sellers_guarantor(item)
#     item = transform_p70_7_documents_buyers_guarantor(item)
#     item = transform_p70_8_documents_broker(item)  # ← ADD THIS LINE
#     item = transform_p70_9_documents_payment_provider_for_buyer(item)
#     # ... remaining transformations ...
#     
#     return item


# =============================================================================
# ALTERNATIVE: COMPACT VERSION
# =============================================================================
# Shorter version with less documentation if preferred

def transform_p70_8_documents_broker(data):
    """Transform gmn:P70_8_documents_broker to CIDOC-CRM structure."""
    if 'gmn:P70_8_documents_broker' not in data:
        return data
    
    brokers = data['gmn:P70_8_documents_broker']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P14_carried_out_by' not in acquisition:
        acquisition['cidoc:P14_carried_out_by'] = []
    
    for broker_obj in brokers:
        if isinstance(broker_obj, dict):
            broker_data = broker_obj.copy()
            if '@type' not in broker_data:
                broker_data['@type'] = 'cidoc:E21_Person'
        else:
            broker_uri = str(broker_obj)
            broker_data = {
                '@id': broker_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        broker_data['cidoc:P14.1_in_the_role_of'] = {
            '@id': AAT_BROKER,
            '@type': 'cidoc:E55_Type'
        }
        
        acquisition['cidoc:P14_carried_out_by'].append(broker_data)
    
    del data['gmn:P70_8_documents_broker']
    return data


# =============================================================================
# UNIT TESTS
# =============================================================================
# Add these tests to your test suite (e.g., test_gmn_transform.py)

import unittest
import json
from uuid import uuid4

class TestBrokerTransformation(unittest.TestCase):
    """Test cases for gmn:P70_8_documents_broker transformation."""
    
    def test_single_broker(self):
        """Test transformation of single broker."""
        input_data = {
            '@id': 'http://example.org/contract/001',
            '@type': 'gmn:E31_2_Sales_Contract',
            'gmn:P70_8_documents_broker': [
                {
                    '@id': 'http://example.org/person/broker',
                    'rdfs:label': 'Giovanni Broker'
                }
            ]
        }
        
        result = transform_p70_8_documents_broker(input_data)
        
        # Check that simplified property is removed
        self.assertNotIn('gmn:P70_8_documents_broker', result)
        
        # Check that P70_documents exists
        self.assertIn('cidoc:P70_documents', result)
        
        # Check acquisition structure
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')
        
        # Check broker in P14_carried_out_by
        self.assertIn('cidoc:P14_carried_out_by', acquisition)
        brokers = acquisition['cidoc:P14_carried_out_by']
        self.assertEqual(len(brokers), 1)
        
        # Check broker details
        broker = brokers[0]
        self.assertEqual(broker['@id'], 'http://example.org/person/broker')
        self.assertEqual(broker['@type'], 'cidoc:E21_Person')
        self.assertEqual(broker['rdfs:label'], 'Giovanni Broker')
        
        # Check role
        self.assertIn('cidoc:P14.1_in_the_role_of', broker)
        role = broker['cidoc:P14.1_in_the_role_of']
        self.assertEqual(role['@id'], AAT_BROKER)
        self.assertEqual(role['@type'], 'cidoc:E55_Type')
    
    def test_multiple_brokers(self):
        """Test transformation of multiple brokers."""
        input_data = {
            '@id': 'http://example.org/contract/002',
            '@type': 'gmn:E31_2_Sales_Contract',
            'gmn:P70_8_documents_broker': [
                {'@id': 'http://example.org/person/broker1', 'rdfs:label': 'Giovanni'},
                {'@id': 'http://example.org/person/broker2', 'rdfs:label': 'Marco'}
            ]
        }
        
        result = transform_p70_8_documents_broker(input_data)
        
        # Check both brokers are present
        acquisition = result['cidoc:P70_documents'][0]
        brokers = acquisition['cidoc:P14_carried_out_by']
        self.assertEqual(len(brokers), 2)
        
        # Check both have correct role
        for broker in brokers:
            self.assertEqual(
                broker['cidoc:P14.1_in_the_role_of']['@id'],
                AAT_BROKER
            )
    
    def test_broker_with_string_uri(self):
        """Test transformation when broker is specified as string URI."""
        input_data = {
            '@id': 'http://example.org/contract/003',
            'gmn:P70_8_documents_broker': ['http://example.org/person/broker']
        }
        
        result = transform_p70_8_documents_broker(input_data)
        
        acquisition = result['cidoc:P70_documents'][0]
        broker = acquisition['cidoc:P14_carried_out_by'][0]
        
        # Check that URI is preserved and type is added
        self.assertEqual(broker['@id'], 'http://example.org/person/broker')
        self.assertEqual(broker['@type'], 'cidoc:E21_Person')
        self.assertIn('cidoc:P14.1_in_the_role_of', broker)
    
    def test_no_broker_property(self):
        """Test that data without broker property passes through unchanged."""
        input_data = {
            '@id': 'http://example.org/contract/004',
            '@type': 'gmn:E31_2_Sales_Contract'
        }
        
        result = transform_p70_8_documents_broker(input_data)
        
        # Should be identical to input
        self.assertEqual(result, input_data)
    
    def test_integration_with_existing_acquisition(self):
        """Test broker addition to existing acquisition structure."""
        input_data = {
            '@id': 'http://example.org/contract/005',
            'cidoc:P70_documents': [{
                '@id': 'http://example.org/contract/005/acquisition',
                '@type': 'cidoc:E8_Acquisition',
                'cidoc:P23_transferred_title_from': {
                    '@id': 'http://example.org/person/seller'
                }
            }],
            'gmn:P70_8_documents_broker': [
                {'@id': 'http://example.org/person/broker'}
            ]
        }
        
        result = transform_p70_8_documents_broker(input_data)
        
        acquisition = result['cidoc:P70_documents'][0]
        
        # Check that existing properties are preserved
        self.assertIn('cidoc:P23_transferred_title_from', acquisition)
        
        # Check that broker is added
        self.assertIn('cidoc:P14_carried_out_by', acquisition)
        broker = acquisition['cidoc:P14_carried_out_by'][0]
        self.assertEqual(broker['@id'], 'http://example.org/person/broker')


# =============================================================================
# DEBUG HELPER FUNCTION
# =============================================================================
# Add this function to help debug transformation issues

def debug_broker_transformation(data, verbose=True):
    """
    Helper function to debug broker transformation.
    
    Args:
        data: Input data dictionary
        verbose: If True, print detailed debug information
    
    Returns:
        Transformed data
    """
    if verbose:
        print("=" * 80)
        print("DEBUG: Broker Transformation")
        print("=" * 80)
        print(f"\nInput data keys: {list(data.keys())}")
        
        if 'gmn:P70_8_documents_broker' in data:
            brokers = data['gmn:P70_8_documents_broker']
            print(f"\nFound {len(brokers)} broker(s):")
            for i, broker in enumerate(brokers):
                print(f"  Broker {i+1}: {broker}")
        else:
            print("\nNo broker property found in input")
        
        print("\nTransforming...")
    
    result = transform_p70_8_documents_broker(data)
    
    if verbose:
        print("\nOutput data keys:", list(result.keys()))
        
        if 'cidoc:P70_documents' in result:
            acquisition = result['cidoc:P70_documents'][0]
            print(f"\nAcquisition keys: {list(acquisition.keys())}")
            
            if 'cidoc:P14_carried_out_by' in acquisition:
                brokers = acquisition['cidoc:P14_carried_out_by']
                print(f"\nTransformed {len(brokers)} broker(s):")
                for i, broker in enumerate(brokers):
                    print(f"  Broker {i+1}:")
                    print(f"    ID: {broker.get('@id')}")
                    print(f"    Type: {broker.get('@type')}")
                    print(f"    Label: {broker.get('rdfs:label', 'N/A')}")
                    role = broker.get('cidoc:P14.1_in_the_role_of', {})
                    print(f"    Role: {role.get('@id', 'N/A')}")
        
        print("\n" + "=" * 80)
    
    return result


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example 1: Simple broker transformation
    example_data = {
        '@id': 'http://example.org/contract/example',
        '@type': 'gmn:E31_2_Sales_Contract',
        'gmn:P70_8_documents_broker': [
            {
                '@id': 'http://example.org/person/giovanni_broker',
                'rdfs:label': 'Giovanni de Sancto Petro, sensale'
            }
        ]
    }
    
    print("Example 1: Simple Broker Transformation")
    print("-" * 80)
    print("\nInput:")
    print(json.dumps(example_data, indent=2))
    
    result = transform_p70_8_documents_broker(example_data)
    
    print("\nOutput:")
    print(json.dumps(result, indent=2))
    
    # Example 2: Multiple brokers
    example_data_2 = {
        '@id': 'http://example.org/contract/example2',
        'gmn:P70_8_documents_broker': [
            {'@id': 'http://example.org/person/broker1', 'rdfs:label': 'Giovanni'},
            {'@id': 'http://example.org/person/broker2', 'rdfs:label': 'Marco'}
        ]
    }
    
    print("\n\nExample 2: Multiple Brokers")
    print("-" * 80)
    print("\nInput:")
    print(json.dumps(example_data_2, indent=2))
    
    result_2 = transform_p70_8_documents_broker(example_data_2)
    
    print("\nOutput:")
    print(json.dumps(result_2, indent=2))


# =============================================================================
# NOTES FOR DEVELOPERS
# =============================================================================

# 1. FUNCTION PLACEMENT
#    Place this function in gmn_to_cidoc_transform.py after the
#    transform_p70_7_documents_buyers_guarantor() function

# 2. CONSTANT DEFINITION
#    Ensure AAT_BROKER constant is defined at the top of the file:
#    AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"

# 3. INTEGRATION
#    Add the function call to transform_item():
#    item = transform_p70_8_documents_broker(item)

# 4. IMPORTS
#    Required imports:
#    - from uuid import uuid4
#    - import json (for testing)

# 5. ERROR HANDLING
#    The function handles:
#    - Missing property (returns data unchanged)
#    - Empty broker list
#    - Both dict and string URI formats
#    - Missing acquisition structure (creates it)
#    - Multiple brokers

# 6. TESTING
#    Run unit tests before deployment:
#    python -m pytest test_gmn_transform.py::TestBrokerTransformation

# 7. DEBUGGING
#    Use debug_broker_transformation() for troubleshooting:
#    debug_broker_transformation(data, verbose=True)

# 8. PERFORMANCE
#    Function has O(n) complexity where n = number of brokers
#    Typical case: n = 1, worst case: n < 10

# =============================================================================
# END OF PYTHON ADDITIONS
# =============================================================================
