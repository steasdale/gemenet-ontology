#!/usr/bin/env python3
"""
Transform GMN shortcut properties to full CIDOC-CRM compliant structure.

This script reads JSON-LD export from Omeka-S and transforms custom shortcut
properties (like gmn:P1_1_has_name) into their full CIDOC-CRM equivalents.

Updated to reflect expanded class hierarchy including:
- gmn:E31_1_Contract (general contract class)
- gmn:E31_2_Sales_Contract (specialized sales contract)
- gmn:E31_4_Cession_of_Rights_Contract
- gmn:E31_5_Declaration
- gmn:E31_6_Correspondence
- gmn:E31_7_Donation_Contract
"""

import json
import sys
from uuid import uuid4

# Getty AAT URI constants
AAT_NAME = "http://vocab.getty.edu/page/aat/300404650"
AAT_NAME_FROM_SOURCE = "http://vocab.getty.edu/page/aat/300456607"
AAT_PATRONYMIC = "http://vocab.getty.edu/page/aat/300404651"
AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/page/aat/300456627"
WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"
AAT_REGION = "http://vocab.getty.edu/page/aat/300055490"
AAT_MARRIAGE = "http://vocab.getty.edu/page/aat/300055475"
AAT_AGENT = "http://vocab.getty.edu/page/aat/300025972"
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"
AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"
AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
AAT_PAYEE = "http://vocab.getty.edu/page/aat/300386184"
AAT_TRANSFER_OF_RIGHTS = "http://vocab.getty.edu/page/aat/300417639"
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"
AAT_DECLARATION = "http://vocab.getty.edu/page/aat/300027623"
AAT_TRANSFER_OF_RIGHTS = "http://vocab.getty.edu/page/aat/300417639"
AAT_CORRESPONDENCE = "http://vocab.getty.edu/page/aat/300026877"


def generate_appellation_uri(subject_uri, name_value, suffix=""):
    """Generate a unique URI for an appellation resource."""
    name_hash = str(hash(name_value + suffix))[-8:]
    return f"{subject_uri}/appellation/{name_hash}"


def transform_name_property(data, property_name, aat_type_uri):
    """
    Generic function to transform name shortcut properties to full CIDOC-CRM structure.
    
    Args:
        data: The item data dictionary
        property_name: The shortcut property name (e.g., 'gmn:P1_1_has_name')
        aat_type_uri: The AAT URI for the type of name
    
    Returns:
        Modified data dictionary
    """
    if property_name not in data:
        return data
    
    names = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    for name_obj in names:
        if isinstance(name_obj, dict):
            name_value = name_obj.get('@value', '')
        else:
            name_value = str(name_obj)
        
        if not name_value:
            continue
        
        appellation_uri = generate_appellation_uri(subject_uri, name_value, property_name)
        
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': aat_type_uri,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': name_value
        }
        
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    del data[property_name]
    return data


def transform_p1_1_has_name(data):
    """Transform gmn:P1_1_has_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_1_has_name', AAT_NAME)


def transform_p1_2_has_name_from_source(data):
    """Transform gmn:P1_2_has_name_from_source to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_2_has_name_from_source', AAT_NAME_FROM_SOURCE)


def transform_p1_3_has_patrilineal_name(data):
    """Transform gmn:P1_3_has_patrilineal_name to full CIDOC-CRM structure."""
    return transform_name_property(data, 'gmn:P1_3_has_patrilineal_name', AAT_PATRONYMIC)


def transform_p1_4_has_loconym(data):
    """
    Transform gmn:P1_4_has_loconym to full CIDOC-CRM structure:
    P1_is_identified_by > E41_Appellation > P2_has_type (loconym) > P67_refers_to > E53_Place
    """
    if 'gmn:P1_4_has_loconym' not in data:
        return data
    
    places = data['gmn:P1_4_has_loconym']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P1_is_identified_by' not in data:
        data['cidoc:P1_is_identified_by'] = []
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            place_uri = place_obj.get('@id', '')
        else:
            place_uri = str(place_obj)
        
        place_hash = str(hash(place_uri))[-8:]
        appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
        
        appellation = {
            '@id': appellation_uri,
            '@type': 'cidoc:E41_Appellation',
            'cidoc:P2_has_type': {
                '@id': WIKIDATA_LOCONYM,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P67_refers_to': {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        }
        
        data['cidoc:P1_is_identified_by'].append(appellation)
    
    del data['gmn:P1_4_has_loconym']
    return data


def transform_p102_1_has_title(data):
    """
    Transform gmn:P102_1_has_title to full CIDOC-CRM structure:
    P102_has_title > E35_Title > P190_has_symbolic_content
    """
    if 'gmn:P102_1_has_title' not in data:
        return data
    
    titles = data['gmn:P102_1_has_title']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P102_has_title' not in data:
        data['cidoc:P102_has_title'] = []
    
    for title_obj in titles:
        if isinstance(title_obj, dict):
            title_value = title_obj.get('@value', '')
        else:
            title_value = str(title_obj)
        
        if not title_value:
            continue
        
        title_hash = str(hash(title_value))[-8:]
        title_uri = f"{subject_uri}/title/{title_hash}"
        
        title = {
            '@id': title_uri,
            '@type': 'cidoc:E35_Title',
            'cidoc:P190_has_symbolic_content': title_value
        }
        
        data['cidoc:P102_has_title'].append(title)
    
    del data['gmn:P102_1_has_title']
    return data


def transform_p3_1_has_editorial_note(data, include_internal=False):
    """
    Transform gmn:P3_1_has_editorial_note to full CIDOC-CRM structure or remove it.
    
    Args:
        data: The item data dictionary
        include_internal: If True, transform to CIDOC-CRM. If False, remove the property.
    
    Returns:
        Modified data dictionary
    """
    if 'gmn:P3_1_has_editorial_note' not in data:
        return data
    
    if not include_internal:
        del data['gmn:P3_1_has_editorial_note']
        return data
    
    notes = data['gmn:P3_1_has_editorial_note']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P67i_is_referred_to_by' not in data:
        data['cidoc:P67i_is_referred_to_by'] = []
    
    for note_obj in notes:
        if isinstance(note_obj, dict):
            note_value = note_obj.get('@value', '')
        else:
            note_value = str(note_obj)
        
        if not note_value:
            continue
        
        note_hash = str(hash(note_value))[-8:]
        note_uri = f"{subject_uri}/note/{note_hash}"
        
        linguistic_object = {
            '@id': note_uri,
            '@type': 'cidoc:E33_Linguistic_Object',
            'cidoc:P2_has_type': {
                '@id': AAT_EDITORIAL_NOTE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P190_has_symbolic_content': note_value
        }
        
        data['cidoc:P67i_is_referred_to_by'].append(linguistic_object)
    
    del data['gmn:P3_1_has_editorial_note']
    return data


def transform_p94i_1_was_created_by(data):
    """
    Transform gmn:P94i_1_was_created_by to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P14_carried_out_by > E21_Person
    """
    if 'gmn:P94i_1_was_created_by' not in data:
        return data
    
    creators = data['gmn:P94i_1_was_created_by']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    creation_uri = f"{subject_uri}/creation"
    creation = {
        '@id': creation_uri,
        '@type': 'cidoc:E65_Creation',
        'cidoc:P14_carried_out_by': []
    }
    
    for creator_obj in creators:
        if isinstance(creator_obj, dict):
            creator_data = creator_obj.copy()
            if '@type' not in creator_data:
                creator_data['@type'] = 'cidoc:E21_Person'
        else:
            creator_uri = str(creator_obj)
            creator_data = {
                '@id': creator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        creation['cidoc:P14_carried_out_by'].append(creator_data)
    
    data['cidoc:P94i_was_created_by'] = creation
    del data['gmn:P94i_1_was_created_by']
    return data


def transform_p94i_2_has_enactment_date(data):
    """
    Transform gmn:P94i_2_has_enactment_date to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P4_has_time-span > E52_Time-Span > P82_at_some_time_within
    """
    if 'gmn:P94i_2_has_enactment_date' not in data:
        return data
    
    dates = data['gmn:P94i_2_has_enactment_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P94i_was_created_by' not in data:
        creation_uri = f"{subject_uri}/creation"
        data['cidoc:P94i_was_created_by'] = {
            '@id': creation_uri,
            '@type': 'cidoc:E65_Creation'
        }
    
    creation = data['cidoc:P94i_was_created_by']
    
    for date_obj in dates:
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            continue
        
        timespan_uri = f"{creation['@id']}/timespan"
        timespan = {
            '@id': timespan_uri,
            '@type': 'cidoc:E52_Time-Span',
            'cidoc:P82_at_some_time_within': date_value
        }
        
        creation['cidoc:P4_has_time-span'] = timespan
    
    del data['gmn:P94i_2_has_enactment_date']
    return data


def transform_p94i_3_has_place_of_enactment(data):
    """
    Transform gmn:P94i_3_has_place_of_enactment to full CIDOC-CRM structure:
    P94i_was_created_by > E65_Creation > P7_took_place_at > E53_Place
    """
    if 'gmn:P94i_3_has_place_of_enactment' not in data:
        return data
    
    places = data['gmn:P94i_3_has_place_of_enactment']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P94i_was_created_by' not in data:
        creation_uri = f"{subject_uri}/creation"
        data['cidoc:P94i_was_created_by'] = {
            '@id': creation_uri,
            '@type': 'cidoc:E65_Creation'
        }
    
    creation = data['cidoc:P94i_was_created_by']
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        creation['cidoc:P7_took_place_at'] = place_data
    
    del data['gmn:P94i_3_has_place_of_enactment']
    return data


def transform_p70_1_documents_seller(data):
    """
    Transform gmn:P70_1_documents_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P23_transferred_title_from > E21_Person
    """
    if 'gmn:P70_1_documents_seller' not in data:
        return data
    
    sellers = data['gmn:P70_1_documents_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P23_transferred_title_from' not in acquisition:
        acquisition['cidoc:P23_transferred_title_from'] = []
    
    for seller_obj in sellers:
        if isinstance(seller_obj, dict):
            seller_data = seller_obj.copy()
            if '@type' not in seller_data:
                seller_data['@type'] = 'cidoc:E21_Person'
        else:
            seller_uri = str(seller_obj)
            seller_data = {
                '@id': seller_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P23_transferred_title_from'].append(seller_data)
    
    del data['gmn:P70_1_documents_seller']
    return data


def transform_p70_2_documents_buyer(data):
    """
    Transform gmn:P70_2_documents_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P22_transferred_title_to > E21_Person
    """
    if 'gmn:P70_2_documents_buyer' not in data:
        return data
    
    buyers = data['gmn:P70_2_documents_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P22_transferred_title_to' not in acquisition:
        acquisition['cidoc:P22_transferred_title_to'] = []
    
    for buyer_obj in buyers:
        if isinstance(buyer_obj, dict):
            buyer_data = buyer_obj.copy()
            if '@type' not in buyer_data:
                buyer_data['@type'] = 'cidoc:E21_Person'
        else:
            buyer_uri = str(buyer_obj)
            buyer_data = {
                '@id': buyer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P22_transferred_title_to'].append(buyer_data)
    
    del data['gmn:P70_2_documents_buyer']
    return data


def transform_p70_3_documents_transfer_of(data):
    """
    Transform gmn:P70_3_documents_transfer_of to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_3_documents_transfer_of' not in data:
        return data
    
    things = data['gmn:P70_3_documents_transfer_of']
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
    
    for thing_obj in things:
        if isinstance(thing_obj, dict):
            thing_data = thing_obj.copy()
            if '@type' not in thing_data:
                thing_data['@type'] = 'cidoc:E18_Physical_Thing'
        else:
            thing_uri = str(thing_obj)
            thing_data = {
                '@id': thing_uri,
                '@type': 'cidoc:E18_Physical_Thing'
            }
        
        acquisition['cidoc:P24_transferred_title_of'].append(thing_data)
    
    del data['gmn:P70_3_documents_transfer_of']
    return data


def transform_procurator_property(data, property_name, motivated_by_property):
    """
    Generic function to transform procurator properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    """
    if property_name not in data:
        return data
    
    procurators = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    # Get the motivated_by person (seller or buyer)
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    for procurator_obj in procurators:
        if isinstance(procurator_obj, dict):
            procurator_uri = procurator_obj.get('@id', '')
            procurator_data = procurator_obj.copy()
        else:
            procurator_uri = str(procurator_obj)
            procurator_data = {
                '@id': procurator_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(procurator_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/procurator_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [procurator_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_AGENT,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data[property_name]
    return data


def transform_p70_4_documents_sellers_procurator(data):
    """Transform gmn:P70_4_documents_sellers_procurator to full CIDOC-CRM structure."""
    return transform_procurator_property(data, 'gmn:P70_4_documents_sellers_procurator', 
                                        'cidoc:P23_transferred_title_from')


def transform_p70_5_documents_buyers_procurator(data):
    """Transform gmn:P70_5_documents_buyers_procurator to full CIDOC-CRM structure."""
    return transform_procurator_property(data, 'gmn:P70_5_documents_buyers_procurator', 
                                        'cidoc:P22_transferred_title_to')


def transform_guarantor_property(data, property_name, motivated_by_property):
    """
    Generic function to transform guarantor properties.
    Creates E7_Activity with P14_carried_out_by and P17_was_motivated_by.
    """
    if property_name not in data:
        return data
    
    guarantors = data[property_name]
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    motivated_by_uri = None
    if motivated_by_property in acquisition:
        motivated_by_list = acquisition[motivated_by_property]
        if isinstance(motivated_by_list, list) and len(motivated_by_list) > 0:
            if isinstance(motivated_by_list[0], dict):
                motivated_by_uri = motivated_by_list[0].get('@id')
            else:
                motivated_by_uri = str(motivated_by_list[0])
    
    for guarantor_obj in guarantors:
        if isinstance(guarantor_obj, dict):
            guarantor_uri = guarantor_obj.get('@id', '')
            guarantor_data = guarantor_obj.copy()
        else:
            guarantor_uri = str(guarantor_obj)
            guarantor_data = {
                '@id': guarantor_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(guarantor_uri + property_name))[-8:]
        activity_uri = f"{subject_uri}/activity/guarantor_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [guarantor_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_GUARANTOR,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        if motivated_by_uri:
            activity['cidoc:P17_was_motivated_by'] = {
                '@id': motivated_by_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data[property_name]
    return data


def transform_p70_6_documents_sellers_guarantor(data):
    """Transform gmn:P70_6_documents_sellers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_6_documents_sellers_guarantor', 
                                       'cidoc:P23_transferred_title_from')


def transform_p70_7_documents_buyers_guarantor(data):
    """Transform gmn:P70_7_documents_buyers_guarantor to full CIDOC-CRM structure."""
    return transform_guarantor_property(data, 'gmn:P70_7_documents_buyers_guarantor', 
                                       'cidoc:P22_transferred_title_to')


def transform_p70_8_documents_broker(data):
    """
    Transform gmn:P70_8_documents_broker to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P14_carried_out_by > E21_Person (with role)
    """
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


def transform_p70_9_documents_payment_provider_for_buyer(data):
    """
    Transform gmn:P70_9_documents_payment_provider_for_buyer to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    """
    if 'gmn:P70_9_documents_payment_provider_for_buyer' not in data:
        return data
    
    payers = data['gmn:P70_9_documents_payment_provider_for_buyer']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    for payer_obj in payers:
        if isinstance(payer_obj, dict):
            payer_uri = payer_obj.get('@id', '')
            payer_data = payer_obj.copy()
        else:
            payer_uri = str(payer_obj)
            payer_data = {
                '@id': payer_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(payer_uri + 'payment_provider'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P14_carried_out_by': [payer_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYER,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data['gmn:P70_9_documents_payment_provider_for_buyer']
    return data


def transform_p70_10_documents_payment_recipient_for_seller(data):
    """
    Transform gmn:P70_10_documents_payment_recipient_for_seller to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    """
    if 'gmn:P70_10_documents_payment_recipient_for_seller' not in data:
        return data
    
    payees = data['gmn:P70_10_documents_payment_recipient_for_seller']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    for payee_obj in payees:
        if isinstance(payee_obj, dict):
            payee_uri = payee_obj.get('@id', '')
            payee_data = payee_obj.copy()
        else:
            payee_uri = str(payee_obj)
            payee_data = {
                '@id': payee_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(payee_uri + 'payment_recipient'))[-8:]
        activity_uri = f"{subject_uri}/activity/payment_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_FINANCIAL_TRANSACTION,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P14_carried_out_by': [payee_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_PAYEE,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data['gmn:P70_10_documents_payment_recipient_for_seller']
    return data


def transform_p70_11_documents_referenced_person(data):
    """
    Transform gmn:P70_11_documents_referenced_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    """
    if 'gmn:P70_11_documents_referenced_person' not in data:
        return data
    
    persons = data['gmn:P70_11_documents_referenced_person']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for person_obj in persons:
        if isinstance(person_obj, dict):
            person_data = person_obj.copy()
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        data['cidoc:P67_refers_to'].append(person_data)
    
    del data['gmn:P70_11_documents_referenced_person']
    return data


def transform_p70_12_documents_payment_through_organization(data):
    """
    Transform gmn:P70_12_documents_payment_through_organization to full CIDOC-CRM structure:
    P67_refers_to > E74_Group
    """
    if 'gmn:P70_12_documents_payment_through_organization' not in data:
        return data
    
    organizations = data['gmn:P70_12_documents_payment_through_organization']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for org_obj in organizations:
        if isinstance(org_obj, dict):
            org_data = org_obj.copy()
            if '@type' not in org_data:
                org_data['@type'] = 'cidoc:E74_Group'
        else:
            org_uri = str(org_obj)
            org_data = {
                '@id': org_uri,
                '@type': 'cidoc:E74_Group'
            }
        
        data['cidoc:P67_refers_to'].append(org_data)
    
    del data['gmn:P70_12_documents_payment_through_organization']
    return data


def transform_p70_13_documents_referenced_place(data):
    """
    Transform gmn:P70_13_documents_referenced_place to full CIDOC-CRM structure:
    P67_refers_to > E53_Place
    """
    if 'gmn:P70_13_documents_referenced_place' not in data:
        return data
    
    places = data['gmn:P70_13_documents_referenced_place']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        data['cidoc:P67_refers_to'].append(place_data)
    
    del data['gmn:P70_13_documents_referenced_place']
    return data


def transform_p70_14_documents_referenced_object(data):
    """
    Transform gmn:P70_14_documents_referenced_object to full CIDOC-CRM structure:
    P67_refers_to > E18_Physical_Thing
    """
    if 'gmn:P70_14_documents_referenced_object' not in data:
        return data
    
    objects = data['gmn:P70_14_documents_referenced_object']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
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
        
        data['cidoc:P67_refers_to'].append(obj_data)
    
    del data['gmn:P70_14_documents_referenced_object']
    return data


def transform_p70_15_documents_witness(data):
    """
    Transform gmn:P70_15_documents_witness to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P9_consists_of > E7_Activity > P14_carried_out_by > E21_Person (with role)
    """
    if 'gmn:P70_15_documents_witness' not in data:
        return data
    
    witnesses = data['gmn:P70_15_documents_witness']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P9_consists_of' not in acquisition:
        acquisition['cidoc:P9_consists_of'] = []
    
    for witness_obj in witnesses:
        if isinstance(witness_obj, dict):
            witness_uri = witness_obj.get('@id', '')
            witness_data = witness_obj.copy()
        else:
            witness_uri = str(witness_obj)
            witness_data = {
                '@id': witness_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        activity_hash = str(hash(witness_uri + 'witness'))[-8:]
        activity_uri = f"{subject_uri}/activity/witness_{activity_hash}"
        
        activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P14_carried_out_by': [witness_data],
            'cidoc:P14.1_in_the_role_of': {
                '@id': AAT_WITNESS,
                '@type': 'cidoc:E55_Type'
            }
        }
        
        acquisition['cidoc:P9_consists_of'].append(activity)
    
    del data['gmn:P70_15_documents_witness']
    return data


def transform_p70_16_documents_sale_price_amount(data):
    """
    Transform gmn:P70_16_documents_sale_price_amount to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency_amount
    """
    if 'gmn:P70_16_documents_sale_price_amount' not in data:
        return data
    
    amounts = data['gmn:P70_16_documents_sale_price_amount']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    for amount_obj in amounts:
        if isinstance(amount_obj, dict):
            amount_value = amount_obj.get('@value', '')
        else:
            amount_value = str(amount_obj)
        
        if not amount_value:
            continue
        
        monetary_uri = f"{acquisition['@id']}/monetary_amount"
        monetary_amount = {
            '@id': monetary_uri,
            '@type': 'cidoc:E97_Monetary_Amount',
            'cidoc:P180_has_currency_amount': amount_value
        }
        
        acquisition['cidoc:P177_assigned_property_of_type'] = monetary_amount
    
    del data['gmn:P70_16_documents_sale_price_amount']
    return data


def transform_p70_17_documents_sale_price_currency(data):
    """
    Transform gmn:P70_17_documents_sale_price_currency to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P177_assigned_property_of_type > E97_Monetary_Amount > P180_has_currency > E98_Currency
    """
    if 'gmn:P70_17_documents_sale_price_currency' not in data:
        return data
    
    currencies = data['gmn:P70_17_documents_sale_price_currency']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P177_assigned_property_of_type' not in acquisition:
        monetary_uri = f"{acquisition['@id']}/monetary_amount"
        acquisition['cidoc:P177_assigned_property_of_type'] = {
            '@id': monetary_uri,
            '@type': 'cidoc:E97_Monetary_Amount'
        }
    
    monetary_amount = acquisition['cidoc:P177_assigned_property_of_type']
    
    for currency_obj in currencies:
        if isinstance(currency_obj, dict):
            currency_data = currency_obj.copy()
            if '@type' not in currency_data:
                currency_data['@type'] = 'cidoc:E98_Currency'
        else:
            currency_uri = str(currency_obj)
            currency_data = {
                '@id': currency_uri,
                '@type': 'cidoc:E98_Currency'
            }
        
        monetary_amount['cidoc:P180_has_currency'] = currency_data
    
    del data['gmn:P70_17_documents_sale_price_currency']
    return data


def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    parties = data['gmn:P70_18_documents_disputing_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    for party_obj in parties:
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
    
    del data['gmn:P70_18_documents_disputing_party']
    return data


def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    for arbitrator_obj in arbitrators:
        if isinstance(arbitrator_obj, dict):
            arbitrator_data = arbitrator_obj.copy()
            if '@type' not in arbitrator_data:
                arbitrator_data['@type'] = 'cidoc:E39_Actor'
        else:
            arbitrator_uri = str(arbitrator_obj)
            arbitrator_data = {
                '@id': arbitrator_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    del data['gmn:P70_19_documents_arbitrator']
    return data


def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    """
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    subjects = data['gmn:P70_20_documents_dispute_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/arbitration"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity'
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    for subject_obj in subjects:
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
        
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    del data['gmn:P70_20_documents_dispute_subject']
    return data


def transform_p70_21_indicates_conceding_party(data):
    """
    Transform gmn:P70_21_indicates_conceding_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_21_indicates_conceding_party' not in data:
        return data
    
    conceding_parties = data['gmn:P70_21_indicates_conceding_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
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
    
    for party_obj in conceding_parties:
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
    
    del data['gmn:P70_21_indicates_conceding_party']
    return data

def transform_p70_22_indicates_receiving_party(data):
    """
    Transform gmn:P70_22_indicates_receiving_party to full CIDOC-CRM structure.
    
    Handles different document types:
    - For cessions (E31_4): P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    - For declarations (E31_5): P70_documents > E7_Activity > P01_has_domain > E39_Actor
    - For donations (E31_7): P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
    - For dowries (E31_8): P70_documents > E8_Acquisition > P22_transferred_title_to > E39_Actor
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

def transform_p70_23_indicates_object_of_cession(data):
    """
    Transform gmn:P70_23_indicates_object_of_cession to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E72_Legal_Object
    """
    if 'gmn:P70_23_indicates_object_of_cession' not in data:
        return data
    
    rights = data['gmn:P70_23_indicates_object_of_cession']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
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
    
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    for right_obj in rights:
        if isinstance(right_obj, dict):
            right_data = right_obj.copy()
            if '@type' not in right_data:
                right_data['@type'] = 'cidoc:E72_Legal_Object'
        else:
            right_uri = str(right_obj)
            right_data = {
                '@id': right_uri,
                '@type': 'cidoc:E72_Legal_Object'
            }
        
        activity['cidoc:P16_used_specific_object'].append(right_data)
    
    del data['gmn:P70_23_indicates_object_of_cession']
    return data


def transform_p70_24_indicates_declarant(data):
    """
    Transform gmn:P70_24_indicates_declarant to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_24_indicates_declarant' not in data:
        return data
    
    declarants = data['gmn:P70_24_indicates_declarant']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
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
    
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    for declarant_obj in declarants:
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
        
        activity['cidoc:P14_carried_out_by'].append(declarant_data)
    
    del data['gmn:P70_24_indicates_declarant']
    return data


def transform_p70_25_indicates_declaration_subject(data):
    """
    Transform gmn:P70_25_indicates_declaration_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    """
    if 'gmn:P70_25_indicates_declaration_subject' not in data:
        return data
    
    subjects = data['gmn:P70_25_indicates_declaration_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
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
    
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    for subject_obj in subjects:
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
        
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    del data['gmn:P70_25_indicates_declaration_subject']
    return data


def transform_p70_26_indicates_sender(data):
    """
    Transform gmn:P70_26_indicates_sender to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    """
    if 'gmn:P70_26_indicates_sender' not in data:
        return data
    
    senders = data['gmn:P70_26_indicates_sender']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/correspondence"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P14_carried_out_by' not in activity:
        activity['cidoc:P14_carried_out_by'] = []
    
    for sender_obj in senders:
        if isinstance(sender_obj, dict):
            sender_data = sender_obj.copy()
            if '@type' not in sender_data:
                sender_data['@type'] = 'cidoc:E39_Actor'
        else:
            sender_uri = str(sender_obj)
            sender_data = {
                '@id': sender_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P14_carried_out_by'].append(sender_data)
    
    del data['gmn:P70_26_indicates_sender']
    return data


def transform_p70_27_has_address_of_origin(data):
    """
    Transform gmn:P70_27_has_address_of_origin to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P27_moved_from > E53_Place
    """
    if 'gmn:P70_27_has_address_of_origin' not in data:
        return data
    
    places = data['gmn:P70_27_has_address_of_origin']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/correspondence"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        activity['cidoc:P27_moved_from'] = place_data
    
    del data['gmn:P70_27_has_address_of_origin']
    return data


def transform_p70_28_indicates_addressee(data):
    """
    Transform gmn:P70_28_indicates_addressee to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P01_has_domain > E39_Actor
    """
    if 'gmn:P70_28_indicates_addressee' not in data:
        return data
    
    addressees = data['gmn:P70_28_indicates_addressee']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/correspondence"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P01_has_domain' not in activity:
        activity['cidoc:P01_has_domain'] = []
    
    for addressee_obj in addressees:
        if isinstance(addressee_obj, dict):
            addressee_data = addressee_obj.copy()
            if '@type' not in addressee_data:
                addressee_data['@type'] = 'cidoc:E39_Actor'
        else:
            addressee_uri = str(addressee_obj)
            addressee_data = {
                '@id': addressee_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        activity['cidoc:P01_has_domain'].append(addressee_data)
    
    del data['gmn:P70_28_indicates_addressee']
    return data


def transform_p70_29_describes_subject(data):
    """
    Transform gmn:P70_29_describes_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    """
    if 'gmn:P70_29_describes_subject' not in data:
        return data
    
    subjects = data['gmn:P70_29_describes_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/correspondence"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P16_used_specific_object' not in activity:
        activity['cidoc:P16_used_specific_object'] = []
    
    for subject_obj in subjects:
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
        
        activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    del data['gmn:P70_29_describes_subject']
    return data


def transform_p70_30_mentions_person(data):
    """
    Transform gmn:P70_30_mentions_person to full CIDOC-CRM structure:
    P67_refers_to > E21_Person
    """
    if 'gmn:P70_30_mentions_person' not in data:
        return data
    
    persons = data['gmn:P70_30_mentions_person']
    
    if 'cidoc:P67_refers_to' not in data:
        data['cidoc:P67_refers_to'] = []
    
    for person_obj in persons:
        if isinstance(person_obj, dict):
            person_data = person_obj.copy()
            if '@type' not in person_data:
                person_data['@type'] = 'cidoc:E21_Person'
        else:
            person_uri = str(person_obj)
            person_data = {
                '@id': person_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        data['cidoc:P67_refers_to'].append(person_data)
    
    del data['gmn:P70_30_mentions_person']
    return data


def transform_p70_31_has_address_of_destination(data):
    """
    Transform gmn:P70_31_has_address_of_destination to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P26_moved_to > E53_Place
    """
    if 'gmn:P70_31_has_address_of_destination' not in data:
        return data
    
    places = data['gmn:P70_31_has_address_of_destination']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        activity_uri = f"{subject_uri}/correspondence"
        data['cidoc:P70_documents'] = [{
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_CORRESPONDENCE,
                '@type': 'cidoc:E55_Type'
            }
        }]
    
    activity = data['cidoc:P70_documents'][0]
    
    for place_obj in places:
        if isinstance(place_obj, dict):
            place_data = place_obj.copy()
            if '@type' not in place_data:
                place_data['@type'] = 'cidoc:E53_Place'
        else:
            place_uri = str(place_obj)
            place_data = {
                '@id': place_uri,
                '@type': 'cidoc:E53_Place'
            }
        
        activity['cidoc:P26_moved_to'] = place_data
    
    del data['gmn:P70_31_has_address_of_destination']
    return data


def transform_p70_32_indicates_donor(data):
    """
    Transform gmn:P70_32_indicates_donor to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P23_transferred_title_from > E39_Actor
    """
    if 'gmn:P70_32_indicates_donor' not in data:
        return data
    
    donors = data['gmn:P70_32_indicates_donor']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P70_documents' not in data or len(data['cidoc:P70_documents']) == 0:
        acquisition_uri = f"{subject_uri}/acquisition"
        data['cidoc:P70_documents'] = [{
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition'
        }]
    
    acquisition = data['cidoc:P70_documents'][0]
    
    if 'cidoc:P23_transferred_title_from' not in acquisition:
        acquisition['cidoc:P23_transferred_title_from'] = []
    
    for donor_obj in donors:
        if isinstance(donor_obj, dict):
            donor_data = donor_obj.copy()
            if '@type' not in donor_data:
                donor_data['@type'] = 'cidoc:E39_Actor'
        else:
            donor_uri = str(donor_obj)
            donor_data = {
                '@id': donor_uri,
                '@type': 'cidoc:E39_Actor'
            }
        
        acquisition['cidoc:P23_transferred_title_from'].append(donor_data)
    
    del data['gmn:P70_32_indicates_donor']
    return data


def transform_p70_33_indicates_object_of_donation(data):
    """
    Transform gmn:P70_33_indicates_object_of_donation to full CIDOC-CRM structure:
    P70_documents > E8_Acquisition > P24_transferred_title_of > E18_Physical_Thing
    """
    if 'gmn:P70_33_indicates_object_of_donation' not in data:
        return data
    
    objects = data['gmn:P70_33_indicates_object_of_donation']
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
    
    del data['gmn:P70_33_indicates_object_of_donation']
    return data


def transform_p138i_1_has_representation(data):
    """
    Transform gmn:P138i_1_has_representation to full CIDOC-CRM structure:
    P138i_has_representation > E36_Visual_Item
    """
    if 'gmn:P138i_1_has_representation' not in data:
        return data
    
    representations = data['gmn:P138i_1_has_representation']
    
    if 'cidoc:P138i_has_representation' not in data:
        data['cidoc:P138i_has_representation'] = []
    
    for rep_obj in representations:
        if isinstance(rep_obj, dict):
            rep_data = rep_obj.copy()
            if '@type' not in rep_data:
                rep_data['@type'] = 'cidoc:E36_Visual_Item'
        else:
            rep_uri = str(rep_obj)
            rep_data = {
                '@id': rep_uri,
                '@type': 'cidoc:E36_Visual_Item'
            }
        
        data['cidoc:P138i_has_representation'].append(rep_data)
    
    del data['gmn:P138i_1_has_representation']
    return data


def transform_p11i_1_earliest_attestation_date(data):
    """
    Transform gmn:P11i_1_earliest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82a_begin_of_the_begin
    """
    if 'gmn:P11i_1_earliest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_1_earliest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for date_obj in dates:
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            continue
        
        event_hash = str(hash(date_value + 'earliest'))[-8:]
        event_uri = f"{subject_uri}/event/earliest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82a_begin_of_the_begin': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_1_earliest_attestation_date']
    return data


def transform_p11i_2_latest_attestation_date(data):
    """
    Transform gmn:P11i_2_latest_attestation_date to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event > P4_has_time-span > E52_Time-Span > P82b_end_of_the_end
    """
    if 'gmn:P11i_2_latest_attestation_date' not in data:
        return data
    
    dates = data['gmn:P11i_2_latest_attestation_date']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for date_obj in dates:
        if isinstance(date_obj, dict):
            date_value = date_obj.get('@value', '')
        else:
            date_value = str(date_obj)
        
        if not date_value:
            continue
        
        event_hash = str(hash(date_value + 'latest'))[-8:]
        event_uri = f"{subject_uri}/event/latest_{event_hash}"
        timespan_uri = f"{event_uri}/timespan"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P4_has_time-span': {
                '@id': timespan_uri,
                '@type': 'cidoc:E52_Time-Span',
                'cidoc:P82b_end_of_the_end': date_value
            }
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_2_latest_attestation_date']
    return data


def transform_p11i_3_has_spouse(data):
    """
    Transform gmn:P11i_3_has_spouse to full CIDOC-CRM structure:
    P11i_participated_in > E5_Event (marriage) > P11_had_participant > E21_Person
    """
    if 'gmn:P11i_3_has_spouse' not in data:
        return data
    
    spouses = data['gmn:P11i_3_has_spouse']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P11i_participated_in' not in data:
        data['cidoc:P11i_participated_in'] = []
    
    for spouse_obj in spouses:
        if isinstance(spouse_obj, dict):
            spouse_uri = spouse_obj.get('@id', '')
            spouse_data = spouse_obj.copy()
        else:
            spouse_uri = str(spouse_obj)
            spouse_data = {
                '@id': spouse_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        event_hash = str(hash(spouse_uri + 'marriage'))[-8:]
        event_uri = f"{subject_uri}/event/marriage_{event_hash}"
        
        event = {
            '@id': event_uri,
            '@type': 'cidoc:E5_Event',
            'cidoc:P2_has_type': {
                '@id': AAT_MARRIAGE,
                '@type': 'cidoc:E55_Type'
            },
            'cidoc:P11_had_participant': [spouse_data]
        }
        
        data['cidoc:P11i_participated_in'].append(event)
    
    del data['gmn:P11i_3_has_spouse']
    return data


def transform_p22_1_has_owner(data):
    """
    Transform gmn:P22_1_has_owner to full CIDOC-CRM structure:
    P24i_changed_ownership_through > E8_Acquisition > P22_transferred_title_to > E21_Person
    """
    if 'gmn:P22_1_has_owner' not in data:
        return data
    
    owners = data['gmn:P22_1_has_owner']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    if 'cidoc:P24i_changed_ownership_through' not in data:
        data['cidoc:P24i_changed_ownership_through'] = []
    
    for owner_obj in owners:
        if isinstance(owner_obj, dict):
            owner_uri = owner_obj.get('@id', '')
            owner_data = owner_obj.copy()
        else:
            owner_uri = str(owner_obj)
            owner_data = {
                '@id': owner_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        acquisition_hash = str(hash(owner_uri + 'ownership'))[-8:]
        acquisition_uri = f"{subject_uri}/acquisition/ownership_{acquisition_hash}"
        
        acquisition = {
            '@id': acquisition_uri,
            '@type': 'cidoc:E8_Acquisition',
            'cidoc:P22_transferred_title_to': [owner_data]
        }
        
        data['cidoc:P24i_changed_ownership_through'].append(acquisition)
    
    del data['gmn:P22_1_has_owner']
    return data


def transform_p53_1_has_occupant(data):
    """
    Transform gmn:P53_1_has_occupant to full CIDOC-CRM structure:
    P59i_is_located_on_or_within > E53_Place > P53_has_former_or_current_location > E21_Person
    """
    if 'gmn:P53_1_has_occupant' not in data:
        return data
    
    occupants = data['gmn:P53_1_has_occupant']
    
    if 'cidoc:P53_has_former_or_current_location' not in data:
        data['cidoc:P53_has_former_or_current_location'] = []
    
    for occupant_obj in occupants:
        if isinstance(occupant_obj, dict):
            occupant_data = occupant_obj.copy()
            if '@type' not in occupant_data:
                occupant_data['@type'] = 'cidoc:E21_Person'
        else:
            occupant_uri = str(occupant_obj)
            occupant_data = {
                '@id': occupant_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        data['cidoc:P53_has_former_or_current_location'].append(occupant_data)
    
    del data['gmn:P53_1_has_occupant']
    return data

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

def transform_p96_1_has_mother(data):
    """
    Transform gmn:P96_1_has_mother to full CIDOC-CRM structure:
    P98i_was_born > E67_Birth > P96_by_mother > E21_Person
    """
    if 'gmn:P96_1_has_mother' not in data:
        return data
    
    mothers = data['gmn:P96_1_has_mother']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    birth_uri = f"{subject_uri}/birth"
    
    if 'cidoc:P98i_was_born' not in data:
        data['cidoc:P98i_was_born'] = {
            '@id': birth_uri,
            '@type': 'cidoc:E67_Birth'
        }
    
    birth = data['cidoc:P98i_was_born']
    
    if 'cidoc:P96_by_mother' not in birth:
        birth['cidoc:P96_by_mother'] = []
    
    for mother_obj in mothers:
        if isinstance(mother_obj, dict):
            mother_data = mother_obj.copy()
            if '@type' not in mother_data:
                mother_data['@type'] = 'cidoc:E21_Person'
        else:
            mother_uri = str(mother_obj)
            mother_data = {
                '@id': mother_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        birth['cidoc:P96_by_mother'].append(mother_data)
    
    del data['gmn:P96_1_has_mother']
    return data


def transform_p97_1_has_father(data):
    """
    Transform gmn:P97_1_has_father to full CIDOC-CRM structure:
    P98i_was_born > E67_Birth > P97_from_father > E21_Person
    """
    if 'gmn:P97_1_has_father' not in data:
        return data
    
    fathers = data['gmn:P97_1_has_father']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    birth_uri = f"{subject_uri}/birth"
    
    if 'cidoc:P98i_was_born' not in data:
        data['cidoc:P98i_was_born'] = {
            '@id': birth_uri,
            '@type': 'cidoc:E67_Birth'
        }
    
    birth = data['cidoc:P98i_was_born']
    
    if 'cidoc:P97_from_father' not in birth:
        birth['cidoc:P97_from_father'] = []
    
    for father_obj in fathers:
        if isinstance(father_obj, dict):
            father_data = father_obj.copy()
            if '@type' not in father_data:
                father_data['@type'] = 'cidoc:E21_Person'
        else:
            father_uri = str(father_obj)
            father_data = {
                '@id': father_uri,
                '@type': 'cidoc:E21_Person'
            }
        
        birth['cidoc:P97_from_father'].append(father_data)
    
    del data['gmn:P97_1_has_father']
    return data


def transform_p107i_1_has_regional_provenance(data):
    """
    Transform gmn:P107i_1_has_regional_provenance to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_1_Regional_Provenance
    """
    if 'gmn:P107i_1_has_regional_provenance' not in data:
        return data
    
    groups = data['gmn:P107i_1_has_regional_provenance']
    
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    for group_obj in groups:
        if isinstance(group_obj, dict):
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_1_Regional_Provenance']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_1_Regional_Provenance']
        elif 'gmn:E74_1_Regional_Provenance' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_1_Regional_Provenance')
        
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    del data['gmn:P107i_1_has_regional_provenance']
    return data


def transform_p107i_2_has_social_category(data):
    """
    Transform gmn:P107i_2_has_social_category to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_2_Social_Category
    """
    if 'gmn:P107i_2_has_social_category' not in data:
        return data
    
    groups = data['gmn:P107i_2_has_social_category']
    
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    for group_obj in groups:
        if isinstance(group_obj, dict):
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_2_Social_Category']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_2_Social_Category']
        elif 'gmn:E74_2_Social_Category' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_2_Social_Category')
        
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    del data['gmn:P107i_2_has_social_category']
    return data


def transform_p107i_3_has_occupation(data):
    """
    Transform gmn:P107i_3_has_occupation to full CIDOC-CRM structure:
    P107i_is_current_or_former_member_of > gmn:E74_3_Occupational_Group
    """
    if 'gmn:P107i_3_has_occupation' not in data:
        return data
    
    groups = data['gmn:P107i_3_has_occupation']
    
    if 'cidoc:P107i_is_current_or_former_member_of' not in data:
        data['cidoc:P107i_is_current_or_former_member_of'] = []
    
    for group_obj in groups:
        if isinstance(group_obj, dict):
            group_data = group_obj.copy()
        else:
            group_uri = str(group_obj)
            group_data = {'@id': group_uri}
        
        if '@type' not in group_data:
            group_data['@type'] = ['cidoc:E74_Group', 'gmn:E74_3_Occupational_Group']
        elif isinstance(group_data['@type'], str):
            group_data['@type'] = [group_data['@type'], 'gmn:E74_3_Occupational_Group']
        elif 'gmn:E74_3_Occupational_Group' not in group_data['@type']:
            group_data['@type'].append('gmn:E74_3_Occupational_Group')
        
        data['cidoc:P107i_is_current_or_former_member_of'].append(group_data)
    
    del data['gmn:P107i_3_has_occupation']
    return data


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

    # Dowry properties (P70.34)
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


def transform_export(input_file, output_file, include_internal=False):
    """
    Transform an entire JSON-LD export file.
    
    Args:
        input_file: Path to input JSON-LD file
        output_file: Path to output CIDOC-CRM compliant file
        include_internal: If True, transform internal notes. If False (default), remove them.
    
    Returns:
        Boolean indicating success or failure
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single items and arrays of items
        if isinstance(data, list):
            transformed = [transform_item(item, include_internal) for item in data]
        elif isinstance(data, dict) and '@graph' in data:
            # Handle JSON-LD with @graph
            data['@graph'] = [transform_item(item, include_internal) for item in data['@graph']]
            transformed = data
        else:
            transformed = transform_item(data, include_internal)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transformed, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Transformation complete: {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: Input file '{input_file}' not found", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON in input file: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error during transformation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


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
        print("  - gmn:E31_4_Cession_of_Rights_Contract")
        print("  - gmn:E31_5_Declaration")
        print("  - gmn:E31_6_Correspondence")
        print("  - gmn:E31_7_Donation_Contract")
        print("  - gmn:E31_8_Dowry_Contract")
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


if __name__ == '__main__':
    main()
