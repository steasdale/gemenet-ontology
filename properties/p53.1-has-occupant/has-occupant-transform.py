# Python Additions for gmn:P53_1_has_occupant Transformation
# Ready-to-copy code for gmn_to_cidoc_transform.py

# ==============================================================================
# TRANSFORMATION FUNCTION
# ==============================================================================
# Insert this function after transform_p22_1_has_owner() in the script

def transform_p53_1_has_occupant(data):
    """
    Transform gmn:P53_1_has_occupant to full CIDOC-CRM structure:
    P53_has_former_or_current_location > E21_Person
    
    The building's location serves as a place where persons reside.
    This captures occupation/residence relationships that are distinct from ownership.
    
    Args:
        data: Dictionary containing item data with potential gmn:P53_1_has_occupant property
    
    Returns:
        Modified data dictionary with CIDOC-CRM compliant structure
    
    Example Input:
        {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": [
                {"@id": "person456", "@type": "cidoc:E21_Person"}
            ]
        }
    
    Example Output:
        {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "cidoc:P53_has_former_or_current_location": [
                {"@id": "person456", "@type": "cidoc:E21_Person"}
            ]
        }
    """
    # Check if property exists in data
    if 'gmn:P53_1_has_occupant' not in data:
        return data
    
    # Get list of occupants
    occupants = data['gmn:P53_1_has_occupant']
    
    # Initialize CIDOC-CRM property if not present
    if 'cidoc:P53_has_former_or_current_location' not in data:
        data['cidoc:P53_has_former_or_current_location'] = []
    
    # Process each occupant
    for occupant_obj in occupants:
        if isinstance(occupant_obj, dict):
            # Occupant is a dictionary object - copy and ensure type
            occupant_data = occupant_obj.copy()
            if '@type' not in occupant_data:
                occupant_data['@type'] = 'cidoc:E21_Person'
        else:
            # Occupant is a URI string - create proper structure
            occupant_uri = str(occupant_obj)
            occupant_data = {
                '@id': occupant_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        # Add occupant to CIDOC-CRM property
        data['cidoc:P53_has_former_or_current_location'].append(occupant_data)
    
    # Remove shortcut property
    del data['gmn:P53_1_has_occupant']
    return data


# ==============================================================================
# INTEGRATION INTO TRANSFORM_ITEM PIPELINE
# ==============================================================================
# Add this function call in the transform_item() function pipeline
# Location: After transform_p22_1_has_owner() call

# Find this section in transform_item():
#     # Property ownership and occupation
#     item = transform_p22_1_has_owner(item)

# Add this line immediately after:
#     item = transform_p53_1_has_occupant(item)

# Complete context:
def transform_item(data, include_internal=False):
    """Transform a single item from GMN shortcuts to CIDOC-CRM."""
    # ... earlier transformations ...
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)  # <-- ADD THIS LINE
    
    # Family relationships
    item = transform_p96_1_has_mother(item)
    # ... later transformations ...


# ==============================================================================
# UNIT TESTS (optional but recommended)
# ==============================================================================

import unittest
import json

class TestOccupantTransformation(unittest.TestCase):
    """Unit tests for P53.1 has occupant transformation."""
    
    def test_single_occupant_dict_format(self):
        """Test transformation with single occupant in dict format."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": [
                {"@id": "person456", "@type": "cidoc:E21_Person"}
            ]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        # Check shortcut property removed
        self.assertNotIn("gmn:P53_1_has_occupant", result)
        
        # Check CIDOC property added
        self.assertIn("cidoc:P53_has_former_or_current_location", result)
        
        # Check occupant preserved
        occupants = result["cidoc:P53_has_former_or_current_location"]
        self.assertEqual(len(occupants), 1)
        self.assertEqual(occupants[0]["@id"], "person456")
        self.assertEqual(occupants[0]["@type"], "cidoc:E21_Person")
    
    def test_single_occupant_string_format(self):
        """Test transformation with single occupant as URI string."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": ["person456"]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        occupants = result["cidoc:P53_has_former_or_current_location"]
        self.assertEqual(len(occupants), 1)
        self.assertEqual(occupants[0]["@id"], "person456")
        self.assertEqual(occupants[0]["@type"], "cidoc:E21_Person")
    
    def test_multiple_occupants(self):
        """Test transformation with multiple occupants."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": [
                {"@id": "person1"},
                {"@id": "person2"},
                {"@id": "person3"}
            ]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        occupants = result["cidoc:P53_has_former_or_current_location"]
        self.assertEqual(len(occupants), 3)
        
        # Check all occupants present
        occupant_ids = [occ["@id"] for occ in occupants]
        self.assertIn("person1", occupant_ids)
        self.assertIn("person2", occupant_ids)
        self.assertIn("person3", occupant_ids)
    
    def test_no_occupant_property(self):
        """Test that data without occupant property passes through unchanged."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P1_1_has_name": [{"@value": "Test Building"}]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        # Should return unchanged
        self.assertEqual(result, input_data)
    
    def test_empty_occupant_list(self):
        """Test transformation with empty occupant list."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": []
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        # Shortcut property should be removed
        self.assertNotIn("gmn:P53_1_has_occupant", result)
        
        # CIDOC property should exist but be empty
        self.assertIn("cidoc:P53_has_former_or_current_location", result)
        self.assertEqual(len(result["cidoc:P53_has_former_or_current_location"]), 0)
    
    def test_preserves_other_properties(self):
        """Test that transformation preserves other building properties."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P1_1_has_name": [{"@value": "Palazzo Medici"}],
            "gmn:P22_1_has_owner": [{"@id": "owner789"}],
            "gmn:P53_1_has_occupant": [{"@id": "person456"}]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        # Other properties should remain
        self.assertIn("gmn:P1_1_has_name", result)
        self.assertIn("gmn:P22_1_has_owner", result)
        self.assertEqual(result["gmn:P1_1_has_name"][0]["@value"], "Palazzo Medici")
    
    def test_occupant_without_type(self):
        """Test that missing @type is added correctly."""
        input_data = {
            "@id": "building123",
            "@type": "gmn:E22_1_Building",
            "gmn:P53_1_has_occupant": [
                {"@id": "person456"}  # No @type
            ]
        }
        
        result = transform_p53_1_has_occupant(input_data)
        
        occupants = result["cidoc:P53_has_former_or_current_location"]
        self.assertEqual(occupants[0]["@type"], "cidoc:E21_Person")


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

# Example 1: Simple usage
def example_simple():
    """Example of basic transformation."""
    data = {
        "@id": "http://example.org/building/palace",
        "@type": "gmn:E22_1_Building",
        "gmn:P53_1_has_occupant": [
            {"@id": "http://example.org/person/lorenzo"}
        ]
    }
    
    result = transform_p53_1_has_occupant(data)
    print(json.dumps(result, indent=2))


# Example 2: Processing a full export file
def example_process_file():
    """Example of processing a complete JSON-LD file."""
    # Read input file
    with open('input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single items and arrays
    if isinstance(data, list):
        transformed = [transform_p53_1_has_occupant(item) for item in data]
    elif isinstance(data, dict) and '@graph' in data:
        data['@graph'] = [transform_p53_1_has_occupant(item) for item in data['@graph']]
        transformed = data
    else:
        transformed = transform_p53_1_has_occupant(data)
    
    # Write output file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)


# Example 3: Debug mode with logging
def transform_p53_1_has_occupant_debug(data, verbose=False):
    """Debug version with detailed logging."""
    if verbose:
        print(f"DEBUG: Processing item: {data.get('@id', 'unknown')}")
    
    if 'gmn:P53_1_has_occupant' not in data:
        if verbose:
            print("DEBUG: No occupant property found")
        return data
    
    occupants = data['gmn:P53_1_has_occupant']
    if verbose:
        print(f"DEBUG: Found {len(occupants)} occupant(s)")
    
    if 'cidoc:P53_has_former_or_current_location' not in data:
        data['cidoc:P53_has_former_or_current_location'] = []
    
    for i, occupant_obj in enumerate(occupants):
        if verbose:
            print(f"DEBUG: Processing occupant {i+1}/{len(occupants)}")
        
        if isinstance(occupant_obj, dict):
            occupant_data = occupant_obj.copy()
            if '@type' not in occupant_data:
                occupant_data['@type'] = 'cidoc:E21_Person'
                if verbose:
                    print(f"DEBUG: Added missing @type for occupant {i+1}")
        else:
            occupant_uri = str(occupant_obj)
            occupant_data = {
                '@id': occupant_uri,
                '@type': 'cidoc:E21_Person'
            }
            if verbose:
                print(f"DEBUG: Created structure for string URI occupant {i+1}")
        
        data['cidoc:P53_has_former_or_current_location'].append(occupant_data)
    
    del data['gmn:P53_1_has_occupant']
    if verbose:
        print("DEBUG: Transformation complete")
    
    return data


# ==============================================================================
# ERROR HANDLING (enhanced version)
# ==============================================================================

def transform_p53_1_has_occupant_safe(data):
    """
    Enhanced version with comprehensive error handling.
    Use this version if you want robust error recovery.
    """
    try:
        # Check if property exists
        if 'gmn:P53_1_has_occupant' not in data:
            return data
        
        occupants = data['gmn:P53_1_has_occupant']
        
        # Validate occupants is a list
        if not isinstance(occupants, list):
            print(f"Warning: gmn:P53_1_has_occupant is not a list for {data.get('@id', 'unknown')}")
            occupants = [occupants]  # Convert to list
        
        # Initialize CIDOC-CRM property
        if 'cidoc:P53_has_former_or_current_location' not in data:
            data['cidoc:P53_has_former_or_current_location'] = []
        
        # Process each occupant with error handling
        for occupant_obj in occupants:
            try:
                if isinstance(occupant_obj, dict):
                    occupant_data = occupant_obj.copy()
                    if '@type' not in occupant_data:
                        occupant_data['@type'] = 'cidoc:E21_Person'
                    
                    # Validate @id present
                    if '@id' not in occupant_data:
                        print(f"Warning: Occupant missing @id for {data.get('@id', 'unknown')}")
                        continue
                else:
                    occupant_uri = str(occupant_obj)
                    if not occupant_uri:
                        print(f"Warning: Empty occupant URI for {data.get('@id', 'unknown')}")
                        continue
                    occupant_data = {
                        '@id': occupant_uri,
                        '@type': 'cidoc:E21_Person'
                    }
                
                data['cidoc:P53_has_former_or_current_location'].append(occupant_data)
            
            except Exception as e:
                print(f"Error processing occupant: {e}")
                continue
        
        # Remove shortcut property
        del data['gmn:P53_1_has_occupant']
        
    except Exception as e:
        print(f"Error in transform_p53_1_has_occupant: {e}")
        # Return data unchanged on error
        return data
    
    return data


# ==============================================================================
# PERFORMANCE METRICS (optional)
# ==============================================================================

import time

def transform_p53_1_has_occupant_timed(data):
    """Version with performance timing."""
    start_time = time.time()
    
    result = transform_p53_1_has_occupant(data)
    
    elapsed = time.time() - start_time
    if elapsed > 0.1:  # Log if takes more than 100ms
        print(f"Warning: Slow transformation ({elapsed:.3f}s) for {data.get('@id', 'unknown')}")
    
    return result


# ==============================================================================
# VALIDATION HELPER
# ==============================================================================

def validate_occupant_transformation(original, transformed):
    """
    Validate that transformation was successful.
    
    Args:
        original: Original data before transformation
        transformed: Transformed data
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check shortcut property removed
    if 'gmn:P53_1_has_occupant' in transformed:
        errors.append("Shortcut property not removed")
    
    # Check CIDOC property added
    if 'cidoc:P53_has_former_or_current_location' not in transformed:
        if 'gmn:P53_1_has_occupant' in original:
            errors.append("CIDOC property not added")
    
    # Check occupant count matches
    if 'gmn:P53_1_has_occupant' in original:
        original_count = len(original['gmn:P53_1_has_occupant'])
        transformed_count = len(transformed.get('cidoc:P53_has_former_or_current_location', []))
        
        if original_count != transformed_count:
            errors.append(f"Occupant count mismatch: {original_count} -> {transformed_count}")
    
    # Check all occupants have @type
    if 'cidoc:P53_has_former_or_current_location' in transformed:
        for i, occ in enumerate(transformed['cidoc:P53_has_former_or_current_location']):
            if '@type' not in occ:
                errors.append(f"Occupant {i} missing @type")
            elif occ['@type'] != 'cidoc:E21_Person':
                errors.append(f"Occupant {i} has incorrect @type: {occ['@type']}")
    
    return (len(errors) == 0, errors)


# ==============================================================================
# DOCUMENTATION REFERENCES
# ==============================================================================

"""
Related Documentation:
- Ontology definition: gmn_ontology.ttl (search for P53_1_has_occupant)
- Implementation guide: has-occupant-implementation-guide.md
- Full documentation: has-occupant-documentation.md
- TTL snippets: has-occupant-ontology.ttl

CIDOC-CRM References:
- P53 has former or current location: http://www.cidoc-crm.org/Property/P53
- E21 Person: http://www.cidoc-crm.org/Entity/E21-Person
- E22 Human-Made Object: http://www.cidoc-crm.org/Entity/E22-Human-Made-Object

Property Relationships:
- Parent: cidoc:P53i_is_former_or_current_location_of
- Related: cidoc:P25_moved (move event property)
- Sibling: gmn:P22_1_has_owner (ownership property)
"""

# ==============================================================================
# END OF PYTHON ADDITIONS
# ==============================================================================
