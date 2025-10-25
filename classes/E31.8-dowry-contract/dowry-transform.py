#!/usr/bin/env python3
"""
Dowry Contract Transformation Functions
To be added to gmn_to_cidoc_transform.py
"""

def transform_p70_34_indicates_object_of_dowry(data):
    """
    Transform gmn:P70_34_indicates_object_of_dowry to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_34_indicates_object_of_dowry' not in data:
        return data
    
    objects = data['gmn:P70_34_indicates_object_of_dowry']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P24_transferred_title_of' not in acquisition:
        acquisition['cidoc:P24_transferred_title_of'] = []
    
    for obj_obj in objects:
        if isinstance(obj_obj, dict):
            obj_data = obj_obj.copy()
            if '@type' not in obj_data:
                obj_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            obj_uri = str(obj_obj)
            obj_data = {
                '@id': obj_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        acquisition['cidoc:P24_transferred_title_of'].append(obj_data)
    
    del data['gmn:P70_34_indicates_object_of_dowry']
    return data


def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    For cessions: P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    For declarations: P70_documents > E7_Activity > P01_has_domain > E39_Actor
    For donations: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    For dowries: P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    
    UPDATED VERSION - replaces existing function in gmn_to_cidoc_transform.py
    """
    if 'gmn:P70_22_indicates_receiving_party' not in data:
        return data
    
    receiving_parties = data['gmn:P70_22_indicates_receiving_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    item_type = data.get('@type', '')
    
    # Determine document type
    is_cession = 'gmn:E31_4_Cession_of_Rights_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_4_Cession_of_Rights_Contract'
    is_declaration = 'gmn:E31_5_Declaration' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_5_Declaration'
    is_donation = 'gmn:E31_7_Donation_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_7_Donation_Contract'
    is_dowry = 'gmn:E31_8_Dowry_Contract' in item_type if isinstance(item_type, list) else item_type == 'gmn:E31_8_Dowry_Contract'
    
    if is_donation or is_dowry:
        # For donations and dowries, use E8_Acquisition
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            acquisition_uri = f"{subject_uri}/acquisition"
            data['cidoc:P70_documents'] = [{
                '@id': acquisition_uri,
                '@type': 'cidoc:E8_Acquisition'
            }]
        
        acquisition = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P22_transferred_title_to' not in acquisition:
            acquisition['cidoc:P22_transferred_title_to'] = []
        
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
        # For declarations, use P01_has_domain
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/declaration"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_DECLARATION,
                    '@type': 'cidoc:E55_Type'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P01_has_domain' not in activity:
            activity['cidoc:P01_has_domain'] = []
        
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
        # For cessions, use P14_carried_out_by
        if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
            activity_uri = f"{subject_uri}/cession"
            data['cidoc:P70_documents'] = [{
                '@id': activity_uri,
                '@type': 'cidoc:E7_Activity',
                'cidoc:P2_has_type': {
                    '@id': AAT_TRANSFER_OF_RIGHTS,
                    '@type': 'cidoc:E55_Type'
                }
            }]
        
        activity = data['cidoc:P70_documents'][0]
        
        if 'cidoc:P14_carried_out_by' not in activity:
            activity['cidoc:P14_carried_out_by'] = []
        
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
    
    del data['gmn:P70_22_indicates_receiving_party']
    return data


# UPDATE TO transform_item() FUNCTION
# Add this line in the appropriate section:

def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    
    Returns:
        Transformed item dictionary
    """
    # Name and title properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    item = transform_p1_3_has_patrilineal_name(item)
    item = transform_p1_4_has_loconym(item)
    item = transform_p102_1_has_title(item)
    
    # Creation properties (notary, date, place)
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
    item = transform_p70_16_documents_sale_price_amount(item)
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # Arbitration properties (P70.18-P70.20)
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    
    # Cession properties (P70.21-P70.23)
    item = transform_p70_21_indicates_conceding_party(item)
    item = transform_p70_22_indicates_receiving_party(item)
    item = transform_p70_23_indicates_object_of_cession(item)
    
    # Declaration properties (P70.24-P70.25)
    item = transform_p70_24_indicates_declarant(item)
    item = transform_p70_25_indicates_declaration_subject(item)
    
    # Correspondence properties (P70.26-P70.31)
    item = transform_p70_26_indicates_sender(item)
    item = transform_p70_27_has_address_of_origin(item)
    item = transform_p70_28_indicates_addressee(item)
    item = transform_p70_29_describes_subject(item)
    item = transform_p70_30_mentions_person(item)
    item = transform_p70_31_has_address_of_destination(item)
    
    # Donation properties (P70.32-P70.33)
    item = transform_p70_32_indicates_donor(item)
    item = transform_p70_33_indicates_object_of_donation(item)
    
    # Dowry properties (P70.34) - ADD THIS LINE
    item = transform_p70_34_indicates_object_of_dowry(item)
    
    # Visual representation
    item = transform_p138i_1_has_representation(item)
    
    # Person attestation and relationship properties
    item = transform_p11i_1_earliest_attestation_date(item)
    item = transform_p11i_2_latest_attestation_date(item)
    item = transform_p11i_3_has_spouse(item)
    
    # Property ownership and occupation
    item = transform_p22_1_has_owner(item)
    item = transform_p53_1_has_occupant(item)
    
    # Family relationships
    item = transform_p96_1_has_mother(item)
    item = transform_p97_1_has_father(item)
    
    # Group memberships
    item = transform_p107i_1_has_regional_provenance(item)
    item = transform_p107i_2_has_social_category(item)
    item = transform_p107i_3_has_occupation(item)
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item


# UPDATE TO main() FUNCTION HELP TEXT
# Update the "Supported contract types" section to include:

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python gmn_to_cidoc_transform_script.py <input_file.json> <output_file.json> [--include-internal]")
        print("\nOptions:")
        print("  --include-internal    Include editorial notes in output (default: exclude)")
        print("\nExamples:")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json public_output.json")
        print("  python gmn_to_cidoc_transform_script.py omeka_export.json full_output.json --include-internal")
        print("\nSupported contract types:")
        print("  - gmn:E31_1_Contract (general contracts)")
        print("  - gmn:E31_2_Sales_Contract")
        print("  - gmn:E31_3_Arbitration_Agreement")
        print("  - gmn:E31_4_Cession_of_Rights_Contract")
        print("  - gmn:E31_5_Declaration")
        print("  - gmn:E31_6_Correspondence")
        print("  - gmn:E31_7_Donation_Contract")
        print("  - gmn:E31_8_Dowry_Contract")  # ADD THIS LINE
        sys.exit(1)
    
    # ... rest of main() function
