documents'] = [existing_activity]
    
    # Step 4: Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Step 5: Add disputing parties to the activity
    for party_obj in parties:
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
        
        # Add to arbitration activity
        existing_activity['cidoc:P14_carried_out_by'].append(party_data)
    
    # Step 6: Remove shortcut property from data
    del data['gmn:P70_18_documents_disputing_party']
    
    return data
```

**Understanding the function step-by-step**:

**Step 1: Check if property exists**
```python
if 'gmn:P70_18_documents_disputing_party' not in data:
    return data
```
- If the property isn't present, nothing to do
- Returns data unchanged

**Step 2: Get property values**
```python
parties = data['gmn:P70_18_documents_disputing_party']
subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
```
- Retrieves the array of disputing parties
- Gets the document URI (or generates one if missing)

**Step 3: Find or create E7_Activity**
```python
if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
    existing_activity = data['cidoc:P70_documents'][0]
else:
    # Create new activity...
```
- **Critical logic**: Checks if activity already exists
- If yes: reuses it (ensuring shared activity pattern)
- If no: creates new one with proper typing

**Step 4: Initialize P14**
```python
if 'cidoc:P14_carried_out_by' not in existing_activity:
    existing_activity['cidoc:P14_carried_out_by'] = []
```
- Ensures P14 array exists before adding to it
- Prevents errors if this is first property processed

**Step 5: Add parties**
```python
for party_obj in parties:
    if isinstance(party_obj, dict):
        # Handle full object...
    else:
        # Handle URI reference...
```
- Handles both formats: `{"@id": "uri"}` and just `"uri"`
- Ensures @type is set to E39_Actor
- Appends to P14 array

**Step 6: Clean up**
```python
del data['gmn:P70_18_documents_disputing_party']
```
- Removes the shortcut property
- Leaves only CIDOC-CRM compliant structure

### Step 2.6: Add transform_p70_19_documents_arbitrator Function

**Insert this complete function immediately after the previous one**:

```python
def transform_p70_19_documents_arbitrator(data):
    """
    Transform gmn:P70_19_documents_arbitrator to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function locates the existing E7_Activity node (or creates one) and adds
    arbitrators to it via P14_carried_out_by. Arbitrators are the neutral third
    parties who conduct the arbitration and render binding decisions.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Note:
        Arbitrators and disputing parties both use P14_carried_out_by because
        they are all active principals carrying out the arbitration agreement.
    """
    # Step 1: Check if property exists in data
    if 'gmn:P70_19_documents_arbitrator' not in data:
        return data
    
    # Step 2: Get the property values (array of arbitrators)
    arbitrators = data['gmn:P70_19_documents_arbitrator']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Step 4: Initialize P14 if it doesn't exist
    if 'cidoc:P14_carried_out_by' not in existing_activity:
        existing_activity['cidoc:P14_carried_out_by'] = []
    
    # Step 5: Add arbitrators to the activity
    for arbitrator_obj in arbitrators:
        # Handle both URI references and full objects
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
        
        # Add to arbitration activity
        existing_activity['cidoc:P14_carried_out_by'].append(arbitrator_data)
    
    # Step 6: Remove shortcut property from data
    del data['gmn:P70_19_documents_arbitrator']
    
    return data
```

**Key similarities with P70.18 function**:
- Same overall structure
- Same activity detection/creation logic
- Same P14 initialization
- Same actor handling (URI vs object)

**Key differences**:
- Operates on `gmn:P70_19_documents_arbitrator` instead of P70.18
- Variable names use "arbitrator" instead of "party"
- Documentation emphasizes arbitrators as "neutral third parties"

**Why so similar?**
Both disputing parties and arbitrators are added to the **same property** (P14_carried_out_by) on the **same activity**. The functions are nearly identical by design.

### Step 2.7: Add transform_p70_20_documents_dispute_subject Function

**Insert this complete function immediately after the previous one**:

```python
def transform_p70_20_documents_dispute_subject(data):
    """
    Transform gmn:P70_20_documents_dispute_subject to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity
    
    This function locates the existing E7_Activity node and adds the dispute
    subject(s) via P16_used_specific_object. The dispute subject is the matter
    being arbitrated - can be property, rights, debts, contracts, etc.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Note:
        Unlike P70.18/P70.19 which use P14 (carried out by), this uses P16
        (used specific object) because the subject is operated on, not a participant.
    """
    # Step 1: Check if property exists in data
    if 'gmn:P70_20_documents_dispute_subject' not in data:
        return data
    
    # Step 2: Get the property values (array of subjects)
    subjects = data['gmn:P70_20_documents_dispute_subject']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_documents'] = [existing_activity]
    
    # Step 4: Initialize P16 if it doesn't exist
    if 'cidoc:P16_used_specific_object' not in existing_activity:
        existing_activity['cidoc:P16_used_specific_object'] = []
    
    # Step 5: Add dispute subjects to the activity
    for subject_obj in subjects:
        # Handle both URI references and full objects
        if isinstance(subject_obj, dict):
            subject_data = subject_obj.copy()
            if '@type' not in subject_data:
                subject_data['@type'] = 'cidoc:E1_CRM_Entity'
        else:
            subject_uri_ref = str(subject_obj)
            subject_data = {
                '@id': subject_uri_ref,
                '@type': 'cidoc:E1_CRM_Entity'
            }
        
        # Add to arbitration activity
        existing_activity['cidoc:P16_used_specific_object'].append(subject_data)
    
    # Step 6: Remove shortcut property from data
    del data['gmn:P70_20_documents_dispute_subject']
    
    return data
```

**Key differences from P70.18/P70.19**:

1. **Different target property**: `P16_used_specific_object` instead of `P14_carried_out_by`
2. **Different type**: `E1_CRM_Entity` instead of `E39_Actor`
3. **Different semantic**: Subject is operated on, not a participant

**Understanding P16 vs P14**:
- **P14_carried_out_by**: For actors who perform/enact the activity
- **P16_used_specific_object**: For things the activity operates on/uses

The dispute subject doesn't carry out arbitration - it's what the arbitration is about.

### Step 2.8: Update the transform_item Function

**Location**: Find the `transform_item()` function (usually near the end of the file)

**Find this section**:
```python
def transform_item(item, include_internal=False):
    """
    Transform a single item, applying all transformation rules.
    
    Args:
        item: Item data dictionary
        include_internal: If True, transform internal notes to CIDOC-CRM. 
                         If False (default), remove internal notes entirely.
    """
    # Name and identification properties
    item = transform_p1_1_has_name(item)
    item = transform_p1_2_has_name_from_source(item)
    # ... many more transformations ...
    
    # Sales contract properties
    item = transform_p70_1_documents_seller(item)
    item = transform_p70_2_documents_buyer(item)
    # ... more sales contract properties ...
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # ← INSERT HERE
    
    return item
```

**Insert these three lines after sales contract properties**:
```python
    # Arbitration agreement properties
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
```

**Complete section should look like**:
```python
    # Sales contract properties
    item = transform_p70_1_documents_seller(item)
    # ... other sales contract functions ...
    item = transform_p70_17_documents_sale_price_currency(item)
    
    # Arbitration agreement properties
    item = transform_p70_18_documents_disputing_party(item)
    item = transform_p70_19_documents_arbitrator(item)
    item = transform_p70_20_documents_dispute_subject(item)
    
    return item
```

**Why this matters**:
- Without these calls, the transformation functions won't run
- Order doesn't matter for these three (they share activity)
- But they must come after any document creation properties

### Step 2.9: Save and Test Python Syntax

**Save the file**: Ctrl+S (or Cmd+S)

**Test syntax compilation**:
```bash
python3 -m py_compile gmn_to_cidoc_transform_script.py
```

**If successful**: No output, file compiles without errors

**If errors**: Python will show line number and error type

**Common Python errors and fixes**:

Error: `IndentationError: unexpected indent`
- **Cause**: Mixed tabs and spaces, or wrong indentation level
- **Fix**: Use 4 spaces consistently, check indentation matches surrounding code

Error: `NameError: name 'uuid4' is not defined`
- **Cause**: Missing import statement
- **Fix**: Ensure `from uuid import uuid4` is at top of file

Error: `NameError: name 'AAT_ARBITRATION' is not defined`
- **Cause**: Constant not defined or defined after function
- **Fix**: Move constant definition before function definitions

Error: `SyntaxError: invalid syntax`
- **Cause**: Missing colon, parenthesis, or quote
- **Fix**: Check line indicated in error message, look for missing syntax elements

### Step 2.10: Visual Check of Script Structure

Before moving on, verify:

**Check 1: Constant is defined**
```python
# Should see in constants section:
AAT_WITNESS = "http://..."
AAT_ARBITRATION = "http://..."  # ← NEW
```

**Check 2: Three functions exist**
```python
# Should see these function signatures:
def transform_p70_18_documents_disputing_party(data):
def transform_p70_19_documents_arbitrator(data):
def transform_p70_20_documents_dispute_subject(data):
```

**Check 3: Functions are called**
```python
# Should see in transform_item():
item = transform_p70_18_documents_disputing_party(item)
item = transform_p70_19_documents_arbitrator(item)
item = transform_p70_20_documents_dispute_subject(item)
```

**Check 4: Indentation is consistent**
- All function definitions start at column 0
- All code inside functions indented by 4 spaces
- Nested code indented by additional 4 spaces

✅ **Phase 2 Checkpoint**: Transformation script updated with 1 constant and 3 functions, all syntax valid

---

## Phase 3: Documentation Updates

### Overview

In this phase, you'll update your project documentation to describe the new class and properties. The exact location and format will depend on your documentation structure.

**Time estimate**: 15-20 minutes

### Step 3.1: Locate and Open Documentation

1. Find your main project documentation file
2. **Create a backup**:
   ```bash
   cp main_documentation.md main_documentation.md.backup
   ```
3. Open in your text editor

### Step 3.2: Update Class Hierarchy Section

**Find the section** describing contract classes (might be titled "Classes", "Ontology Structure", "Contract Types", etc.)

**Update the hierarchy to**:
```
E31_1_Contract (General contract class)
├── E31_2_Sales_Contract (Sales and acquisition contracts)
└── E31_3_Arbitration_Agreement (Arbitration agreements)  ← NEW
```

**Add description** after the hierarchy:
```markdown
### E31_3_Arbitration_Agreement

Represents arbitration agreement documents that record agreements between 
disputing parties to transfer the obligation to resolve their dispute to 
appointed arbitrator(s). In medieval commerce, arbitration provided a faster, 
more flexible alternative to formal court proceedings.

**Key characteristics:**
- Models arbitration as E7_Activity (collaborative process)
- All parties (disputing parties AND arbitrators) are active principals
- Uses P14_carried_out_by for all actors
- Links dispute subject via P16_used_specific_object
- Typed as AAT 300417271 (arbitration process)
```

### Step 3.3: Add Property Descriptions

**In the properties reference section**, add entries for the three new properties.

You can copy the complete text from `arbitration-agreement-doc-note.txt`, or use this condensed version:

```markdown
### P70.18 documents disputing party

**Domain:** E31_3_Arbitration_Agreement  
**Range:** E39_Actor  
**Path:** E31 → P70 → E7_Activity → P14 → E39_Actor

Links arbitration agreement to parties involved in the dispute. Disputing 
parties are active principals who agree to submit their conflict to arbitration.

**Example:**
```turtle
<contract_123> gmn:P70_18_documents_disputing_party <merchant_giovanni> ;
               gmn:P70_18_documents_disputing_party <merchant_marco> .
```

---

### P70.19 documents arbitrator

**Domain:** E31_3_Arbitration_Agreement  
**Range:** E39_Actor  
**Path:** E31 → P70 → E7_Activity → P14 → E39_Actor

Links arbitration agreement to person(s) appointed to resolve the dispute. 
Arbitrators are neutral third parties who render binding decisions.

**Example:**
```turtle
<contract_123> gmn:P70_19_documents_arbitrator <judge_antonio> .
```

---

### P70.20 documents dispute subject

**Domain:** E31_3_Arbitration_Agreement  
**Range:** E1_CRM_Entity  
**Path:** E31 → P70 → E7_Activity → P16 → E1_CRM_Entity

Links arbitration agreement to the subject matter of the dispute. Can be any 
entity type: property, rights, debts, contracts, etc.

**Example:**
```turtle
<contract_123> gmn:P70_20_documents_dispute_subject <palazzo_spinola> .
```
```

### Step 3.4: Add Usage Example

**Find or create an "Examples" section**, then add:

```markdown
## Example: Arbitration Agreement

Two merchants dispute ownership of a building and agree to arbitration:

**Input (Omeka-S):**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [{
    "@value": "Arbitration - Palazzo Spinola Dispute"
  }],
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/giovanni"},
    {"@id": "http://example.org/persons/marco"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/judge_antonio"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/buildings/palazzo_spinola"}
  ],
  "gmn:P94i_2_has_enactment_date": [{
    "@value": "1450-06-15",
    "@type": "xsd:date"
  }]
}
```

**Output (Transformed):**
```json
{
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "cidoc:P70_documents": [{
    "@id": "http://example.org/contract/123/arbitration",
    "@type": "cidoc:E7_Activity",
    "cidoc:P2_has_type": {
      "@id": "http://vocab.getty.edu/page/aat/300417271"
    },
    "cidoc:P14_carried_out_by": [
      {"@id": "http://example.org/persons/giovanni"},
      {"@id": "http://example.org/persons/marco"},
      {"@id": "http://example.org/persons/judge_antonio"}
    ],
    "cidoc:P16_used_specific_object": [
      {"@id": "http://example.org/buildings/palazzo_spinola"}
    ]
  }]
}
```

**Key points:**
- All three actors appear under P14_carried_out_by
- Single E7_Activity node represents the arbitration
- Activity is typed as AAT 300417271 (arbitration)
- Building linked via P16_used_specific_object
```

### Step 3.5: Add Workflow Guidance

**In a "Data Entry" or "Workflow" section**, add:

```markdown
## Creating Arbitration Agreements

### Step-by-step workflow:

1. **Create item in Omeka-S**
   - Type: `gmn:E31_3_Arbitration_Agreement`

2. **Add basic information**
   - Name: `gmn:P1_1_has_name`
   - Date: `gmn:P94i_2_has_enactment_date`
   - Notary: `gmn:P94i_1_was_created_by`

3. **Add disputing parties** (2+)
   - Use: `gmn:P70_18_documents_disputing_party`
   - Link to each party involved in dispute

4. **Add arbitrator(s)** (1+)
   - Use: `gmn:P70_19_documents_arbitrator`
   - Link to person/people appointed to arbitrate

5. **Add dispute subject(s)**
   - Use: `gmn:P70_20_documents_dispute_subject`
   - Link to property, debt, right, or other matter in dispute

6. **Add optional details**
   - Place: `gmn:P94i_3_has_place_of_enactment`
   - Archive location: `gmn:P46i_1_is_contained_in`
   - Digital images: `gmn:P138i_1_has_representation`
```

### Step 3.6: Add Quick Reference Table

**In a "Quick Reference" or "Properties" section**, add:

```markdown
## Arbitration Agreement Properties

| Property | Range | Transforms To | Description |
|----------|-------|---------------|-------------|
| P70.18 | E39_Actor | E7 → P14 → Actor | Disputing party |
| P70.19 | E39_Actor | E7 → P14 → Actor | Arbitrator |
| P70.20 | E1_CRM_Entity | E7 → P16 → Entity | Dispute subject |

**Note:** All three properties share the same E7_Activity node in transformed output.
```

### Step 3.7: Save Documentation

**Save the file**: Ctrl+S (or Cmd+S)

**Review for**:
- Consistency with existing documentation style
- Correct formatting (Markdown, headings, code blocks)
- Working internal links (if any)
- Accurate information

✅ **Phase 3 Checkpoint**: Documentation updated with class description, property details, and examples

---

## Phase 4: Testing and Validation

### Overview

In this phase, you'll test the implementation with real data and validate CIDOC-CRM compliance.

**Time estimate**: 20-30 minutes

### Step 4.1: Create Test Data File

Create a file named `test_arbitration.json`:

```json
{
  "@context": {
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "http://example.org/contracts/arb_test_001",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P1_1_has_name": [
    {
      "@value": "Arbitration Agreement - Test Case"
    }
  ],
  "gmn:P70_18_documents_disputing_party": [
    {
      "@id": "http://example.org/persons/giovanni_merchant"
    },
    {
      "@id": "http://example.org/persons/marco_merchant"
    }
  ],
  "gmn:P70_19_documents_arbitrator": [
    {
      "@id": "http://example.org/persons/judge_antonio"
    }
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {
      "@id": "http://example.org/buildings/palazzo_spinola"
    }
  ],
  "gmn:P94i_2_has_enactment_date": [
    {
      "@value": "1450-06-15",
      "@type": "xsd:date"
    }
  ]
}
```

**Save this file** in your project directory.

### Step 4.2: Run Transformation

Execute the transformation script:

```bash
python3 gmn_to_cidoc_transform_script.py test_arbitration.json test_output.json
```

**Expected output**:
```
✓ Transformation complete: test_output.json
```

**If errors occur**, see Troubleshooting section below.

### Step 4.3: Inspect Output File

Open `test_output.json` and verify:

**Check 1: E7_Activity exists**
```json
"cidoc:P70_documents": [{
  "@id": "http://example.org/contracts/arb_test_001/arbitration",
  "@type": "cidoc:E7_Activity",
  ...
}]
```
✅ Should have exactly ONE E7_Activity

**Check 2: Activity is typed**
```json
"cidoc:P2_has_type": {
  "@id": "http://vocab.getty.edu/page/aat/300417271",
  "@type": "cidoc:E55_Type"
}
```
✅ Type should be AAT 300417271

**Check 3: All actors under P14**
```json
"cidoc:P14_carried_out_by": [
  {"@id": "http://example.org/persons/giovanni_merchant", "@type": "cidoc:E39_Actor"},
  {"@id": "http://example.org/persons/marco_merchant", "@type": "cidoc:E39_Actor"},
  {"@id": "http://example.org/persons/judge_antonio", "@type": "cidoc:E39_Actor"}
]
```
✅ Should have THREE actors (2 parties + 1 arbitrator)

**Check 4: Dispute subject under P16**
```json
"cidoc:P16_used_specific_object": [
  {"@id": "http://example.org/buildings/palazzo_spinola", "@type": "cidoc:E1_CRM_Entity"}
]
```
✅ Should have dispute subject

**Check 5: Shortcut properties removed**
```json
// These should NOT appear in output:
"gmn:P70_18_documents_disputing_party"  // ❌ Should be removed
"gmn:P70_19_documents_arbitrator"       // ❌ Should be removed
"gmn:P70_20_documents_dispute_subject"  // ❌ Should be removed
```

### Step 4.4: Validate JSON Structure

Validate the output JSON:

```bash
python3 -m json.tool test_output.json > /dev/null
```

**If successful**: No output
**If errors**: JSON formatting issues

### Step 4.5: Test Edge Cases

Create additional test files:

**Test Case 2: Only disputing parties (no arbitrator yet)**
```json
{
  "@id": "http://example.org/contracts/arb_test_002",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ]
}
```

Run transformation and verify:
- E7_Activity is created
- P14 contains two actors
- No P16 property (since no subject provided)

**Test Case 3: Multiple arbitrators**
```json
{
  "@id": "http://example.org/contracts/arb_test_003",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator1"},
    {"@id": "http://example.org/persons/arbitrator2"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/debts/debt1"}
  ]
}
```

Run transformation and verify:
- P14 contains three actors (1 party + 2 arbitrators)

**Test Case 4: Multiple subjects**
```json
{
  "@id": "http://example.org/contracts/arb_test_004",
  "@type": "gmn:E31_3_Arbitration_Agreement",
  "gmn:P70_18_documents_disputing_party": [
    {"@id": "http://example.org/persons/party1"},
    {"@id": "http://example.org/persons/party2"}
  ],
  "gmn:P70_19_documents_arbitrator": [
    {"@id": "http://example.org/persons/arbitrator1"}
  ],
  "gmn:P70_20_documents_dispute_subject": [
    {"@id": "http://example.org/buildings/building1"},
    {"@id": "http://example.org/debts/debt1"},
    {"@id": "http://example.org/contracts/contract1"}
  ]
}
```

Run transformation and verify:
- P16 contains three entities

### Step 4.6: CIDOC-CRM Compliance Validation

Verify compliance with CIDOC-CRM standards:

**Validation Checklist**:

- [ ] **E7_Activity** is a valid CIDOC-CRM class
- [ ] **P2_has_type** correctly links E7 to E55_Type
- [ ] **P14_carried_out_by** correctly links E7 to E39_Actor
- [ ] **P16_used_specific_object** correctly links E7 to E1_CRM_Entity
- [ ] **P70_documents** correctly links E31 to E7
- [ ] **AAT 300417271** is accessible at Getty AAT

**Test AAT URI accessibility**:
```bash
curl -I http://vocab.getty.edu/page/aat/300417271
```

Should return `HTTP/1.1 200 OK`

### Step 4.7: Formatted Output Review

Pretty-print the output for human review:

```bash
python3 -m json.tool test_output.json
```

Review the formatted output and confirm:
- Structure is logical
- All URIs are valid
- Types are correct
- No malformed JSON

✅ **Phase 4 Checkpoint**: All tests pass, output validates, CIDOC-CRM compliant

---

## Omeka-S Integration

### Overview

After implementing in the ontology and transformation script, you'll want to use the new properties in Omeka-S.# Arbitration Agreement Implementation Guide

**Version:** 1.0  
**Date:** October 26, 2025  
**Estimated Implementation Time:** 60-90 minutes  
**Difficulty Level:** Intermediate

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites and Preparation](#prerequisites-and-preparation)
3. [Understanding the Arbitration Agreement Model](#understanding-the-arbitration-agreement-model)
4. [Implementation Workflow](#implementation-workflow)
5. [Phase 1: Ontology Updates](#phase-1-ontology-updates)
6. [Phase 2: Transformation Script Updates](#phase-2-transformation-script-updates)
7. [Phase 3: Documentation Updates](#phase-3-documentation-updates)
8. [Phase 4: Testing and Validation](#phase-4-testing-and-validation)
9. [Omeka-S Integration](#omeka-s-integration)
10. [Advanced Usage](#advanced-usage)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Reference Materials](#reference-materials)

---

## Introduction

### What Are Arbitration Agreements?

Arbitration agreements are legal contracts that document a specific type of transaction in medieval and early modern commerce: the **transfer of the obligation to resolve a dispute** from the disputing parties to appointed arbitrator(s). In these agreements:

- Two or more parties acknowledge an existing dispute
- They agree to relinquish other forms of dispute resolution (litigation, negotiation, etc.)
- They transfer the authority to resolve the dispute to one or more neutral arbitrators
- All parties commit to accepting the arbitrator's binding decision
- The dispute concerns specific subject matter (property, debts, rights, contracts, etc.)

### Historical Context

In medieval Italian commerce, arbitration was preferred over formal court proceedings because:

1. **Speed**: Arbitration resolved disputes in weeks rather than months or years
2. **Expertise**: Arbitrators often had specialized knowledge of commercial practices
3. **Privacy**: Proceedings could be conducted discreetly
4. **Finality**: Decisions were binding and enforceable
5. **Flexibility**: Parties could choose arbitrators they trusted

### Why This Implementation?

This implementation provides:

- **Semantic accuracy**: Models arbitration as an E7_Activity (joint process) rather than forcing it into acquisition patterns
- **Active agency**: Uses P14_carried_out_by for all parties to reflect that everyone actively participates in the arbitration agreement
- **Flexibility**: Can model various dispute types and subjects
- **Consistency**: Follows the same document → event → actors pattern as sales contracts
- **Extensibility**: Can be enhanced with additional properties in the future

### What You'll Accomplish

By completing this guide, you will:

1. Add one new class to the GMN ontology
2. Add three new properties to the GMN ontology
3. Implement three transformation functions in Python
4. Update project documentation
5. Test the implementation with sample data
6. Validate CIDOC-CRM compliance

---

## Prerequisites and Preparation

### Required Skills

- **Basic RDF/Turtle syntax**: Ability to read and edit Turtle files
- **Basic Python**: Understanding of functions, dictionaries, and lists
- **Text editing**: Comfortable using a text editor or IDE
- **Command line basics**: Ability to run commands in terminal

### Required Software

- **Text editor or IDE** (VS Code, Sublime Text, Atom, or similar)
- **Python 3.6+** installed and accessible from command line
- **RDF validator** (rapper, online validator, or Protégé)
- **Optional**: Git for version control

### Required Files

Locate these files in your project:

- `gmn_ontology.rdf` - Main ontology file
- `gmn_to_cidoc_transform_script.py` - Transformation script
- Main project documentation file (usually Markdown or text)

### Pre-Implementation Checklist

Before you begin, complete these preparation steps:

- [ ] **Backup all files** you'll be modifying
- [ ] **Test current transformation script** to ensure it works
- [ ] **Review existing sales contract implementation** for comparison
- [ ] **Read the semantic documentation** (arbitration-agreement-documentation.md)
- [ ] **Set up test environment** for validation
- [ ] **Clear your workspace** - close unnecessary applications
- [ ] **Allocate uninterrupted time** (60-90 minutes)

### Understanding Your Starting Point

Before implementing, verify:

1. **Ontology version**: Should be 1.3 or higher
2. **Existing contract classes**: Should include E31_1_Contract and E31_2_Sales_Contract
3. **Existing properties**: Should include P70.1 through P70.17
4. **Python script functionality**: Should have working transformation functions

### Creating Backups

Create timestamped backups:

```bash
# Backup ontology
cp gmn_ontology.rdf gmn_ontology.rdf.backup-$(date +%Y%m%d)

# Backup transformation script
cp gmn_to_cidoc_transform_script.py gmn_to_cidoc_transform_script.py.backup-$(date +%Y%m%d)

# Backup documentation
cp main_documentation.md main_documentation.md.backup-$(date +%Y%m%d)
```

---

## Understanding the Arbitration Agreement Model

### Conceptual Overview

The arbitration agreement model treats arbitration as a **collaborative activity** carried out jointly by all parties:

```
┌─────────────────────────────────────────────────────────────┐
│                  Arbitration Agreement                       │
│                  (E31_3_Arbitration_Agreement)              │
└──────────────────────┬──────────────────────────────────────┘
                       │ P70_documents
                       ▼
         ┌─────────────────────────────────┐
         │      Arbitration Activity        │
         │      (E7_Activity)               │
         │      Type: AAT 300417271         │
         └──┬────────────────┬──────────┬───┘
            │                │          │
            │ P14            │ P14      │ P16
            ▼                ▼          ▼
    ┌──────────────┐  ┌──────────┐  ┌──────────────┐
    │ Disputing    │  │Arbitrator│  │   Dispute    │
    │ Parties      │  │          │  │   Subject    │
    │ (Actors)     │  │(Actor)   │  │  (Entity)    │
    └──────────────┘  └──────────┘  └──────────────┘
```

### Key Semantic Decisions

#### Decision 1: E7_Activity vs E8_Acquisition

**Why E7_Activity?**

Arbitration agreements are not property acquisitions. They are legal processes/agreements where parties collaborate to transfer dispute resolution obligations. E7_Activity:

- Is semantically accurate for collaborative processes
- Allows flexible typing (via P2_has_type → AAT)
- Doesn't force the wrong acquisition model
- Better represents the nature of arbitration

**Why not E8_Acquisition?**

E8_Acquisition is specifically for transferring ownership of physical objects. While there is a transfer (of obligations), it's not a property transfer, making E7 more appropriate.

#### Decision 2: P14_carried_out_by for All Parties

**Why P14 for disputing parties AND arbitrators?**

Both disputing parties and arbitrators are **active principals** in the arbitration agreement:

- **Disputing parties**: Actively consent to arbitration, agree to be bound, participate in proceedings
- **Arbitrators**: Actively consent to serve, agree to render decision, conduct the arbitration

This is fundamentally different from passive presence (which would use P11_had_participant).

**Real-world analogy**: Think of arbitration like a mediated negotiation. All parties must actively agree to participate - it's not something done TO them, but something they all DO together.

#### Decision 3: P16_used_specific_object for Dispute Subject

**Why P16?**

The arbitration activity **operates on** the dispute subject. The arbitrators examine it, analyze it, and render a decision about it. P16 captures this operational relationship better than generic reference (P67_refers_to).

### Comparison with Sales Contracts

Understanding the parallel structure helps:

| Element | Sales Contract | Arbitration Agreement |
|---------|---------------|----------------------|
| **What's being transferred?** | Ownership of property | Obligation to resolve dispute |
| **From whom?** | Seller | Disputing parties |
| **To whom?** | Buyer | Arbitrator(s) |
| **Event type** | E8_Acquisition | E7_Activity |
| **Main properties** | P23, P22, P24 | P14 (all), P16 |
| **What changes hands?** | Physical object | Legal obligation |

### The Shared Activity Pattern

All three properties (P70.18, P70.19, P70.20) contribute to **one shared E7_Activity node**:

```turtle
# Input (three separate properties)
<contract> gmn:P70_18_documents_disputing_party <person1>, <person2> .
<contract> gmn:P70_19_documents_arbitrator <person3> .
<contract> gmn:P70_20_documents_dispute_subject <building> .

# Output (single E7_Activity)
<contract> cidoc:P70_documents <contract/arbitration> .
<contract/arbitration> a cidoc:E7_Activity ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300417271> ;
    cidoc:P14_carried_out_by <person1>, <person2>, <person3> ;
    cidoc:P16_used_specific_object <building> .
```

This ensures:
- **Data integrity**: All information about one arbitration stays together
- **Query efficiency**: Easy to retrieve complete arbitration information
- **Logical coherence**: One agreement = one activity
- **Pattern consistency**: Matches sales contract structure

---

## Implementation Workflow

### Overview of Steps

```
Phase 1: Ontology Updates (20-25 minutes)
├── Step 1: Update ontology metadata
├── Step 2: Add E31_3_Arbitration_Agreement class
├── Step 3: Add P70.18 property
├── Step 4: Add P70.19 property
├── Step 5: Add P70.20 property
└── Step 6: Validate RDF syntax

Phase 2: Transformation Script (20-25 minutes)
├── Step 1: Add AAT_ARBITRATION constant
├── Step 2: Add transform_p70_18 function
├── Step 3: Add transform_p70_19 function
├── Step 4: Add transform_p70_20 function
├── Step 5: Update transform_item() calls
└── Step 6: Test Python syntax

Phase 3: Documentation (15-20 minutes)
├── Step 1: Update class hierarchy
├── Step 2: Add property descriptions
├── Step 3: Add examples
└── Step 4: Add workflow guidance

Phase 4: Testing & Validation (20-30 minutes)
├── Step 1: Create test data
├── Step 2: Run transformation
├── Step 3: Validate output
├── Step 4: Test with Omeka-S
└── Step 5: CIDOC-CRM compliance check
```

### Workflow Tips

1. **Work in phases**: Complete each phase before moving to the next
2. **Test frequently**: Validate after each major addition
3. **Keep reference files open**: Have the .ttl and .py files handy
4. **Take breaks**: Step away if you get stuck
5. **Document changes**: Keep notes on what you modified

---

## Phase 1: Ontology Updates

### Overview

In this phase, you will add one class and three properties to the RDF ontology. The additions follow alphabetical ordering and maintain consistency with existing ontology patterns.

**Time estimate**: 20-25 minutes

### Step 1.1: Locate and Open the Ontology File

1. Navigate to your project directory
2. Locate `gmn_ontology.rdf`
3. **Create a backup** (if not already done):
   ```bash
   cp gmn_ontology.rdf gmn_ontology.rdf.backup
   ```
4. Open the file in your text editor

**File structure reminder**:
```
gmn_ontology.rdf
├── Prefixes and namespaces
├── Ontology declaration
├── Classes section (alphabetical)
└── Properties section (alphabetical)
```

### Step 1.2: Update Ontology Metadata

**Location**: Near the top of the file (lines 10-20 approximately)

**Find this section**:
```turtle
<http://www.genoesemerchantnetworks.com/ontology> 
    a owl:Ontology ;
    rdfs:label "Genoese Merchant Networks CIDOC-CRM Extension"@en ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-17"^^xsd:date ;  # OLD DATE
    owl:versionInfo "1.3" ;                      # OLD VERSION
    owl:imports <http://www.cidoc-crm.org/cidoc-crm/> .
```

**Update to**:
```turtle
<http://www.genoesemerchantnetworks.com/ontology> 
    a owl:Ontology ;
    rdfs:label "Genoese Merchant Networks CIDOC-CRM Extension"@en ;
    dcterms:created "2025-10-16"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;  # TODAY'S DATE
    owl:versionInfo "1.4" ;                      # NEW VERSION
    owl:imports <http://www.cidoc-crm.org/cidoc-crm/> .
```

**What changed**:
- `dcterms:modified`: Updated to today's date (2025-10-26)
- `owl:versionInfo`: Incremented from "1.3" to "1.4"

**Why this matters**: Version tracking helps manage changes and dependencies. Other systems may rely on version numbers.

### Step 1.3: Add the Arbitration Agreement Class

**Location**: In the Classes section, after `gmn:E31_2_Sales_Contract` and before `gmn:E74_1_Regional_Provenance`

**Find this marker**:
```turtle
# Class: E31.2 Sales Contract
gmn:E31_2_Sales_Contract
    a owl:Class ;
    # ... properties ...
    .

# Class: E74.1 Regional Provenance  ← INSERT BEFORE THIS
```

**Insert this complete class definition**:
```turtle
# Class: E31.3 Arbitration Agreement
gmn:E31_3_Arbitration_Agreement
    a owl:Class ;
    rdfs:subClassOf gmn:E31_1_Contract ;
    rdfs:label "E31.3 Arbitration Agreement"@en ;
    rdfs:comment "Specialized class that describes arbitration agreement documents. This is a specialized type of gmn:E31_1_Contract used to represent legal documents that record the agreement between disputing parties to transfer the obligation to resolve their dispute to one or more arbitrators. In this transaction, two or more parties involved in a conflict agree to relinquish their right to pursue other forms of dispute resolution and instead accept the binding decision of the appointed arbitrator(s). The contract documents both the transfer of the dispute resolution obligation from the parties to the arbitrator(s) and the agreement by the parties to be bound by the arbitrator's decision. This represents a transfer of legal obligations similar to how sales contracts represent transfers of ownership rights. Instances of this class represent the physical or conceptual document itself, while the actual arbitration activity is modeled through E7_Activity that the document documents (via P70_documents)."@en ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso gmn:E31_1_Contract, cidoc:E7_Activity, cidoc:P70_documents .
```

**Understanding the class definition**:

- `a owl:Class`: Declares this as an OWL class
- `rdfs:subClassOf gmn:E31_1_Contract`: Inherits from general contract class
- `rdfs:label`: Human-readable name
- `rdfs:comment`: Detailed description of purpose and usage
- `dcterms:created`: Original creation date
- `dcterms:modified`: Last modification date
- `rdfs:seeAlso`: Related classes for reference

**Common mistakes to avoid**:
- ❌ Forgetting the period (.) at the end
- ❌ Wrong indentation (use spaces, not tabs)
- ❌ Missing the subClassOf declaration
- ❌ Incorrect URIs in rdfs:seeAlso

### Step 1.4: Add Property P70.18 (Disputing Party)

**Location**: In the Properties section, after `gmn:P70_17_documents_sale_price_currency` and before `gmn:P94i_1_was_created_by`

**Find this marker**:
```turtle
# Property: P70.17 documents sale price currency
gmn:P70_17_documents_sale_price_currency
    # ... properties ...
    .

# Property: P94i.1 was created by  ← INSERT BEFORE THIS
```

**Insert this complete property definition**:
```turtle
# Property: P70.18 documents disputing party
gmn:P70_18_documents_disputing_party
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.18 documents disputing party"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with a party involved in the dispute. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Disputing parties are the active principals who have agreed to submit their dispute to arbitration and are carrying out the arbitration agreement alongside the arbitrator(s)."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

**Understanding the property definition**:

- `a owl:ObjectProperty`: This property links to other resources (not literals)
- `a rdf:Property`: Also declares it as an RDF property
- `rdfs:label`: Short human-readable name
- `rdfs:comment`: Detailed explanation including transformation path
- `rdfs:subPropertyOf cidoc:P70_documents`: Inherits from CIDOC-CRM P70
- `rdfs:domain`: Can only be used on E31_3_Arbitration_Agreement
- `rdfs:range`: Must link to E39_Actor or subclass
- `rdfs:seeAlso`: Related properties in transformation path

**Key points**:
- The comment explicitly states the full CIDOC-CRM path
- Emphasizes that disputing parties are "active principals"
- References AAT 300417271 for typing
- Notes that it should be transformed for compliance

### Step 1.5: Add Property P70.19 (Arbitrator)

**Location**: Immediately after P70.18

**Insert this complete property definition**:
```turtle
# Property: P70.19 documents arbitrator
gmn:P70_19_documents_arbitrator
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.19 documents arbitrator"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with the person or persons appointed to resolve the dispute. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P14_carried_out_by > E39_Actor. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. Arbitrators are the neutral third parties who will hear the dispute and render a binding decision."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E39_Actor ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P14_carried_out_by .
```

**Similarities with P70.18**:
- Same domain (E31_3_Arbitration_Agreement)
- Same range (E39_Actor)
- Same transformation path (→ E7 → P14)
- Same typing (AAT 300417271)

**Differences from P70.18**:
- Describes arbitrators rather than disputing parties
- Emphasizes "neutral third parties"
- Notes "render a binding decision"

### Step 1.6: Add Property P70.20 (Dispute Subject)

**Location**: Immediately after P70.19

**Insert this complete property definition**:
```turtle
# Property: P70.20 documents dispute subject
gmn:P70_20_documents_dispute_subject
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P70.20 documents dispute subject"@en ;
    rdfs:comment "Simplified property for associating an arbitration agreement with the subject matter of the dispute being arbitrated. Represents the full CIDOC-CRM path: E31_Document > P70_documents > E7_Activity > P16_used_specific_object > E1_CRM_Entity. The E7_Activity should be typed as an arbitration agreement (AAT 300417271). This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The dispute subject can be any entity - a property (E18_Physical_Thing), a legal right (E72_Legal_Object), a debt, a contract claim, or any other matter in contention."@en ;
    rdfs:subPropertyOf cidoc:P70_documents ;
    rdfs:domain gmn:E31_3_Arbitration_Agreement ;
    rdfs:range cidoc:E1_CRM_Entity ;
    dcterms:created "2025-10-17"^^xsd:date ;
    dcterms:modified "2025-10-26"^^xsd:date ;
    rdfs:seeAlso cidoc:P70_documents, cidoc:P16_used_specific_object .
```

**Key differences from P70.18/P70.19**:

- **Different transformation path**: Uses P16_used_specific_object instead of P14
- **Broader range**: E1_CRM_Entity (anything) instead of E39_Actor
- **Different semantic**: The dispute subject is operated on, not a participant

**Why P16 instead of P14?**

The dispute subject is not carrying out the arbitration - it's the thing being arbitrated about. P16 captures this "object of activity" relationship.

### Step 1.7: Save and Perform Initial Validation

**Save the file**: Use Ctrl+S (or Cmd+S on Mac)

**Validate RDF syntax**:

Option 1: Using rapper (command line tool)
```bash
rapper -i turtle -o turtle gmn_ontology.rdf > /dev/null
```

If successful, you'll see no output. If there are errors, they'll be displayed.

Option 2: Using an online validator
1. Go to http://www.w3.org/RDF/Validator/
2. Upload your gmn_ontology.rdf file
3. Review results

Option 3: Using Protégé
1. Open Protégé
2. File → Open → Select gmn_ontology.rdf
3. Check for errors in the bottom panel

**Common validation errors and fixes**:

Error: "Unexpected end of file"
- **Cause**: Missing period (.) at end of definition
- **Fix**: Add period after last property in class/property definition

Error: "Undefined prefix"
- **Cause**: Missing namespace declaration
- **Fix**: Ensure all prefixes (gmn:, cidoc:, etc.) are declared at top of file

Error: "Invalid URI"
- **Cause**: Malformed URI or missing angle brackets
- **Fix**: Check that all URIs are properly formatted with < >

### Step 1.8: Visual Check of Ontology Structure

Before moving on, verify the structure:

**Check 1: Class hierarchy is correct**
```turtle
# Should see this structure in Classes section:
E31_1_Contract
  └── E31_2_Sales_Contract
  └── E31_3_Arbitration_Agreement  ← NEW
```

**Check 2: Properties are in order**
```turtle
# Should see this sequence in Properties section:
P70_16_documents_sale_price_amount
P70_17_documents_sale_price_currency
P70_18_documents_disputing_party      ← NEW
P70_19_documents_arbitrator          ← NEW
P70_20_documents_dispute_subject     ← NEW
P94i_1_was_created_by
```

**Check 3: All dates are consistent**
- ontology modified: 2025-10-26
- class created: 2025-10-17
- class modified: 2025-10-26
- properties created: 2025-10-17
- properties modified: 2025-10-26

✅ **Phase 1 Checkpoint**: Ontology file updated with 1 class and 3 properties, all validated

---

## Phase 2: Transformation Script Updates

### Overview

In this phase, you will add Python code to transform the shortcut properties into full CIDOC-CRM structures. You'll add one constant and three transformation functions.

**Time estimate**: 20-25 minutes

### Understanding the Transformation Pattern

All three transformation functions follow the same basic pattern:

```python
def transform_property(data):
    # 1. Check if property exists
    if 'gmn:property_name' not in data:
        return data
    
    # 2. Get property values
    values = data['gmn:property_name']
    
    # 3. Find or create E7_Activity
    activity = get_or_create_activity(data)
    
    # 4. Initialize target property in activity
    if 'cidoc:target_property' not in activity:
        activity['cidoc:target_property'] = []
    
    # 5. Add values to activity
    for value in values:
        activity['cidoc:target_property'].append(process_value(value))
    
    # 6. Remove shortcut property
    del data['gmn:property_name']
    
    return data
```

The key insight: **All three functions share the same E7_Activity node**.

### Step 2.1: Locate and Open the Transformation Script

1. Navigate to your project directory
2. Locate `gmn_to_cidoc_transform_script.py`
3. **Create a backup** (if not already done):
   ```bash
   cp gmn_to_cidoc_transform_script.py gmn_to_cidoc_transform_script.py.backup
   ```
4. Open the file in your text editor

**File structure reminder**:
```python
# Imports
from uuid import uuid4
import json
# etc.

# Constants
AAT_NAME = "http://..."
AAT_WITNESS = "http://..."
# etc.

# Transformation functions
def transform_p1_1_has_name(data):
    # ...

# ... more functions ...

def transform_item(item, include_internal=False):
    # Calls all transformation functions
    # ...

def main():
    # Command-line interface
    # ...
```

### Step 2.2: Add the AAT_ARBITRATION Constant

**Location**: In the constants section, after `AAT_WITNESS` and before the first function definition

**Find this section** (around lines 30-60):
```python
# Getty AAT URI for witnesses
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"

# ← INSERT HERE

def transform_p1_1_has_name(data):
```

**Insert this line**:
```python
# Getty AAT URI for arbitration (process)
AAT_ARBITRATION = "http://vocab.getty.edu/page/aat/300417271"
```

**Complete section should look like**:
```python
# Getty AAT URI for witnesses
AAT_WITNESS = "http://vocab.getty.edu/page/aat/300028910"
# Getty AAT URI for arbitration (process)
AAT_ARBITRATION = "http://vocab.getty.edu/page/aat/300417271"

def transform_p1_1_has_name(data):
```

**Why this constant?**
- Avoids hardcoding the URI multiple times
- Makes updates easier if AAT changes
- Improves code readability
- Follows existing pattern in the script

### Step 2.3: Locate the Function Insertion Point

**Find the section** for arbitration agreement functions or sales contract functions.

Look for comments like:
```python
# Sales Contract transformation functions
# ... functions ...

# ← INSERT ARBITRATION FUNCTIONS HERE

def transform_item(item, include_internal=False):
```

If there's already a section labeled "# Arbitration Agreement transformation functions", add there. Otherwise, create the section.

### Step 2.4: Add Function Header Comment

**Insert this comment**:
```python
# ============================================================================
# Arbitration Agreement transformation functions
# ============================================================================
```

This helps organize the code and makes it clear where arbitration functions begin.

### Step 2.5: Add transform_p70_18_documents_disputing_party Function

**Insert this complete function**:

```python
def transform_p70_18_documents_disputing_party(data):
    """
    Transform gmn:P70_18_documents_disputing_party to full CIDOC-CRM structure:
    P70_documents > E7_Activity > P14_carried_out_by > E39_Actor
    
    This function creates or locates an E7_Activity node typed as an arbitration
    agreement and adds disputing parties to it via P14_carried_out_by. Disputing
    parties are the active principals who have agreed to submit their dispute to
    arbitration.
    
    Args:
        data: The item data dictionary (JSON-LD structure)
    
    Returns:
        Modified data dictionary with shortcut property transformed
    
    Example:
        Input:  {'gmn:P70_18_documents_disputing_party': [{'@id': 'person1'}]}
        Output: {'cidoc:P70_documents': [{'@type': 'cidoc:E7_Activity', ...}]}
    """
    # Step 1: Check if property exists in data
    if 'gmn:P70_18_documents_disputing_party' not in data:
        return data
    
    # Step 2: Get the property values (array of parties)
    parties = data['gmn:P70_18_documents_disputing_party']
    subject_uri = data.get('@id', f"urn:uuid:{uuid4()}")
    
    # Step 3: Check if arbitration activity already exists
    existing_activity = None
    if 'cidoc:P70_documents' in data and len(data['cidoc:P70_documents']) > 0:
        # Use existing arbitration activity
        existing_activity = data['cidoc:P70_documents'][0]
    else:
        # Create new arbitration activity
        activity_uri = f"{subject_uri}/arbitration"
        existing_activity = {
            '@id': activity_uri,
            '@type': 'cidoc:E7_Activity',
            'cidoc:P2_has_type': {
                '@id': AAT_ARBITRATION,
                '@type': 'cidoc:E55_Type'
            }
        }
        data['cidoc:P70_