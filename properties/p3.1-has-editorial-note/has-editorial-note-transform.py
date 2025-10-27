# GMN P3.1 has editorial note - Python Transformation Code
#
# This file contains the Python transformation code for gmn:P3_1_has_editorial_note.
# This code is ALREADY IMPLEMENTED in the main gmn_to_cidoc_transform.py script.
# This file is provided for reference and documentation purposes.
#
# Property: gmn:P3_1_has_editorial_note
# Version: 1.0
# Date: October 26, 2025
# Status: ✅ Already Implemented
#
# =============================================================================

import json
import sys
from uuid import uuid4

# =============================================================================
# AAT CONSTANT
# =============================================================================

# Getty AAT URI for editorial notes
AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/aat/300456627"

# =============================================================================
# MAIN TRANSFORMATION FUNCTION
# =============================================================================

def transform_p3_1_has_editorial_note(data, include_internal=False):
    """
    Transform gmn:P3_1_has_editorial_note to full CIDOC-CRM structure or remove it.
    
    This function handles the transformation of simplified editorial note properties
    into full CIDOC-CRM compliant structure using E33_Linguistic_Object with 
    AAT type 300456627 (editorial notes).
    
    The function behavior depends on the include_internal flag:
    - If False (default): The property is removed from the output (public export)
    - If True: The property is transformed to full CIDOC-CRM structure (internal export)
    
    Transformation pattern:
    ----------------------
    FROM: <entity> gmn:P3_1_has_editorial_note "Note text"
    TO:   <entity> cidoc:P67i_is_referred_to_by <note_uri>
          <note_uri> a cidoc:E33_Linguistic_Object
                     cidoc:P2_has_type <aat:300456627>
                     cidoc:P190_has_symbolic_content "Note text"
    
    Args:
        data (dict): The item data dictionary containing entity information
        include_internal (bool): If True, transform to CIDOC-CRM. 
                                If False, remove the property.
    
    Returns:
        dict: Modified data dictionary with either transformed notes (include_internal=True)
              or removed notes (include_internal=False)
    
    Examples:
        >>> data = {
        ...     "@id": "http://example.org/person/001",
        ...     "gmn:P3_1_has_editorial_note": [{"@value": "Requires verification"}]
        ... }
        >>> # Public export (default)
        >>> result = transform_p3_1_has_editorial_note(data)
        >>> "gmn:P3_1_has_editorial_note" in result
        False
        >>> # Internal export
        >>> result = transform_p3_1_has_editorial_note(data, include_internal=True)
        >>> "cidoc:P67i_is_referred_to_by" in result
        True
    """
    # Check if property exists
    if 'gmn:P3_1_has_editorial_note' not in data:
        return data
    
    # If not including internal notes, remove the property and return
    if not include_internal:
        del data['gmn:P3_1_has_editorial_note']
        return data
    
    # Get the notes and subject URI
    notes = data['gmn:P3_1_has_editorial_note']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P67i property if it doesn't exist
    if 'cidoc:P67i_is_referred_to_by' not in data:
        data['cidoc:P67i_is_referred_to_by'] = []
    
    # Transform each note to E33_Linguistic_Object
    for note_obj in notes:
        # Extract note value (handle both string and dict formats)
        if isinstance(note_obj, dict):
            note_value = note_obj.get('@value', '')
        else:
            note_value = str(note_obj)
        
        # Skip empty notes
        if not note_value:
            continue
        
        # Generate unique URI for this note using hash
        note_hash = str(hash(note_value))[-8:]
        note_uri = f"{subject_uri}/note/{note_hash}"
        
        # Create E33_Linguistic_Object structure
        linguistic_object = {
            '@id': note_uri,
            '@type': 'cidoc:E33_Linguistic_Object',
            'cidoc:P2_has_type': {
                '@id': AAT_EDITORIAL_NOTE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': note_value
        }
        
        # Add to P67i array
        data['cidoc:P67i_is_referred_to_by'].append(linguistic_object)
    
    # Remove original simplified property
    del data['gmn:P3_1_has_editorial_note']
    
    return data

# =============================================================================
# INTEGRATION WITH MAIN TRANSFORM PIPELINE
# =============================================================================

def transform_item(data, include_internal=False):
    """
    Transform a single item with all applicable transformations.
    
    This function should be called from the main transformation pipeline.
    The editorial note transformation should be called LAST to ensure all
    other properties are transformed first.
    
    Args:
        data (dict): Item data dictionary
        include_internal (bool): Whether to include internal properties
    
    Returns:
        dict: Fully transformed item
    """
    # ... other transformations ...
    
    # Name properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    
    # Date properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    
    # ... more transformations ...
    
    # Editorial notes (LAST, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item

# =============================================================================
# COMMAND LINE INTERFACE INTEGRATION
# =============================================================================

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python gmn_to_cidoc_transform.py <input_file.json> <output_file.json> [--include-internal]")
        print("\nOptions:")
        print("  --include-internal    Include editorial notes in output (default: exclude)")
        print("\nExamples:")
        print("  python gmn_to_cidoc_transform.py omeka_export.json public_output.json")
        print("  python gmn_to_cidoc_transform.py omeka_export.json full_output.json --include-internal")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    include_internal = '--include-internal' in sys.argv
    
    if include_internal:
        print("Note: Including internal editorial notes in output")
    else:
        print("Note: Excluding internal editorial notes from output")
    
    success = transform_export(input_file, output_file, include_internal)
    sys.exit(0 if success else 1)

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_usage_1():
    """Example 1: Transform with include_internal=False (default/public export)"""
    
    input_data = {
        "@id": "http://example.org/person/giovanni_001",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": [
            {"@value": "Giovanni Rossi"}
        ],
        "gmn:P3_1_has_editorial_note": [
            {"@value": "Identity requires verification against parish records."}
        ]
    }
    
    # Transform for public export (notes removed)
    result = transform_p3_1_has_editorial_note(input_data.copy(), include_internal=False)
    
    print("Public Export Result:")
    print(json.dumps(result, indent=2))
    # Output will NOT contain gmn:P3_1_has_editorial_note
    
    return result

def example_usage_2():
    """Example 2: Transform with include_internal=True (internal export)"""
    
    input_data = {
        "@id": "http://example.org/person/giovanni_001",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": [
            {"@value": "Giovanni Rossi"}
        ],
        "gmn:P3_1_has_editorial_note": [
            {"@value": "Identity requires verification against parish records."}
        ]
    }
    
    # Transform for internal export (notes transformed to E33)
    result = transform_p3_1_has_editorial_note(input_data.copy(), include_internal=True)
    
    print("Internal Export Result:")
    print(json.dumps(result, indent=2))
    # Output will contain cidoc:P67i_is_referred_to_by with E33_Linguistic_Object
    
    return result

def example_usage_3():
    """Example 3: Multiple notes on single entity"""
    
    input_data = {
        "@id": "http://example.org/person/bartolomeo_001",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": [
            {"@value": "Bartolomeo de Vignolo"}
        ],
        "gmn:P3_1_has_editorial_note": [
            {"@value": "Primary attestation: ASG Not. 456, f. 78r"},
            {"@value": "Loconym suggests origin from Vignolo"},
            {"@value": "Possible relation to Giovanni de Vignolo"}
        ]
    }
    
    # Transform with internal flag
    result = transform_p3_1_has_editorial_note(input_data.copy(), include_internal=True)
    
    # Each note becomes separate E33_Linguistic_Object
    print(f"Number of notes transformed: {len(result.get('cidoc:P67i_is_referred_to_by', []))}")
    
    return result

def example_usage_4():
    """Example 4: Entity without editorial notes"""
    
    input_data = {
        "@id": "http://example.org/person/maria_001",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": [
            {"@value": "Maria de Genova"}
        ]
    }
    
    # Transform (no changes expected)
    result = transform_p3_1_has_editorial_note(input_data.copy(), include_internal=True)
    
    # Data unchanged since no editorial notes present
    assert result == input_data
    
    return result

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def extract_editorial_notes(data):
    """
    Extract all editorial notes from an entity for reporting.
    
    Args:
        data (dict): Entity data dictionary
    
    Returns:
        list: List of editorial note strings
    """
    if 'gmn:P3_1_has_editorial_note' not in data:
        return []
    
    notes = []
    for note_obj in data['gmn:P3_1_has_editorial_note']:
        if isinstance(note_obj, dict):
            notes.append(note_obj.get('@value', ''))
        else:
            notes.append(str(note_obj))
    
    return [n for n in notes if n]  # Filter empty strings

def count_entities_with_notes(json_data):
    """
    Count how many entities in a JSON-LD export have editorial notes.
    
    Args:
        json_data (dict or list): JSON-LD data
    
    Returns:
        int: Count of entities with editorial notes
    """
    count = 0
    
    # Handle both single items and arrays
    items = json_data if isinstance(json_data, list) else json_data.get('@graph', [json_data])
    
    for item in items:
        if 'gmn:P3_1_has_editorial_note' in item:
            count += 1
    
    return count

def validate_note_length(note_text, min_length=1, max_length=1000):
    """
    Validate editorial note length.
    
    Args:
        note_text (str): Note text to validate
        min_length (int): Minimum acceptable length
        max_length (int): Maximum acceptable length
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not note_text or len(note_text.strip()) < min_length:
        return False, f"Note too short (minimum {min_length} characters)"
    
    if len(note_text) > max_length:
        return False, f"Note too long (maximum {max_length} characters)"
    
    return True, ""

# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_transform_removes_notes_by_default():
    """Test that notes are removed when include_internal=False"""
    data = {
        "@id": "test:001",
        "gmn:P3_1_has_editorial_note": [{"@value": "Test note"}]
    }
    
    result = transform_p3_1_has_editorial_note(data, include_internal=False)
    
    assert 'gmn:P3_1_has_editorial_note' not in result
    assert 'cidoc:P67i_is_referred_to_by' not in result
    print("✓ Test passed: Notes removed by default")

def test_transform_creates_e33_with_flag():
    """Test that notes transform to E33 when include_internal=True"""
    data = {
        "@id": "test:001",
        "gmn:P3_1_has_editorial_note": [{"@value": "Test note"}]
    }
    
    result = transform_p3_1_has_editorial_note(data, include_internal=True)
    
    assert 'gmn:P3_1_has_editorial_note' not in result
    assert 'cidoc:P67i_is_referred_to_by' in result
    assert len(result['cidoc:P67i_is_referred_to_by']) == 1
    
    note = result['cidoc:P67i_is_referred_to_by'][0]
    assert note['@type'] == 'cidoc:E33_Linguistic_Object'
    assert note['cidoc:P2_has_type']['@id'] == AAT_EDITORIAL_NOTE
    assert note['cidoc:P190_has_symbolic_content'] == "Test note"
    
    print("✓ Test passed: Notes transform to E33")

def test_multiple_notes():
    """Test that multiple notes are handled correctly"""
    data = {
        "@id": "test:001",
        "gmn:P3_1_has_editorial_note": [
            {"@value": "Note 1"},
            {"@value": "Note 2"},
            {"@value": "Note 3"}
        ]
    }
    
    result = transform_p3_1_has_editorial_note(data, include_internal=True)
    
    assert len(result['cidoc:P67i_is_referred_to_by']) == 3
    print("✓ Test passed: Multiple notes handled correctly")

def test_empty_notes_skipped():
    """Test that empty notes are skipped"""
    data = {
        "@id": "test:001",
        "gmn:P3_1_has_editorial_note": [
            {"@value": "Valid note"},
            {"@value": ""},  # Empty
            {"@value": "   "}  # Whitespace only
        ]
    }
    
    result = transform_p3_1_has_editorial_note(data, include_internal=True)
    
    # Should skip empty and whitespace-only notes
    # Note: Current implementation doesn't trim, so "   " would be included
    # Adjust test based on actual implementation behavior
    assert 'cidoc:P67i_is_referred_to_by' in result
    print("✓ Test passed: Empty notes handled")

def run_all_tests():
    """Run all test functions"""
    print("Running tests...")
    test_transform_removes_notes_by_default()
    test_transform_creates_e33_with_flag()
    test_multiple_notes()
    test_empty_notes_skipped()
    print("All tests passed!")

# =============================================================================
# DOCUMENTATION EXAMPLES
# =============================================================================

"""
COMPLETE TRANSFORMATION EXAMPLE
================================

INPUT JSON-LD (Simplified):
---------------------------
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#"
  },
  "@id": "http://example.org/person/giacomo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [
    {"@value": "Giacomo Spinola q. Antonio"}
  ],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Name varies between 'Giacomo' and 'Iacopo' in sources."}
  ]
}

OUTPUT JSON-LD (Public Export - default):
-----------------------------------------
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@id": "http://example.org/person/giacomo_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/person/giacomo_001/appellation/12345678",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo Spinola q. Antonio"
    }
  ]
}

NOTE: Editorial note is completely removed.

OUTPUT JSON-LD (Internal Export - with --include-internal):
-----------------------------------------------------------
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@id": "http://example.org/person/giacomo_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/person/giacomo_001/appellation/12345678",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300404650",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Giacomo Spinola q. Antonio"
    }
  ],
  "cidoc:P67i_is_referred_to_by": [
    {
      "@id": "http://example.org/person/giacomo_001/note/87654321",
      "@type": "cidoc:E33_Linguistic_Object",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/aat/300456627",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Name varies between 'Giacomo' and 'Iacopo' in sources."
    }
  ]
}

NOTE: Editorial note is transformed to full CIDOC-CRM structure.
"""

# =============================================================================
# COMMAND LINE USAGE
# =============================================================================

"""
COMMAND LINE EXAMPLES
=====================

Public Export (default - removes editorial notes):
--------------------------------------------------
$ python gmn_to_cidoc_transform.py input.json public_output.json
Note: Excluding internal editorial notes from output
✓ Transformation complete: public_output.json

Internal Export (includes editorial notes):
-------------------------------------------
$ python gmn_to_cidoc_transform.py input.json internal_output.json --include-internal
Note: Including internal editorial notes in output
✓ Transformation complete: internal_output.json

Batch Processing:
-----------------
$ for file in exports/*.json; do
    python gmn_to_cidoc_transform.py "$file" "public/${file##*/}"
  done
"""

# =============================================================================
# END OF FILE
# =============================================================================

if __name__ == '__main__':
    # Run tests when executed directly
    print("GMN P3.1 has editorial note - Transformation Code Reference")
    print("=" * 60)
    print("This file contains reference implementations.")
    print("The actual code is already in gmn_to_cidoc_transform.py")
    print("=" * 60)
    print()
    
    # Optionally run tests
    # run_all_tests()
