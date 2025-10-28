# Python Additions for P70.22 Indicates Receiving Party
# Ready-to-Copy Code for gmn_to_cidoc_transform.py

# ============================================================================
# MAIN TRANSFORMATION FUNCTION
# ============================================================================
# Copy this entire function to gmn_to_cidoc_transform.py
# Replace the existing transform_p70_22_indicates_receiving_party function

from uuid import uuid4

# AAT Constants (add these near the top of the file with other constants)
AAT_TRANSFER_OF_RIGHTS = 'http://vocab.getty.edu/aat/300417639'
AAT_DECLARATIONS = 'http://vocab.getty.edu/aat/300027623'

def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    
    Handles multiple document types with different transformation paths:
    - Cessions: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    - Declarations: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    - Donations: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    - Dowries: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    
    Args:
        data (dict): The document data with gmn:P70_22_indicates_receiving_party property
        
    Returns:
        dict: Transformed data with full CIDOC-CRM structure
        
    Examples:
        Donation transformation:
        >>> data = {
        ...     '@id': 'http://example.org/donation001',
        ...     '@type': 'gmn:E31_7_Donation_Contract',
        ...     'gmn:P70_22_indicates_receiving_party': [
        ...         {'@id': 'http://example.org/person/maria'}
        ...     ]
        ... }
        >>> result = transform_p70_22_indicates_receiving_party(data)
        >>> 'cidoc:P70_documents' in result
        True
        >>> result['cidoc:P70_documents'][0]['@type']
        'cidoc:E8_Acquisition'
        
    Version: 1.0 (Updated 2025-10-28)
    """
    # Check if property exists
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    item_type = data.get('@type', '')
    
    # Determine document type
    # Handle both single type and list of types
    is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_4_Cession_of_Rights_Contract'
    is_declaration = 'gmn:E31_5_Declaration' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_5_Declaration'
    is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
    is_dowry = 'gmn:E31_8_Dowry_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_8_Dowry_Contract'
    
    # Process based on document type
    if is_donation or is_dowry:
        # For donations and dowries, use E8_Acquisition with P22_transferred_title_to
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            acquisition_uri = f"{subject_uri}/acquisition"
            data['cidoc:P70_documents'] = [{
                '@id': acquisition_uri,
                '@type': 'cidoc:E8_Acquisition'
            }]
        
        acquisition = data['cidoc:P70_documents'][0]
        
        # Initialize P22 property if not present
        if 'cidoc:P22_transferred_title_to' not in acquisition:
            acquisition['cidoc:P22_transferred_title_to'] = []
        
        # Add each receiving party
        for party_obj in receiving_parties:
            if isinstance(party_obj, dict):
                party_data = party_obj.copy()
                if '@type' not in party_data:
                    party_data['@type'] = 'cidoc:E39_Actor'
            else:
                party_uri = str(party_obj)
                party_data = {
                    '@id': party_uri,
                    '@type': 'cidoc:E39_Actor'
                }
            
            acquisition['cidoc:P22_transferred_title_to'].append(party_data)
    
    elif is_declaration:
        # For declarations, use E7_Activity with P01_has_domain
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/declaration"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_DECLARATIONS,
                    '@type': 'cidoc:E55_Type',
                    'rdfs:label': 'declarations'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        # Initialize P01 property if not present
        if 'cidoc:P01_has_domain' not in activity:
            activity['cidoc:P01_has_domain'] = []
        
        # Add each receiving party
        for party_obj in receiving_parties:
            if isinstance(party_obj, dict):
                party_data = party_obj.copy()
                if '@type' not in party_data:
                    party_data['@type'] = 'cidoc:E39_Actor'
            else:
                party_uri = str(party_obj)
                party_data = {
                    '@id': party_uri,
                    '@type': 'cidoc:E39_Actor'
                }
            
            activity['cidoc:P01_has_domain'].append(party_data)
    
    elif is_cession:
        # For cessions, use E7_Activity with P14_carried_out_by
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/cession"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_TRANSFER_OF_RIGHTS,
                    '@type': 'cidoc:E55_Type',
                    'rdfs:label': 'transfers of rights'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        # Initialize P14 property if not present
        if 'cidoc:P14_carried_out_by' not in activity:
            activity['cidoc:P14_carried_out_by'] = []
        
        # Add each receiving party
        for party_obj in receiving_parties:
            if isinstance(party_obj, dict):
                party_data = party_obj.copy()
                if '@type' not in party_data:
                    party_data['@type'] = 'cidoc:E39_Actor'
            else:
                party_uri = str(party_obj)
                party_data = {
                    '@id': party_uri,
                    '@type': 'cidoc:E39_Actor'
                }
            
            activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Remove the simplified property after transformation
    del data['gmn:P70_22_indicates_receiving_party']
    return data


# ============================================================================
# UPDATE TO transform_item() FUNCTION
# ============================================================================
# Ensure this function call is present in the transform_item() function
# Add it in the appropriate location with other P70 property transformations

def transform_item(item, include_internal=False):
    """Transform a single item, applying all transformation rules."""
    # ... existing code ...
    
    # P70.22 - Indicates receiving party (cessions, declarations, donations, dowries)
    item = transform_p70_22_indicates_receiving_party(item)
    
    # ... remaining transformations ...
    return item


# ============================================================================
# HELPER FUNCTIONS (OPTIONAL)
# ============================================================================
# These are optional utility functions that can be used to modularize the code

def _determine_document_type(item_type):
    """
    Determine the document type from @type value.
    
    Args:
        item_type: Either a string or list of type URIs
        
    Returns:
        str: One of 'cession', 'declaration', 'donation', 'dowry', or None
    """
    type_mappings = {
        'gmn:E31_4_Cession_of_Rights_Contract': 'cession',
        'gmn:E31_5_Declaration': 'declaration',
        'gmn:E31_7_Donation_Contract': 'donation',
        'gmn:E31_8_Dowry_Contract': 'dowry'
    }
    
    if isinstance(item_type, list):
        for t in item_type:
            if t in type_mappings:
                return type_mappings[t]
    elif item_type in type_mappings:
        return type_mappings[item_type]
    
    return None


def _normalize_actor(party_obj):
    """
    Normalize a party object to ensure it has proper structure and typing.
    
    Args:
        party_obj: Either a dict with actor data or a URI string
        
    Returns:
        dict: Normalized actor object with @id and @type
    """
    if isinstance(party_obj, dict):
        party_data = party_obj.copy()
        if '@type' not in party_data:
            party_data['@type'] = 'cidoc:E39_Actor'
    else:
        party_uri = str(party_obj)
        party_data = {
            '@id': party_uri,
            '@type': 'cidoc:E39_Actor'
        }
    return party_data


def _get_or_create_event_node(data, event_type, subject_uri):
    """
    Get existing event node or create a new one based on document type.
    
    Args:
        data (dict): Document data
        event_type (str): One of 'cession', 'declaration', 'donation', 'dowry'
        subject_uri (str): Base URI for generating event URI
        
    Returns:
        dict: Event node (E7_Activity or E8_Acquisition)
    """
    # Check if event node already exists
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        return data['cidoc:P70_documents'][0]
    
    # Create new event node based on type
    if event_type in ['donation', 'dowry']:
        event_uri = f"{subject_uri}/acquisition"
        event_node = {
            '@id': event_uri,
            '@type': 'cidoc:E8_Acquisition'
        }
    else:
        event_name = 'cession' if event_type == 'cession' else 'declaration'
        event_uri = f"{subject_uri}/{event_name}"
        event_node = {
            '@id': event_uri,
            '@type': 'cidoc:E7_Activity'
        }
        
        # Add appropriate type
        if event_type == 'cession':
            event_node['cidoc:P2_has_type'] = {
                '@id': AAT_TRANSFER_OF_RIGHTS,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'transfers of rights'
            }
        elif event_type == 'declaration':
            event_node['cidoc:P2_has_type'] = {
                '@id': AAT_DECLARATIONS,
                '@type': 'cidoc:E55_Type',
                'rdfs:label': 'declarations'
            }
    
    data['cidoc:P70_documents'] = [event_node]
    return event_node


# ============================================================================
# ALTERNATIVE IMPLEMENTATION USING HELPER FUNCTIONS
# ============================================================================
# This is a refactored version using the helper functions above
# Use this if you prefer more modular code

def transform_p70_22_indicates_receiving_party_modular(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    This is a modular version using helper functions.
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    item_type = data.get('@type', '')
    
    # Determine document type
    doc_type = _determine_document_type(item_type)
    if not doc_type:
        return data  # Unknown type, skip transformation
    
    # Get or create event node
    event_node = _get_or_create_event_node(data, doc_type, subject_uri)
    
    # Determine which property to use based on document type
    property_mappings = {
        'donation': 'cidoc:P22_transferred_title_to',
        'dowry': 'cidoc:P22_transferred_title_to',
        'declaration': 'cidoc:P01_has_domain',
        'cession': 'cidoc:P14_carried_out_by'
    }
    
    target_property = property_mappings[doc_type]
    
    # Initialize property if not present
    if target_property not in event_node:
        event_node[target_property] = []
    
    # Add each receiving party
    for party_obj in receiving_parties:
        party_data = _normalize_actor(party_obj)
        event_node[target_property].append(party_data)
    
    # Remove simplified property
    del data['gmn:P70_22_indicates_receiving_party']
    return data


# ============================================================================
# UNIT TESTS
# ============================================================================
# Copy these tests to a test file to verify the transformation works correctly

import unittest
import json

class TestP7022Transformation(unittest.TestCase):
    
    def test_donation_transformation(self):
        """Test that donations use E8_Acquisition with P22"""
        data = {
            '@id': 'http://test/doc1',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor1'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')
        self.assertIn('cidoc:P22_transferred_title_to', acquisition)
        self.assertEqual(len(acquisition['cidoc:P22_transferred_title_to']), 1)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_declaration_transformation(self):
        """Test that declarations use E7_Activity with P01"""
        data = {
            '@id': 'http://test/doc2',
            '@type': 'gmn:E31_5_Declaration',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor2'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        activity = result['cidoc:P70_documents'][0]
        self.assertEqual(activity['@type'], 'cidoc:E7_Activity')
        self.assertIn('cidoc:P01_has_domain', activity)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_cession_transformation(self):
        """Test that cessions use E7_Activity with P14"""
        data = {
            '@id': 'http://test/doc3',
            '@type': 'gmn:E31_4_Cession_of_Rights_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor3'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        activity = result['cidoc:P70_documents'][0]
        self.assertEqual(activity['@type'], 'cidoc:E7_Activity')
        self.assertIn('cidoc:P14_carried_out_by', activity)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_dowry_transformation(self):
        """Test that dowries use E8_Acquisition with P22"""
        data = {
            '@id': 'http://test/doc4',
            '@type': 'gmn:E31_8_Dowry_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor4'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')
        self.assertIn('cidoc:P22_transferred_title_to', acquisition)
        self.assertNotIn('gmn:P70_22_indicates_receiving_party', result)
    
    def test_multiple_receiving_parties(self):
        """Test handling of multiple receiving parties"""
        data = {
            '@id': 'http://test/doc5',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor5a'},
                {'@id': 'http://test/actor5b'},
                {'@id': 'http://test/actor5c'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(len(acquisition['cidoc:P22_transferred_title_to']), 3)
    
    def test_no_receiving_party(self):
        """Test that transformation is skipped when property is absent"""
        data = {
            '@id': 'http://test/doc6',
            '@type': 'gmn:E31_7_Donation_Contract'
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        # Should return unchanged
        self.assertEqual(data, result)
    
    def test_actor_type_added(self):
        """Test that E39_Actor type is added when missing"""
        data = {
            '@id': 'http://test/doc7',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor7'}  # No @type provided
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        acquisition = result['cidoc:P70_documents'][0]
        party = acquisition['cidoc:P22_transferred_title_to'][0]
        self.assertEqual(party['@type'], 'cidoc:E39_Actor')
    
    def test_uri_only_party(self):
        """Test transformation of URI-only (string) parties"""
        data = {
            '@id': 'http://test/doc8',
            '@type': 'gmn:E31_7_Donation_Contract',
            'gmn:P70_22_indicates_receiving_party': [
                'http://test/actor8'  # Just a URI string, not a dict
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        acquisition = result['cidoc:P70_documents'][0]
        party = acquisition['cidoc:P22_transferred_title_to'][0]
        self.assertEqual(party['@id'], 'http://test/actor8')
        self.assertEqual(party['@type'], 'cidoc:E39_Actor')
    
    def test_list_type_detection(self):
        """Test that type detection works with list of types"""
        data = {
            '@id': 'http://test/doc9',
            '@type': ['gmn:E31_7_Donation_Contract', 'gmn:E31_1_Notarial_Document'],
            'gmn:P70_22_indicates_receiving_party': [
                {'@id': 'http://test/actor9'}
            ]
        }
        result = transform_p70_22_indicates_receiving_party(data)
        
        self.assertIn('cidoc:P70_documents', result)
        acquisition = result['cidoc:P70_documents'][0]
        self.assertEqual(acquisition['@type'], 'cidoc:E8_Acquisition')


# Run tests
if __name__ == '__main__':
    unittest.main()


# ============================================================================
# INTEGRATION NOTES
# ============================================================================

"""
INTEGRATION CHECKLIST:

1. ADD AAT CONSTANTS at the top of gmn_to_cidoc_transform.py:
   AAT_TRANSFER_OF_RIGHTS = 'http://vocab.getty.edu/aat/300417639'
   AAT_DECLARATIONS = 'http://vocab.getty.edu/aat/300027623'

2. ENSURE uuid4 is imported:
   from uuid import uuid4

3. REPLACE or ADD the transform_p70_22_indicates_receiving_party function

4. UPDATE transform_item() to include:
   item = transform_p70_22_indicates_receiving_party(item)

5. VERIFY the transformation order:
   - Process related properties in logical order
   - P70.32 (donor) should be processed before or after P70.22
   - P70.33/P70.34 (objects) should be processed with P70.22
   - All should reference the same event node

6. TEST with sample data covering all four document types

7. VALIDATE output using SPARQL queries or RDF validator
"""

# ============================================================================
# END OF FILE
# ============================================================================
