# GMN P3.1 has editorial note - Implementation Guide

**Property:** `gmn:P3_1_has_editorial_note`  
**Document Version:** 1.0  
**Date:** October 26, 2025  
**Status:** ✅ Already Implemented

---

## Table of Contents

1. [Implementation Status](#implementation-status)
2. [Verification Steps](#verification-steps)
3. [Testing the Property](#testing-the-property)
4. [Usage Instructions](#usage-instructions)
5. [Transformation Testing](#transformation-testing)
6. [Common Scenarios](#common-scenarios)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## Implementation Status

### Current Status: ✅ FULLY IMPLEMENTED

The `gmn:P3_1_has_editorial_note` property is **already implemented** in:

1. ✅ **Ontology File** (`gmn_ontology.ttl`) - Line containing property definition
2. ✅ **Transformation Script** (`gmn_to_cidoc_transform.py`) - Function `transform_p3_1_has_editorial_note`
3. ✅ **AAT Constants** - `AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/aat/300456627"`

**No new code installation is required.** This guide helps you verify and use the existing implementation.

---

## Verification Steps

### Step 1: Verify Ontology Definition

**File:** `gmn_ontology.ttl`

**Search for:** `gmn:P3_1_has_editorial_note`

**Expected Content:**
```turtle
# Property: P3.1 has editorial note
gmn:P3_1_has_editorial_note 
    a owl:DatatypeProperty ;
    a rdf:Property ;
    rdfs:label "P3.1 has editorial note"@en ;
    rdfs:comment "Simplified property for expressing editorial notes, comments, and internal documentation about an entity. Represents the full CIDOC-CRM path: P67i_is_referred_to_by > E33_Linguistic_Object > P2_has_type <http://vocab.getty.edu/aat/300456627> > P190_has_symbolic_content. This property is provided as a convenience for data entry and should be transformed to the full CIDOC-CRM structure for formal compliance. The linguistic object type is automatically set to AAT 300456627. This property is intended for internal project use and may be excluded from public data exports."@en ;
    rdfs:subPropertyOf cidoc:P3_has_note ;
    rdfs:domain cidoc:E1_CRM_Entity ;
    rdfs:range cidoc:E62_String ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P3_has_note, cidoc:P67i_is_referred_to_by, cidoc:P190_has_symbolic_content, aat:300456627 ;
    gmn:hasImplicitType aat:300456627 ;
    gmn:isInternalOnly true .
```

**✓ Verification:** Confirm all lines are present and correct.

---

### Step 2: Verify AAT Constant

**File:** `gmn_to_cidoc_transform.py`

**Search for:** `AAT_EDITORIAL_NOTE`

**Expected Content:**
```python
# Getty AAT URI constants
AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/aat/300456627"
```

**✓ Verification:** Confirm the constant is defined near the top of the file.

---

### Step 3: Verify Transformation Function

**File:** `gmn_to_cidoc_transform.py`

**Search for:** `def transform_p3_1_has_editorial_note`

**Expected Content:**
```python
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
```

**✓ Verification:** Confirm the function exists and matches this structure.

---

### Step 4: Verify Integration in Transform Pipeline

**File:** `gmn_to_cidoc_transform.py`

**Search for:** The call to `transform_p3_1_has_editorial_note` in the `transform_item` function

**Expected Location:** Near the end of the transformation pipeline

**Expected Content:**
```python
def transform_item(data, include_internal=False):
    """Transform a single item with all applicable transformations."""
    # ... other transformations ...
    
    # Editorial notes (last, with optional inclusion)
    item = transform_p3_1_has_editorial_note(item, include_internal)
    
    return item
```

**✓ Verification:** Confirm the function is called with the `include_internal` parameter.

---

## Testing the Property

### Test 1: Create Sample Data

Create a test JSON-LD file: `test_editorial_note.json`

```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@graph": [
    {
      "@id": "http://example.org/person/test_001",
      "@type": "cidoc:E21_Person",
      "gmn:P1_1_has_name": [
        {"@value": "Giovanni Rossi"}
      ],
      "gmn:P3_1_has_editorial_note": [
        {"@value": "This is a test editorial note. The person's identity requires verification."}
      ]
    }
  ]
}
```

---

### Test 2: Transform Without Internal Flag (Default)

**Command:**
```bash
python gmn_to_cidoc_transform.py test_editorial_note.json output_public.json
```

**Expected Output Message:**
```
Note: Excluding internal editorial notes from output
✓ Transformation complete: output_public.json
```

**Expected Result in `output_public.json`:**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@graph": [
    {
      "@id": "http://example.org/person/test_001",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@id": "http://example.org/person/test_001/appellation/12345678",
          "@type": "cidoc:E41_Appellation",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/aat/300404650",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P190_has_symbolic_content": "Giovanni Rossi"
        }
      ]
    }
  ]
}
```

**✓ Test Pass Criteria:** The editorial note is **completely removed** from the output.

---

### Test 3: Transform With Internal Flag

**Command:**
```bash
python gmn_to_cidoc_transform.py test_editorial_note.json output_internal.json --include-internal
```

**Expected Output Message:**
```
Note: Including internal editorial notes in output
✓ Transformation complete: output_internal.json
```

**Expected Result in `output_internal.json`:**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://www.genoesemerchantnetworks.com/ontology#",
    "aat": "http://vocab.getty.edu/aat/"
  },
  "@graph": [
    {
      "@id": "http://example.org/person/test_001",
      "@type": "cidoc:E21_Person",
      "cidoc:P1_is_identified_by": [
        {
          "@id": "http://example.org/person/test_001/appellation/12345678",
          "@type": "cidoc:E41_Appellation",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/aat/300404650",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P190_has_symbolic_content": "Giovanni Rossi"
        }
      ],
      "cidoc:P67i_is_referred_to_by": [
        {
          "@id": "http://example.org/person/test_001/note/87654321",
          "@type": "cidoc:E33_Linguistic_Object",
          "cidoc:P2_has_type": {
            "@id": "http://vocab.getty.edu/aat/300456627",
            "@type": "cidoc:E55_Type"
          },
          "cidoc:P190_has_symbolic_content": "This is a test editorial note. The person's identity requires verification."
        }
      ]
    }
  ]
}
```

**✓ Test Pass Criteria:** The editorial note is **transformed** to full CIDOC-CRM structure.

---

## Usage Instructions

### Adding Editorial Notes in Omeka-S

1. **Navigate to Item** - Open the entity you want to annotate
2. **Add Property** - Find "P3.1 has editorial note" in the property list
3. **Enter Note** - Type your editorial comment
4. **Save** - Save the item

**Example Values:**
- "Name spelling varies between 'Giacomo' and 'Jacopo' in different sources."
- "Date uncertain. Archive records damaged but context suggests 1450-1455."
- "Identity tentative. Requires cross-reference with port records."
- "Property location modern-day Serra Riccò, frazione of Vignolo."

---

### Adding Editorial Notes Programmatically

**Python Example:**
```python
import json

# Load existing data
with open('data.json', 'r') as f:
    data = json.load(f)

# Add editorial note to an entity
entity = data['@graph'][0]
entity['gmn:P3_1_has_editorial_note'] = [
    {"@value": "This entity requires further verification."}
]

# Save
with open('data_with_notes.json', 'w') as f:
    json.dump(data, f, indent=2)
```

---

### Adding Multiple Notes

Multiple notes can be added to a single entity:

```json
{
  "@id": "http://example.org/person/giovanni_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Giovanni da Genova"}],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Primary source: Notarial contract ASG, Not. 123, f. 45r"},
    {"@value": "Name variant 'Iohanes de Ianua' appears in Latin documents"},
    {"@value": "Possible relation to Giovanni Spinola - requires investigation"}
  ]
}
```

Each note will be transformed to a separate E33_Linguistic_Object.

---

## Transformation Testing

### Testing Checklist

- [ ] **Test 1:** Transform without `--include-internal` flag
  - Verify editorial notes are removed
  - Verify other properties transform correctly
  - Verify no errors occur

- [ ] **Test 2:** Transform with `--include-internal` flag
  - Verify editorial notes transform to E33_Linguistic_Object
  - Verify P2_has_type points to aat:300456627
  - Verify P190_has_symbolic_content contains note text
  - Verify unique URIs are generated for each note

- [ ] **Test 3:** Entity with multiple editorial notes
  - Verify all notes are transformed/removed consistently
  - Verify each note gets unique URI

- [ ] **Test 4:** Different entity types
  - Test on cidoc:E21_Person
  - Test on gmn:E31_2_Sales_Contract
  - Test on cidoc:E53_Place
  - Verify property works on all E1_CRM_Entity subclasses

---

## Common Scenarios

### Scenario 1: Documenting Source Uncertainty

**Use Case:** A person's name spelling varies across sources

**Input:**
```json
{
  "@id": "http://example.org/person/giacomo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Giacomo Spinola"}],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Name appears as 'Iacopo Spinola' in ASG Not. 234, f. 12v. Both spellings refer to same individual based on patronymic and property references."}
  ]
}
```

---

### Scenario 2: Flagging Items for Review

**Use Case:** Preliminary data entry requiring verification

**Input:**
```json
{
  "@id": "http://example.org/contract/sale_045",
  "@type": "gmn:E31_2_Sales_Contract",
  "gmn:P102_1_has_title": [{"@value": "Sale of vineyard"}],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "NEEDS REVIEW: Sale price illegible in source. Tentatively recorded as 100 lire based on context."}
  ]
}
```

---

### Scenario 3: Recording Modern Context

**Use Case:** Connecting historical place to modern location

**Input:**
```json
{
  "@id": "http://example.org/place/vignolo",
  "@type": "cidoc:E53_Place",
  "gmn:P1_1_has_name": [{"@value": "Vignolo"}],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Modern location: frazione of Serra Riccò, province of Genoa. GPS: 44.4833°N, 8.9167°E"}
  ]
}
```

---

### Scenario 4: Explaining Editorial Decisions

**Use Case:** Document why certain interpretation was chosen

**Input:**
```json
{
  "@id": "http://example.org/person/bartolomeo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": [{"@value": "Bartolomeo de Vignolo"}],
  "gmn:P1_4_has_loconym": [{"@id": "http://example.org/place/vignolo"}],
  "gmn:P3_1_has_editorial_note": [
    {"@value": "Loconym 'de Vignolo' interpreted as place of origin rather than property ownership based on comparative analysis of naming patterns in this archive."}
  ]
}
```

---

## Troubleshooting

### Issue 1: Editorial Notes Appearing in Public Export

**Symptom:** Notes marked as internal appear in public JSON-LD export

**Cause:** Missing or incorrect `--include-internal` flag handling

**Solution:**
1. Verify transformation command does NOT include `--include-internal` flag
2. Check that `transform_p3_1_has_editorial_note` function is called in transform pipeline
3. Verify the function's `include_internal` parameter defaults to `False`

**Verification:**
```bash
# Public export should NOT have --include-internal
python gmn_to_cidoc_transform.py input.json public.json

# Check output - should have NO cidoc:P67i_is_referred_to_by with aat:300456627
```

---

### Issue 2: Editorial Notes Not Transforming with --include-internal

**Symptom:** Notes are removed even when `--include-internal` flag is used

**Cause:** Flag not being passed to transformation function

**Solution:**
1. Check main() function passes flag correctly to transform_export()
2. Check transform_export() passes flag to transform_item()
3. Check transform_item() passes flag to transform_p3_1_has_editorial_note()

**Debug:**
```python
# Add debug print in transform_p3_1_has_editorial_note:
def transform_p3_1_has_editorial_note(data, include_internal=False):
    print(f"DEBUG: include_internal={include_internal}")  # Add this line
    if 'gmn:P3_1_has_editorial_note' not in data:
        return data
```

---

### Issue 3: Invalid URI Generated for Notes

**Symptom:** Note URIs are malformed or not unique

**Cause:** Subject URI missing or hash collision

**Solution:**
1. Ensure entity has valid `@id` field
2. Check hash function generating 8-character suffix
3. Verify URI pattern: `{subject_uri}/note/{hash}`

**Example Fix:**
```python
# Correct pattern
note_hash = str(hash(note_value))[-8:]
note_uri = f"{subject_uri}/note/{note_hash}"
```

---

### Issue 4: AAT Type Not Being Applied

**Symptom:** Transformed notes missing P2_has_type or wrong type URI

**Cause:** AAT_EDITORIAL_NOTE constant incorrect or not used

**Solution:**
1. Verify constant: `AAT_EDITORIAL_NOTE = "http://vocab.getty.edu/aat/300456627"`
2. Check it's used in transformation:
```python
'cidoc:P2_has_type': {
    '@id': AAT_EDITORIAL_NOTE,  # Must use constant
    '@type': 'cidoc:E55_Type'
}
```

---

## Advanced Usage

### Filtering Notes by Content

**Python script to extract all editorial notes:**

```python
import json

def extract_editorial_notes(input_file, output_file):
    """Extract all editorial notes from a JSON-LD file."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    notes = []
    for item in data.get('@graph', [data]):
        item_id = item.get('@id', 'Unknown')
        item_type = item.get('@type', 'Unknown')
        
        if 'gmn:P3_1_has_editorial_note' in item:
            for note_obj in item['gmn:P3_1_has_editorial_note']:
                note_text = note_obj.get('@value', str(note_obj))
                notes.append({
                    'entity_id': item_id,
                    'entity_type': item_type,
                    'note': note_text
                })
    
    with open(output_file, 'w') as f:
        json.dump(notes, f, indent=2)
    
    print(f"Extracted {len(notes)} editorial notes to {output_file}")

# Usage
extract_editorial_notes('data.json', 'editorial_notes_report.json')
```

---

### Batch Adding Notes

**Python script to add standard note to entities matching criteria:**

```python
import json

def add_note_to_entities(input_file, output_file, entity_type, note_text):
    """Add editorial note to all entities of specified type."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    count = 0
    for item in data.get('@graph', [data]):
        if item.get('@type') == entity_type:
            if 'gmn:P3_1_has_editorial_note' not in item:
                item['gmn:P3_1_has_editorial_note'] = []
            
            item['gmn:P3_1_has_editorial_note'].append(
                {"@value": note_text}
            )
            count += 1
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added note to {count} entities of type {entity_type}")

# Usage
add_note_to_entities(
    'data.json',
    'data_with_notes.json',
    'cidoc:E21_Person',
    'Requires biographical research in parish records.'
)
```

---

### Validating Note Content

**Python script to check for common issues:**

```python
import json
import re

def validate_editorial_notes(input_file):
    """Validate editorial notes for common issues."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    issues = []
    
    for item in data.get('@graph', [data]):
        item_id = item.get('@id', 'Unknown')
        
        if 'gmn:P3_1_has_editorial_note' in item:
            for idx, note_obj in enumerate(item['gmn:P3_1_has_editorial_note']):
                note = note_obj.get('@value', str(note_obj))
                
                # Check for empty notes
                if not note.strip():
                    issues.append(f"{item_id}: Note {idx} is empty")
                
                # Check for very short notes (might be incomplete)
                if len(note.strip()) < 10:
                    issues.append(f"{item_id}: Note {idx} is very short: '{note}'")
                
                # Check for all caps (might be placeholder)
                if note.isupper():
                    issues.append(f"{item_id}: Note {idx} is all caps: '{note}'")
                
                # Check for placeholder text
                placeholders = ['TODO', 'TBD', 'FIXME', 'XXX']
                if any(p in note.upper() for p in placeholders):
                    issues.append(f"{item_id}: Note {idx} contains placeholder: '{note}'")
    
    if issues:
        print("Found issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All editorial notes validated successfully!")
    
    return issues

# Usage
validate_editorial_notes('data.json')
```

---

## Next Steps

After implementing and testing `gmn:P3_1_has_editorial_note`:

1. **Update Documentation** - Add examples to main GMN documentation using content from `has-editorial-note-doc-note.txt`

2. **Establish Workflow** - Create guidelines for when and how team members should use editorial notes

3. **Training** - Train data entry personnel on proper use of editorial notes

4. **Regular Review** - Periodically extract and review editorial notes to identify patterns and improve data quality

5. **Export Protocols** - Establish clear protocols for when to include or exclude internal notes in different export contexts

---

## Summary

The `gmn:P3_1_has_editorial_note` property is fully implemented and ready to use. This guide provides:

- ✅ Verification steps to confirm implementation
- ✅ Testing procedures for both public and internal exports
- ✅ Usage examples for common scenarios
- ✅ Troubleshooting guidance for common issues
- ✅ Advanced scripts for batch operations and validation

**Key Takeaway:** This property enables rich internal documentation while maintaining clean public exports through the `--include-internal` flag mechanism.

---

**Document Version:** 1.0  
**Date:** October 26, 2025  
**Property:** gmn:P3_1_has_editorial_note
