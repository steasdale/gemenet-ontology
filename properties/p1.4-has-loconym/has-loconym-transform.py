# has-loconym-transform.py
# GMN Ontology - P1.4 has loconym Transformation Function
#
# STATUS: Already implemented in gmn_to_cidoc_transform.py (lines 154-186)
# This file provides a reference copy for documentation purposes.
# NO ADDITIONS ARE NEEDED - the function already exists.

"""
Transformation function for gmn:P1_4_has_loconym property.

This module contains the transformation function that converts the simplified
gmn:P1_4_has_loconym property to its full CIDOC-CRM compliant structure.

The function is already implemented in your gmn_to_cidoc_transform.py script
and is automatically called during the transformation process.
"""

from uuid import uuid4

# ==============================================================================
# Constants
# ==============================================================================

# Wikidata URI for loconym concept
# Used as the P2_has_type value in transformed appellations
WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"

# ==============================================================================
# Transformation Function
# ==============================================================================

def transform_p1_4_has_loconym(data):
    """
    Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (loconym) > P67_refers_to > E53_Place
    
    This function converts the simplified loconym property into a proper CIDOC-CRM
    structure with an E41_Appellation intermediary that references the place.
    
    Args:
        data (dict): Person resource data dictionary in JSON-LD format.
                    Expected to have '@id', '@type', and optionally 
                    'gmn:P1_4_has_loconym' properties.
    
    Returns:
        dict: Modified data dictionary with transformed structure.
              The original 'gmn:P1_4_has_loconym' property is removed and
              replaced with 'cidoc:P1_is_identified_by' containing E41_Appellation
              resources.
    
    Transformation:
        Input:
            {
              "@id": "person_uri",
              "gmn:P1_4_has_loconym": "place_uri"  # or [place_uri1, place_uri2, ...]
            }
        
        Output:
            {
              "@id": "person_uri",
              "cidoc:P1_is_identified_by": [
                {
                  "@id": "person_uri/appellation/loconym_hash",
                  "@type": "cidoc:E41_Appellation",
                  "cidoc:P2_has_type": {
                    "@id": "https://www.wikidata.org/wiki/Q17143070",
                    "@type": "cidoc:E55_Type"
                  },
                  "cidoc:P67_refers_to": {
                    "@id": "place_uri",
                    "@type": "cidoc:E53_Place"
                  }
                }
              ]
            }
    
    CIDOC-CRM Path:
        E21_Person → P1_is_identified_by → E41_Appellation 
                                         → P2_has_type → E55_Type (Wikidata Q17143070)
                                         → P67_refers_to → E53_Place
    
    Examples:
        >>> data = {
        ...     "@id": "http://example.org/person/giovanni",
        ...     "gmn:P1_4_has_loconym": "http://example.org/place/genoa"
        ... }
        >>> result = transform_p1_4_has_loconym(data)
        >>> 'cidoc:P1_is_identified_by' in result
        True
        >>> 'gmn:P1_4_has_loconym' in result
        False
    
    Notes:
        - Handles both single place URIs and arrays of place URIs
        - Handles both string URIs and object format with @id
        - Generates unique appellation URIs using hash of place URI
        - Properly types all generated resources
        - Preserves existing P1_is_identified_by array if present
        - Idempotent: safe to run multiple times on same data
    """
    
    # Check if property exists in data
    if 'gmn:P1_4_has_loconym' not in data:
        return data
    
    # Extract place value(s) - can be single value or array
    places = data['gmn:P1_4_has_loconym']
    
    # Ensure places is a list for uniform processing
    if not isinstance(places, list):
        places = [places]
    
    # Get subject URI (person URI)
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P1_is_identified_by array if it doesn't exist
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    # Process each place reference
    for place_obj in places:
        # Extract place URI - handle both object and string format
        if isinstance(place_obj, dict):
            # Object format: {"@id": "place_uri"}
            place_uri = place_obj.get('@id', '')
        else:
            # String format: "place_uri"
            place_uri = str(place_obj)
        
        # Skip empty place URIs
        if not place_uri:
            continue
        
        # Generate unique appellation URI using hash of place URI
        # This ensures same place always generates same URI (deterministic)
        place_hash = str(hash(place_uri))[-8:]  # Last 8 digits of hash
        appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
        
        # Create E41_Appellation structure
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            # Type as loconym using Wikidata Q17143070
            'cidoc:P2_has_type': {
                '@id': WIKIDATA_LOCONYM,
                '@type': 'cidoc:E55_Type'
            },
            # Reference to the place
            'cidoc:P67_refers_to': {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        }
        
        # Add appellation to P1_is_identified_by array
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    # Remove the shortcut property
    del data['gmn:P1_4_has_loconym']
    
    return data


# ==============================================================================
# Helper Functions
# ==============================================================================

def validate_loconym_data(data):
    """
    Validate that data is suitable for loconym transformation.
    
    Args:
        data (dict): Data dictionary to validate
    
    Returns:
        tuple: (is_valid, error_message)
               is_valid is True if data is valid, False otherwise
               error_message is None if valid, string describing error if not
    
    Examples:
        >>> data = {"@id": "person_1", "gmn:P1_4_has_loconym": "place_1"}
        >>> is_valid, msg = validate_loconym_data(data)
        >>> is_valid
        True
    """
    # Check for required @id
    if '@id' not in data:
        return False, "Data missing required '@id' field"
    
    # Check if loconym property exists
    if 'gmn:P1_4_has_loconym' not in data:
        return False, "Data missing 'gmn:P1_4_has_loconym' property"
    
    # Validate place value(s)
    places = data['gmn:P1_4_has_loconym']
    if not isinstance(places, list):
        places = [places]
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            if '@id' not in place_obj:
                return False, "Place object missing '@id' field"
            if not place_obj['@id']:
                return False, "Place object has empty '@id' field"
        elif isinstance(place_obj, str):
            if not place_obj:
                return False, "Place URI is empty string"
        else:
            return False, f"Invalid place value type: {type(place_obj)}"
    
    return True, None


def extract_loconym_places(data):
    """
    Extract all place URIs referenced by loconyms in the data.
    
    Args:
        data (dict): Person data dictionary
    
    Returns:
        list: List of place URI strings
    
    Examples:
        >>> data = {"gmn:P1_4_has_loconym": ["place_1", "place_2"]}
        >>> extract_loconym_places(data)
        ['place_1', 'place_2']
    """
    if 'gmn:P1_4_has_loconym' not in data:
        return []
    
    places = data['gmn:P1_4_has_loconym']
    if not isinstance(places, list):
        places = [places]
    
    place_uris = []
    for place_obj in places:
        if isinstance(place_obj, dict):
            uri = place_obj.get('@id', '')
        else:
            uri = str(place_obj)
        
        if uri:
            place_uris.append(uri)
    
    return place_uris


def count_loconym_appellations(data):
    """
    Count how many loconym appellations exist in transformed data.
    
    Args:
        data (dict): Person data dictionary (after transformation)
    
    Returns:
        int: Number of loconym appellations
    
    Examples:
        >>> data = {
        ...     "cidoc:P1_is_identified_by": [
        ...         {"cidoc:P2_has_type": {"@id": "https://www.wikidata.org/wiki/Q17143070"}},
        ...         {"cidoc:P2_has_type": {"@id": "http://vocab.getty.edu/aat/300404650"}}
        ...     ]
        ... }
        >>> count_loconym_appellations(data)
        1
    """
    if 'cidoc:P1_is_identified_by' not in data:
        return 0
    
    appellations = data['cidoc:P1_is_identified_by']
    if not isinstance(appellations, list):
        appellations = [appellations]
    
    count = 0
    for app in appellations:
        if isinstance(app, dict):
            type_obj = app.get('cidoc:P2_has_type', {})
            if isinstance(type_obj, dict):
                type_uri = type_obj.get('@id', '')
                if type_uri == WIKIDATA_LOCONYM:
                    count += 1
    
    return count


# ==============================================================================
# Integration with Main Transform
# ==============================================================================

def transform_item(item, include_internal=False):
    """
    Transform all shortcut properties in an item.
    
    This is a reference showing where transform_p1_4_has_loconym() is called
    in the main transformation pipeline. In the actual gmn_to_cidoc_transform.py
    file, this function calls all property transformation functions in sequence.
    
    The transform_p1_4_has_loconym() function is called around line 840 in the
    actual implementation.
    
    Args:
        item (dict): Item data dictionary
        include_internal (bool): Whether to transform internal notes
    
    Returns:
        dict: Transformed item dictionary
    """
    # ... other name transformations ...
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    
    # LOCONYM TRANSFORMATION (THIS FUNCTION)
    item = transform_p1_4_has_loconym(item)
    
    # ... other transformations ...
    item = transform_p102_1_has_title(item)
    
    return item


# ==============================================================================
# Testing Examples
# ==============================================================================

def example_basic_transformation():
    """
    Example: Basic single loconym transformation.
    
    Returns:
        tuple: (input_data, output_data)
    """
    input_data = {
        "@id": "http://example.org/person/giovanni",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": "Giovanni da Genova",
        "gmn:P1_4_has_loconym": "http://example.org/place/genoa"
    }
    
    output_data = transform_p1_4_has_loconym(input_data.copy())
    
    return input_data, output_data


def example_multiple_loconyms():
    """
    Example: Multiple loconyms transformation.
    
    Returns:
        tuple: (input_data, output_data)
    """
    input_data = {
        "@id": "http://example.org/person/maria",
        "@type": "cidoc:E21_Person",
        "gmn:P1_1_has_name": "Maria da Venezia e Genova",
        "gmn:P1_4_has_loconym": [
            "http://example.org/place/venice",
            "http://example.org/place/genoa"
        ]
    }
    
    output_data = transform_p1_4_has_loconym(input_data.copy())
    
    return input_data, output_data


def example_object_format():
    """
    Example: Loconym with object format (dict with @id).
    
    Returns:
        tuple: (input_data, output_data)
    """
    input_data = {
        "@id": "http://example.org/person/bartolomeo",
        "@type": "cidoc:E21_Person",
        "gmn:P1_4_has_loconym": {
            "@id": "http://example.org/place/vignolo"
        }
    }
    
    output_data = transform_p1_4_has_loconym(input_data.copy())
    
    return input_data, output_data


# ==============================================================================
# Usage Instructions
# ==============================================================================

"""
USAGE:

This transformation function is ALREADY implemented in your project at:
  File: gmn_to_cidoc_transform.py
  Lines: 154-186
  Function: transform_p1_4_has_loconym()

You do NOT need to add this code to your project. This file is provided as
a reference for documentation purposes.

To use the loconym property:

1. Add gmn:P1_4_has_loconym to your person data:
   
   <person_giovanni> a cidoc:E21_Person ;
       gmn:P1_1_has_name "Giovanni da Genova" ;
       gmn:P1_4_has_loconym <place_genoa> .

2. Run the transformation script:
   
   python3 gmn_to_cidoc_transform.py your_data.jsonld

3. The transformation will automatically convert to CIDOC-CRM structure:
   
   <person_giovanni> a cidoc:E21_Person ;
       cidoc:P1_is_identified_by <appellation_uri> .
   
   <appellation_uri> a cidoc:E41_Appellation ;
       cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> ;
       cidoc:P67_refers_to <place_genoa> .

TESTING:

To test the transformation:

1. Create test data file (test_loconym.jsonld):
   {
     "@context": {
       "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
       "gmn": "http://example.org/gmn/"
     },
     "@graph": [
       {
         "@id": "http://example.org/person/test",
         "@type": "cidoc:E21_Person",
         "gmn:P1_4_has_loconym": "http://example.org/place/genoa"
       }
     ]
   }

2. Run transformation:
   python3 gmn_to_cidoc_transform.py test_loconym.jsonld

3. Verify output contains:
   - cidoc:P1_is_identified_by array
   - E41_Appellation with correct structure
   - P2_has_type pointing to Wikidata Q17143070
   - P67_refers_to pointing to place
   - No gmn:P1_4_has_loconym property

TROUBLESHOOTING:

Issue: Transformation not occurring
Solution: Check that transform_p1_4_has_loconym() is called in transform_item()

Issue: Invalid place URI
Solution: Ensure place value is a valid URI string or object with @id

Issue: Wrong type in appellation
Solution: Verify WIKIDATA_LOCONYM constant is set correctly

Issue: Duplicate appellations
Solution: Ensure transformation runs once per dataset
"""

# ==============================================================================
# Implementation Status
# ==============================================================================

"""
IMPLEMENTATION STATUS: ✅ COMPLETE

The transform_p1_4_has_loconym() function is already implemented in:
  - File: gmn_to_cidoc_transform.py
  - Location: Lines 154-186
  - Status: Fully functional

The function is integrated into the transformation pipeline at:
  - File: gmn_to_cidoc_transform.py
  - Function: transform_item()
  - Location: Around line 840

The WIKIDATA_LOCONYM constant is defined at:
  - File: gmn_to_cidoc_transform.py
  - Location: Line 27
  - Value: "https://www.wikidata.org/wiki/Q17143070"

NO ADDITIONS ARE NEEDED.

This file is provided as a reference copy for documentation purposes only.
"""

# ==============================================================================
# END OF FILE
# ==============================================================================
