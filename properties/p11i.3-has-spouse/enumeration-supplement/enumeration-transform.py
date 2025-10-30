# Enhanced Python Transformation for Marriage Enumeration
# Replace the existing transform_p11i_3_has_spouse function with this version

# ============================================================================
# ENHANCED TRANSFORMATION FUNCTION
# ============================================================================

def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure with optional enumeration.
    
    Base transformation:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    
    With enumeration (when gmn:marriage_number_for_subject or gmn:marriage_number_for_spouse provided):
    P11i_participated_in > E5_Event > P140i_was_attributed_by > E13_Attribute_Assignment
                                   > P140_assigned_attribute_to > E21_Person
                                   > P141_assigned > integer
                                   > P177_assigned_property_of_type > P11_had_participant
    
    Args:
        data: Dictionary representing a JSON-LD entity with potential spouse information
    
    Returns:
        Dictionary with transformed CIDOC-CRM compliant structure
    
    Features:
        - Backward compatible: works with or without enumeration
        - Handles partial enumeration (subject only, spouse only, or both)
        - Generates unique URIs for E13_Attribute_Assignment nodes
        - Cleans up enumeration properties from spouse data
    
    Example Input:
        {
            "@id": "person:giovanni",
            "gmn:P11i_3_has_spouse": [
                {
                    "@id": "person:maria",
                    "gmn:marriage_number_for_subject": 2,
                    "gmn:marriage_number_for_spouse": 1
                }
            ]
        }
    
    Example Output:
        {
            "@id": "person:giovanni",
            "cidoc:P11i_participated_in": [
                {
                    "@id": "person:giovanni/event/marriage_abc123",
                    "@type": "cidoc:E5_Event",
                    "cidoc:P2_has_type": {...},
                    "cidoc:P11_had_participant": [...],
                    "cidoc:P140i_was_attributed_by": [
                        {
                            "@id": "person:giovanni/event/marriage_abc123/attribution_def456",
                            "@type": "cidoc:E13_Attribute_Assignment",
                            "cidoc:P140_assigned_attribute_to": {"@id": "person:giovanni"},
                            "cidoc:P141_assigned": {"@value": "2", "@type": "xsd:integer"},
                            "cidoc:P177_assigned_property_of_type": {"@id": "cidoc:P11_had_participant"}
                        },
                        {
                            "@id": "person:giovanni/event/marriage_abc123/attribution_xyz789",
                            "@type": "cidoc:E13_Attribute_Assignment",
                            "cidoc:P140_assigned_attribute_to": {"@id": "person:maria"},
                            "cidoc:P141_assigned": {"@value": "1", "@type": "xsd:integer"},
                            "cidoc:P177_assigned_property_of_type": {"@id": "cidoc:P11_had_participant"}
                        }
                    ]
                }
            ]
        }
    """
    # Check if the property exists in the data
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    # Extract spouse list and subject URI
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Initialize P11i_participated_in array if it doesn't exist
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    # Process each spouse
    for spouse_obj in spouses:
        # Handle both dictionary and string formats
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
            
            # Extract enumeration data if present
            subject_marriage_num = spouse_obj.get('gmn:marriage_number_for_subject')
            spouse_marriage_num = spouse_obj.get('gmn:marriage_number_for_spouse')
            
            # Remove enumeration properties from spouse_data
            # These are not attributes of the person entity itself
            spouse_data.pop('gmn:marriage_number_for_subject', None)
            spouse_data.pop('gmn:marriage_number_for_spouse', None)
        else:
            # String format: just the spouse URI
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
            subject_marriage_num = None
            spouse_marriage_num = None
        
        # Generate unique event URI using hash
        event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        event_uri = f"{subject_uri}/event/marriage_{event_hash}"
        
        # Create base marriage event structure
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [spouse_data]
        }
        
        # Add E13_Attribute_Assignment nodes for marriage enumeration if provided
        # Only create attribution array if at least one enumeration is provided
        if subject_marriage_num is not None or spouse_marriage_num is not None:
            event['cidoc:P140i_was_attributed_by'] = []
            
            # Create attribution for subject's marriage number
            if subject_marriage_num is not None:
                # Generate unique URI for subject attribution
                subject_hash = str(hash(subject_uri))[-8:]
                subject_attr_uri = f"{event_uri}/attribution_{subject_hash}"
                
                subject_attribution = {
                    '@id': subject_attr_uri,
                    '@type': 'cidoc:E13_Attribute_Assignment',
                    'cidoc:P140_assigned_attribute_to': {
                        '@id': subject_uri,
                        '@type': 'cidoc:E21_Person'
                    },
                    'cidoc:P141_assigned': {
                        '@value': str(subject_marriage_num),
                        '@type': 'xsd:integer'
                    },
                    'cidoc:P177_assigned_property_of_type': {
                        '@id': 'cidoc:P11_had_participant'
                    }
                }
                event['cidoc:P140i_was_attributed_by'].append(subject_attribution)
            
            # Create attribution for spouse's marriage number
            if spouse_marriage_num is not None:
                # Generate unique URI for spouse attribution
                spouse_hash = str(hash(spouse_uri))[-8:]
                spouse_attr_uri = f"{event_uri}/attribution_{spouse_hash}"
                
                spouse_attribution = {
                    '@id': spouse_attr_uri,
                    '@type': 'cidoc:E13_Attribute_Assignment',
                    'cidoc:P140_assigned_attribute_to': {
                        '@id': spouse_uri,
                        '@type': 'cidoc:E21_Person'
                    },
                    'cidoc:P141_assigned': {
                        '@value': str(spouse_marriage_num),
                        '@type': 'xsd:integer'
                    },
                    'cidoc:P177_assigned_property_of_type': {
                        '@id': 'cidoc:P11_had_participant'
                    }
                }
                event['cidoc:P140i_was_attributed_by'].append(spouse_attribution)
        
        # Add event to participation list
        data['cidoc:P11i_participated_in'].append(event)
    
    # Remove the simplified property
    del data['gmn:P11i_3_has_spouse']
    return data

# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================
#
# 1. Locate the existing transform_p11i_3_has_spouse() function in 
#    gmn_to_cidoc_transform.py (around line 200-300)
#
# 2. REPLACE the entire function with this enhanced version
#
# 3. NO CHANGES needed to:
#    - Function registration in transform_item()
#    - Import statements
#    - AAT_MARRIAGE constant
#
# 4. The enhanced function is BACKWARD COMPATIBLE:
#    - Marriages without enumeration still work
#    - Partial enumeration (subject only or spouse only) works
#    - Full enumeration (both) works
#
# ============================================================================
# TESTING
# ============================================================================
#
# Test with various input formats:
#
# Test 1: Full enumeration
# {
#   "gmn:P11i_3_has_spouse": [
#     {
#       "@id": "person:spouse",
#       "gmn:marriage_number_for_subject": 2,
#       "gmn:marriage_number_for_spouse": 1
#     }
#   ]
# }
# Expected: Event with 2 E13_Attribute_Assignment nodes
#
# Test 2: Subject enumeration only
# {
#   "gmn:P11i_3_has_spouse": [
#     {
#       "@id": "person:spouse",
#       "gmn:marriage_number_for_subject": 1
#     }
#   ]
# }
# Expected: Event with 1 E13_Attribute_Assignment node
#
# Test 3: No enumeration (backward compatibility)
# {
#   "gmn:P11i_3_has_spouse": [
#     {"@id": "person:spouse"}
#   ]
# }
# Expected: Event with no P140i_was_attributed_by property
#
# Test 4: Multiple marriages
# {
#   "gmn:P11i_3_has_spouse": [
#     {
#       "@id": "person:spouse1",
#       "gmn:marriage_number_for_subject": 1
#     },
#     {
#       "@id": "person:spouse2",
#       "gmn:marriage_number_for_subject": 2
#     }
#   ]
# }
# Expected: 2 separate events, each with its own attribution
#
# ============================================================================
# FUNCTION BEHAVIOR
# ============================================================================
#
# Input Handling:
# - Accepts both dictionary and string spouse formats
# - Extracts enumeration properties from spouse object
# - Cleans enumeration properties before adding spouse to event
#
# URI Generation:
# - Event URI: {subject_uri}/event/marriage_{hash}
# - Subject attribution URI: {event_uri}/attribution_{subject_hash}
# - Spouse attribution URI: {event_uri}/attribution_{spouse_hash}
#
# Enumeration Handling:
# - Both properties are optional
# - Can specify one, both, or neither
# - Uses "is not None" check to handle 0 values correctly
# - Converts to string for JSON-LD xsd:integer typing
#
# Backward Compatibility:
# - Marriages without enumeration work exactly as before
# - No P140i_was_attributed_by array created if no enumeration
# - Existing data continues to transform correctly
#
# ============================================================================
# ERROR HANDLING
# ============================================================================
#
# The function handles:
# - Missing gmn:P11i_3_has_spouse property (returns unchanged)
# - Missing @id on subject (generates UUID)
# - String spouse values (creates minimal person structure)
# - Dictionary spouse values (preserves all attributes except enumeration)
# - Missing enumeration properties (works without them)
# - Zero enumeration values (treated as valid ordinal)
# - Multiple spouses (each processed independently)
#
# ============================================================================
# PERFORMANCE NOTES
# ============================================================================
#
# Complexity: O(n) where n = number of spouses
# Additional nodes per marriage with full enumeration: 2 (E13 nodes)
# Storage overhead: ~300-400 bytes per enumerated marriage
#
# For large datasets:
# - Hash computation is O(1) average case
# - No database queries or external calls
# - Suitable for batch processing
#
# ============================================================================
# RELATED FUNCTIONS
# ============================================================================
#
# This function works with:
# - transform_p11i_1_earliest_attestation_date() (person attestation)
# - transform_p11i_2_latest_attestation_date() (person attestation)
# - transform_p96_1_has_mother() (family relationships)
# - transform_p97_1_has_father() (family relationships)
#
# All person participation events accumulate in cidoc:P11i_participated_in
#
# ============================================================================
