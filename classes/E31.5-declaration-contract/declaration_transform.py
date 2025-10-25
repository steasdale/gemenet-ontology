#!/usr/bin/env python3
"""
E31.5 Declaration - Transformation Functions
Add these to gmn_to_cidoc_transform_script.py
"""

# =============================================================================
# CONSTANT DEFINITION - Add at top of script with other AAT constants
# =============================================================================

# Getty AAT URI for declarations
AAT_DECLARATION = "http://vocab.getty.edu/page/aat/300027623"


# =============================================================================
# TRANSFORMATION FUNCTIONS - Add these functions to the script
# =============================================================================

def transform_p70_24_indicates_declarant(data):
    """
    Transform gmn:P70_24_indicates_declarant to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_24_indicates_declarant' not in data:
        return data
    
    declarants = data['gmn:P70_24_indicates_declarant']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if declaration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing declaration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new declaration activity
        activity_uri = f"{subject_uri}/declaration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Add declarants to declaration activity
    for declarant_obj in declarants:
        # Handle both URI references and full objects
        if isinstance(declarant_obj, dict):
            declarant_data = declarant_obj.copy()
            if '@type' not in declarant_data:
                declarant_data['@type'] = 'cidoc:E39_Actor'
        else:
            declarant_uri = str(declarant_obj)
            declarant_data = {
                '@id': declarant_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        # Add to declaration activity
        existing_activity['cidoc:P14_carried_out_by'].append(declarant_data)
    
    # Remove shortcut property
    del data['gmn:P70_24_indicates_declarant']
    
    return data


def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    
    Handles two different document types:
    - For E31_4_Cession_of_Rights_Contract: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    - For E31_5_Declaration: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    
    NOTE: This function REPLACES the existing transform_p70_22_indicates_receiving_party function.
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Determine document type to decide which property to use
    is_declaration = False
    is_cession = False
    
    if '@type' in data:
        types = data['@type'] if isinstance(data['@type'], list) else [data['@type']]
        is_declaration = 'gmn:E31_5_Declaration' in types
        is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in types
    
    # Check if activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new activity with appropriate type
        activity_uri = f"{subject_uri}/{'declaration' if is_declaration else 'cession'}"
        activity_type = AAT_DECLARATION if is_declaration else AAT_TRANSFER_OF_RIGHTS
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': activity_type,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # For declarations, use P01_has_domain
    # For cessions, use P14_carried_out_by (both parties actively carry out the cession)
    property_key = 'cidoc:P01_has_domain' if is_declaration else 'cidoc:P14_carried_out_by'
    
    # Initialize property if it doesn't exist
    if property_key not in existing_activity:
        existing_activity[property_key] = []
    
    # Add receiving parties
    for party_obj in receiving_parties:
        # Handle both URI references and full objects
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
        
        # Add to activity
        existing_activity[property_key].append(party_data)
    
    # Remove shortcut property
    del data['gmn:P70_22_indicates_receiving_party']
    
    return data


def transform_p70_25_indicates_declaration_subject(data):
    """
    Transform gmn:P70_25_indicates_declaration_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    Args:
        data: The item data dictionary
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P70_25_indicates_declaration_subject' not in data:
        return data
    
    subjects = data['gmn:P70_25_indicates_declaration_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Check if declaration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing declaration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new declaration activity
        activity_uri = f"{subject_uri}/declaration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_DECLARATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Initialize P16 if it doesn't exist
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Add declaration subjects
    for subject_obj in subjects:
        # Handle both URI references and full objects
        if isinstance(subject_obj, dict):
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            subj_uri = str(subject_obj)
            subject_data = {
                '@id': subj_uri,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to declaration activity
        existing_activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Remove shortcut property
    del data['gmn:P70_25_indicates_declaration_subject']
    
    return data


# =============================================================================
# UPDATE TO transform_item() FUNCTION
# Find this function in the script and update it as shown below
# =============================================================================

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    """
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p102_1_has_title(item)
    item = transform_p94i_1_was_created_by(item)
    item = transform_p94i_2_has_enactment_date(item)
    item = transform_p94i_3_has_place_of_enactment(item)
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
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    item = transform_p70_21_indicates_conceding_party(item)
    # CRITICAL: P70.22 MUST be called AFTER P70.21 (conceding party) and P70.24 (declarant)
    # so that the activity type is already set when determining which property to use
    item = transform_p70_24_indicates_declarant(item)
    item = transform_p70_22_indicates_receiving_party(item)
    item = transform_p70_23_indicates_object_of_cession(item)
    item = transform_p70_25_indicates_declaration_subject(item)
    item = transform_p138i_1_has_representation(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    item = transform_p96_1_has_mother(item)
    item = transform_p97_1_has_father(item)
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    return item


# =============================================================================
# IMPLEMENTATION NOTES
# =============================================================================
"""
CRITICAL IMPLEMENTATION REQUIREMENTS:

1. ADD AAT CONSTANT:
   - Add AAT_DECLARATION constant at the top of the script with other AAT URIs
   
2. ADD THREE NEW FUNCTIONS:
   - transform_p70_24_indicates_declarant()
   - transform_p70_25_indicates_declaration_subject()
   
3. REPLACE EXISTING FUNCTION:
   - Replace the existing transform_p70_22_indicates_receiving_party() function
     with the updated version provided above
   
4. UPDATE transform_item():
   - Add the three transformation function calls in the correct order
   - IMPORTANT: P70.24 must come BEFORE P70.22
   - IMPORTANT: P70.22 must come AFTER both P70.21 and P70.24

5. TRANSFORMATION ORDER:
   The order is critical because transform_p70_22_indicates_receiving_party()
   needs to detect the document type, which is easier when the activity has
   already been created by P70.24 (for declarations) or P70.21 (for cessions).

6. SHARED ACTIVITY:
   All three properties (P70.24, P70.22, P70.25) check for and reuse the same
   E7_Activity node, ensuring proper semantic structure.

7. ACTIVITY TYPING:
   The E7_Activity is automatically typed as AAT 300027623 (declarations) when
   created by any of the declaration transformation functions.
"""

# =============================================================================
# END OF DECLARATION TRANSFORMATION ADDITIONS
# =============================================================================