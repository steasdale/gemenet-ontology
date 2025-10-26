# E31.2 Sales Contract - Python Transformation Functions
# These functions are already implemented in gmn_to_cidoc_transform.py
# This file provides them separately for reference

from uuid import uuid4

# Getty AAT URI constants for sales contracts
AAT_AGENT = "http://vocab.getty.edu/page/aat/300025972"
AAT_GUARANTOR = "http://vocab.getty.edu/page/aat/300025614"
AAT_BROKER = "http://vocab.getty.edu/page/aat/300025234"
AAT_PAYER = "http://vocab.getty.edu/page/aat/300386048"
AAT_PAYEE = "http://vocab.getty.edu/page/aat/300386184"
AAT_FINANCIAL_TRANSACTION = "http://vocab.getty.edu/page/aat/300055984"
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"


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


# Transform item function integration
# Add these calls to your transform_item() function in the correct order:
#
# # Sales contract properties (P70.1-P70.17)
# item = transform_p70_1_documents_seller(item)
# item = transform_p70_2_documents_buyer(item)
# item = transform_p70_3_documents_transfer_of(item)
# item = transform_p70_4_documents_sellers_procurator(item)
# item = transform_p70_5_documents_buyers_procurator(item)
# item = transform_p70_6_documents_sellers_guarantor(item)
# item = transform_p70_7_documents_buyers_guarantor(item)
# item = transform_p70_8_documents_broker(item)
# item = transform_p70_9_documents_payment_provider_for_buyer(item)
# item = transform_p70_10_documents_payment_recipient_for_seller(item)
# item = transform_p70_11_documents_referenced_person(item)
# item = transform_p70_12_documents_payment_through_organization(item)
# item = transform_p70_13_documents_referenced_place(item)
# item = transform_p70_14_documents_referenced_object(item)
# item = transform_p70_15_documents_witness(item)
# item = transform_p70_16_documents_sale_price_amount(item)
# item = transform_p70_17_documents_sale_price_currency(item)
