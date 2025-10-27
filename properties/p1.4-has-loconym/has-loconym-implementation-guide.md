# gmn:P1_4_has_loconym - Implementation Guide

**Version:** 1.0  
**Last Updated:** October 2025  
**Status:** Property Already Implemented

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Understanding the Implementation](#understanding-the-implementation)
4. [Data Entry Guidelines](#data-entry-guidelines)
5. [Transformation Process](#transformation-process)
6. [Testing Procedures](#testing-procedures)
7. [Integration with Other Properties](#integration-with-other-properties)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Introduction

### Purpose of This Guide

This implementation guide provides step-by-step instructions for **using** the `gmn:P1_4_has_loconym` property, which is **already implemented** in your GMN ontology. Unlike other deliverables packages that contain new code to add, this guide focuses on:

- Understanding the existing implementation
- Using the property correctly in data entry
- Validating that transformations work properly
- Troubleshooting common issues

### What is Already Done

✅ **Ontology Definition** - Property defined in `gmn_ontology.ttl` (lines 183-196)  
✅ **Python Transformation** - Function exists in `gmn_to_cidoc_transform.py` (lines 154-186)  
✅ **Type System** - Wikidata Q17143070 (loconym) integrated

### What This Guide Covers

📖 **Documentation** - How to document this property in your project  
🎯 **Usage** - How to apply this property to your data  
✅ **Testing** - How to verify it works correctly  
🔧 **Troubleshooting** - How to resolve common issues

---

## Prerequisites

### Knowledge Requirements

- Basic understanding of RDF/Turtle syntax
- Familiarity with CIDOC-CRM structure
- Knowledge of JSON-LD format (for transformation testing)
- Understanding of medieval Italian naming conventions (helpful but not required)

### Technical Requirements

- Access to `gmn_ontology.ttl` file
- Access to `gmn_to_cidoc_transform.py` script
- Python 3.6 or higher (for transformation testing)
- Text editor for reviewing code
- Sample data for testing

### Files You'll Need

```
project/
├── gmn_ontology.ttl                    # Contains property definition
├── gmn_to_cidoc_transform.py           # Contains transformation function
├── has-loconym-documentation.md        # Semantic documentation (this package)
├── has-loconym-doc-note.txt           # Usage examples (this package)
└── test_data/                         # Your sample data for testing
    └── person_with_loconym.jsonld     # Example test file
```

---

## Understanding the Implementation

### Step 1: Locate the Ontology Definition

Open `gmn_ontology.ttl` and find the property definition (around line 183):

```turtle
# Property: P1.4 has loconym
gmn:P1_4_has_loconym
    a owl:ObjectProperty ;
    a rdf:Property ;
    rdfs:label "P1.4 has loconym"@en ;
    rdfs:comment "Simplified property for expressing a place referenced in a 
                  person's name (loconym), indicating that the person or their 
                  ancestors originated from that place. Represents the full 
                  CIDOC-CRM path: P1_is_identified_by > E41_Appellation > 
                  P2_has_type <https://www.wikidata.org/wiki/Q17143070> > 
                  P67_refers_to > E53_Place. This captures toponymic naming 
                  patterns common in medieval Italian contexts (e.g., 'Giovanni 
                  da Genova', 'Bartolomeo de Vignolo'). This property is provided 
                  as a convenience for data entry and should be transformed to the 
                  full CIDOC-CRM structure for formal compliance. The appellation 
                  type is automatically set to Wikidata Q17143070 (loconym)."@en ;
    rdfs:subPropertyOf cidoc:P1_is_identified_by ;
    rdfs:domain cidoc:E21_Person ;
    rdfs:range cidoc:E53_Place ;
    dcterms:created "2025-10-16"^^xsd:date ;
    rdfs:seeAlso cidoc:P1_is_identified_by, cidoc:P67_refers_to, 
                 <https://www.wikidata.org/wiki/Q17143070> ;
    gmn:hasImplicitType <https://www.wikidata.org/wiki/Q17143070> .
```

### Step 2: Understand the Key Components

| Component | Value | Meaning |
|-----------|-------|---------|
| **Type** | `owl:ObjectProperty` | Links to another resource (not literal) |
| **Domain** | `cidoc:E21_Person` | Applied to persons only |
| **Range** | `cidoc:E53_Place` | Must link to a place |
| **Supertype** | `cidoc:P1_is_identified_by` | Is a subtype of identification |
| **Implicit Type** | Wikidata Q17143070 | Automatically sets loconym type |

### Step 3: Locate the Transformation Function

Open `gmn_to_cidoc_transform.py` and find the function (around line 154):

```python
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
```

### Step 4: Verify the Constant

Check that `WIKIDATA_LOCONYM` is defined at the top of the file (around line 27):

```python
WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"
```

### Step 5: Confirm Integration in Main Transform

Verify that the function is called in the `transform_item()` function (around line 840):

```python
def transform_item(item, include_internal=False):
    """Transform all shortcut properties in an item."""
    # ... other transformations ...
    item = transform_p1_4_has_loconym(item)
    # ... more transformations ...
```

---

## Data Entry Guidelines

### When to Use This Property

Use `gmn:P1_4_has_loconym` when:

✅ A person's name includes a **place reference** indicating origin  
✅ The place component is part of their **formal identification**  
✅ You want to **link the person to the place** semantically  
✅ You're documenting **medieval Italian naming patterns**

### When NOT to Use This Property

❌ For modern-style addresses or residences → Use location properties  
❌ For places mentioned in documents → Use `P70_13_documents_referenced_place`  
❌ For regional group membership → Use `P107i_1_has_regional_provenance`  
❌ For document creation places → Use `P94i_3_has_place_of_enactment`

### Data Entry Formats

#### Format 1: URI Reference (Recommended)
```turtle
<person_giovanni> a cidoc:E21_Person ;
    gmn:P1_4_has_loconym <place_genova> .

<place_genova> a cidoc:E53_Place ;
    rdfs:label "Genoa"@en .
```

#### Format 2: JSON-LD with Object
```json
{
  "@id": "http://example.org/person/giovanni",
  "@type": "cidoc:E21_Person",
  "gmn:P1_4_has_loconym": {
    "@id": "http://example.org/place/genova"
  }
}
```

#### Format 3: JSON-LD with String URI
```json
{
  "@id": "http://example.org/person/bartolomeo",
  "@type": "cidoc:E21_Person",
  "gmn:P1_4_has_loconym": "http://example.org/place/vignolo"
}
```

### Multiple Loconyms

A person can have multiple loconyms if they moved or had complex origins:

```turtle
<person_maria> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Maria da Venezia e Genova" ;
    gmn:P1_4_has_loconym <place_venice> , <place_genoa> .
```

This will create two separate E41_Appellation resources, one for each place.

---

## Transformation Process

### How Transformation Works

The transformation follows this logic:

```
1. Check if gmn:P1_4_has_loconym exists in data
   ├─ No → Return data unchanged
   └─ Yes → Continue to step 2

2. Extract place URI(s) from property value
   
3. For each place:
   ├─ Generate unique appellation URI
   ├─ Create E41_Appellation resource
   ├─ Set type to Wikidata Q17143070
   ├─ Add P67_refers_to pointing to place
   └─ Add appellation to P1_is_identified_by

4. Remove gmn:P1_4_has_loconym property

5. Return transformed data
```

### Transformation Example

**Input Data (JSON-LD):**
```json
{
  "@id": "http://example.org/person/bartolomeo_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Bartolomeo de Vignolo",
  "gmn:P1_4_has_loconym": "http://example.org/place/vignolo"
}
```

**Output Data (After Transformation):**
```json
{
  "@id": "http://example.org/person/bartolomeo_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/person/bartolomeo_001/appellation/87654321",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": "http://vocab.getty.edu/page/aat/300404650",
      "cidoc:P190_has_symbolic_content": "Bartolomeo de Vignolo"
    },
    {
      "@id": "http://example.org/person/bartolomeo_001/appellation/loconym_23456789",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "https://www.wikidata.org/wiki/Q17143070",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P67_refers_to": {
        "@id": "http://example.org/place/vignolo",
        "@type": "cidoc:E53_Place"
      }
    }
  ]
}
```

### URI Generation Logic

The transformation generates unique URIs for appellations:

```python
place_hash = str(hash(place_uri))[-8:]  # Last 8 digits of hash
appellation_uri = f"{subject_uri}/appellation/loconym_{place_hash}"
```

Example:
- Subject: `http://example.org/person/bartolomeo_001`
- Place: `http://example.org/place/vignolo`
- Hash: `-1234567890` → Last 8: `67890123`
- Result: `http://example.org/person/bartolomeo_001/appellation/loconym_67890123`

---

## Testing Procedures

### Test 1: Basic Transformation

**Objective:** Verify that a simple loconym transforms correctly.

**Test Data (test_basic_loconym.jsonld):**
```json
{
  "@context": {
    "cidoc": "http://www.cidoc-crm.org/cidoc-crm/",
    "gmn": "http://example.org/gmn/"
  },
  "@graph": [
    {
      "@id": "http://example.org/person/test_001",
      "@type": "cidoc:E21_Person",
      "gmn:P1_4_has_loconym": "http://example.org/place/test_genoa"
    }
  ]
}
```

**Steps:**
1. Save test data to a file
2. Run the transformation script:
   ```bash
   python3 gmn_to_cidoc_transform.py test_basic_loconym.jsonld
   ```
3. Check output for:
   - `cidoc:P1_is_identified_by` array created
   - E41_Appellation with correct structure
   - P2_has_type points to Wikidata Q17143070
   - P67_refers_to points to place
   - Original `gmn:P1_4_has_loconym` removed

**Expected Result:**
```json
{
  "@id": "http://example.org/person/test_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/person/test_001/appellation/loconym_12345678",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "https://www.wikidata.org/wiki/Q17143070",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P67_refers_to": {
        "@id": "http://example.org/place/test_genoa",
        "@type": "cidoc:E53_Place"
      }
    }
  ]
}
```

### Test 2: Multiple Loconyms

**Objective:** Verify that multiple loconyms are handled correctly.

**Test Data:**
```json
{
  "@id": "http://example.org/person/test_002",
  "@type": "cidoc:E21_Person",
  "gmn:P1_4_has_loconym": [
    "http://example.org/place/venice",
    "http://example.org/place/genoa"
  ]
}
```

**Validation Checklist:**
- [ ] Two separate E41_Appellation resources created
- [ ] Each has unique URI with different hash
- [ ] Both point to Wikidata Q17143070 type
- [ ] Each refers to correct place
- [ ] No duplicate appellations

### Test 3: Combined with Other Name Properties

**Objective:** Verify that loconym works alongside other name properties.

**Test Data:**
```json
{
  "@id": "http://example.org/person/test_003",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Giovanni da Genova",
  "gmn:P1_2_has_name_from_source": "Iohannes de Ianua",
  "gmn:P1_3_has_patrilineal_name": "Giovanni q. Antonio",
  "gmn:P1_4_has_loconym": "http://example.org/place/genoa"
}
```

**Validation Checklist:**
- [ ] Four E41_Appellation resources created (one per property)
- [ ] Each has correct P2_has_type:
  - P1_1: AAT 300404650 (names)
  - P1_2: AAT 300456607 (names from sources)
  - P1_3: AAT 300404651 (patronymics)
  - P1_4: Wikidata Q17143070 (loconyms)
- [ ] Loconym appellation has P67_refers_to, others have P190_has_symbolic_content
- [ ] All appellations in single P1_is_identified_by array

### Test 4: Empty or Missing Property

**Objective:** Verify graceful handling when property is missing.

**Test Data:**
```json
{
  "@id": "http://example.org/person/test_004",
  "@type": "cidoc:E21_Person",
  "gmn:P1_1_has_name": "Simple Person"
}
```

**Expected Behavior:**
- Transformation completes without errors
- No loconym appellation created
- Other properties transform normally
- No empty P1_is_identified_by array created

### Test 5: Object vs. String URI Format

**Objective:** Verify both input formats work correctly.

**Test Data Set A (Object Format):**
```json
{
  "@id": "http://example.org/person/test_005a",
  "@type": "cidoc:E21_Person",
  "gmn:P1_4_has_loconym": {
    "@id": "http://example.org/place/vignolo"
  }
}
```

**Test Data Set B (String Format):**
```json
{
  "@id": "http://example.org/person/test_005b",
  "@type": "cidoc:E21_Person",
  "gmn:P1_4_has_loconym": "http://example.org/place/vignolo"
}
```

**Validation:**
- [ ] Both produce identical output structure
- [ ] Both correctly extract place URI
- [ ] Both generate valid appellation

---

## Integration with Other Properties

### Combining with Name Properties

Loconym typically works in combination with other name properties:

```turtle
<person_giovanni> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni da Genova" ;           # Display name
    gmn:P1_2_has_name_from_source "Iohannes de Ianua" ;  # Latin source
    gmn:P1_3_has_patrilineal_name "Giovanni q. Antonio" ;  # Patronymic
    gmn:P1_4_has_loconym <place_genoa> .                # Geographic origin
```

**Result:** Four separate E41_Appellation resources, each properly typed.

### Combining with Regional Provenance

You can use both loconym and regional provenance together:

```turtle
<person_merchant> a cidoc:E21_Person ;
    gmn:P1_4_has_loconym <place_genoa> ;              # Place in name
    gmn:P107i_1_has_regional_provenance <group_ligurian> .  # Regional group
```

**Difference:**
- **P1_4**: Place component in the person's **name** → Creates E41_Appellation
- **P107i_1**: Person's membership in a **regional group** → Creates E74_Group

### Integration with Person Properties

Complete person record:

```turtle
<person_complete> a cidoc:E21_Person ;
    # Name properties
    gmn:P1_1_has_name "Bartolomeo de Vignolo" ;
    gmn:P1_4_has_loconym <place_vignolo> ;
    
    # Biographical properties
    gmn:P2_1_gender aat:300189559 ;  # male
    gmn:P97_1_has_father <person_antonio> ;
    gmn:P107i_3_has_occupation <group_notaries> ;
    
    # Administrative properties
    gmn:P3_1_has_editorial_note "Identified in 1445 contract" .
```

---

## Troubleshooting

### Issue 1: Transformation Not Occurring

**Symptoms:**
- `gmn:P1_4_has_loconym` still present after transformation
- No E41_Appellation created

**Possible Causes:**
1. Function not called in `transform_item()`
2. Property name typo in data
3. Data not in expected format

**Solutions:**
1. Verify function is called around line 840 in `transform_item()`
2. Check exact property name: `gmn:P1_4_has_loconym` (not `P1.4`)
3. Verify data uses correct namespace prefix

### Issue 2: Invalid Place URI

**Symptoms:**
- Error during transformation
- Appellation created but P67_refers_to is malformed

**Possible Causes:**
1. Place value is not a URI
2. Place URI is empty or null
3. Place object missing `@id`

**Solutions:**
1. Ensure place value is a valid URI string or object with `@id`
2. Check for empty strings or null values
3. Validate place resource exists

### Issue 3: Duplicate Appellations

**Symptoms:**
- Multiple identical E41_Appellation resources created
- Hash collision in URI generation

**Possible Causes:**
1. Transformation run multiple times on same data
2. Data contains duplicate loconym values

**Solutions:**
1. Ensure transformation runs once per dataset
2. Remove duplicate loconym values from source data
3. Check for already-transformed data before processing

### Issue 4: Wrong Type in Appellation

**Symptoms:**
- P2_has_type not pointing to Wikidata Q17143070
- Type pointing to different AAT term

**Possible Causes:**
1. `WIKIDATA_LOCONYM` constant modified or missing
2. Wrong transformation function called

**Solutions:**
1. Verify constant at top of file:
   ```python
   WIKIDATA_LOCONYM = "https://www.wikidata.org/wiki/Q17143070"
   ```
2. Ensure correct function called for loconym property

### Issue 5: Missing Place Type

**Symptoms:**
- Place resource missing `cidoc:E53_Place` type in output

**Possible Causes:**
- Place not declared as E53_Place in source data
- Transformation not adding type

**Solutions:**
This is expected behavior if place isn't pre-typed. The transformation adds:
```json
{
  "@id": "place_uri",
  "@type": "cidoc:E53_Place"
}
```

If missing, add explicit type declaration to place resource in your data.

---

## Best Practices

### 1. Place Resource Management

**DO:**
✅ Create persistent place resources with stable URIs  
✅ Add labels and descriptions to place resources  
✅ Link places to external gazetteers (GeoNames, Getty TGN)  
✅ Document place hierarchies (neighborhood → city → region)

**DON'T:**
❌ Use inline literals for places  
❌ Create duplicate place resources for same location  
❌ Use temporary or random URIs for important places  
❌ Mix loconym places with other place uses

**Example:**
```turtle
<place_genoa> a cidoc:E53_Place ;
    rdfs:label "Genoa"@en ;
    rdfs:label "Genova"@it ;
    rdfs:label "Ianua"@la ;
    owl:sameAs <http://www.geonames.org/3176219> ;
    owl:sameAs <http://vocab.getty.edu/tgn/7006082> ;
    cidoc:P89_falls_within <place_liguria> .
```

### 2. Naming Consistency

**DO:**
✅ Use consistent place naming across your dataset  
✅ Include multiple language forms of place names  
✅ Link variant spellings with `owl:sameAs`  
✅ Document historical vs. modern place names

**Example:**
```turtle
# Historical person with historical place name
<person_giovanni_1445> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Iohannes de Ianua" ;
    gmn:P1_4_has_loconym <place_ianua> .

<place_ianua> a cidoc:E53_Place ;
    rdfs:label "Ianua"@la ;          # Latin name (historical)
    rdfs:label "Genova"@it ;         # Italian name (historical)
    rdfs:label "Genoa"@en ;          # English name (modern)
    owl:sameAs <place_genoa> .       # Link to modern resource
```

### 3. Documentation Standards

**DO:**
✅ Add `gmn:P3_1_has_editorial_note` for uncertain identifications  
✅ Document source of place identification  
✅ Note ambiguous or unclear loconyms  
✅ Record variant interpretations

**Example:**
```turtle
<person_bartolomeo> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Bartholomeus de Vignolo" ;
    gmn:P1_4_has_loconym <place_vignolo> ;
    gmn:P3_1_has_editorial_note """Vignolo likely refers to Vignole Borbera 
        in Piedmont, though other places named Vignolo exist. Identification 
        based on regional context of contract."""@en .
```

### 4. Querying Patterns

Common SPARQL queries for loconyms:

**Find all people from a specific place:**
```sparql
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gmn: <http://example.org/gmn/>

SELECT ?person ?name WHERE {
  ?person gmn:P1_4_has_loconym <http://example.org/place/genoa> ;
          gmn:P1_1_has_name ?name .
}
```

**Find all places referenced in loconyms:**
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT DISTINCT ?place WHERE {
  ?person gmn:P1_4_has_loconym ?place .
}
```

**Find people with both loconym and regional provenance:**
```sparql
PREFIX gmn: <http://example.org/gmn/>

SELECT ?person ?loconym_place ?region_group WHERE {
  ?person gmn:P1_4_has_loconym ?loconym_place ;
          gmn:P107i_1_has_regional_provenance ?region_group .
}
```

### 5. Data Quality Checks

Regular validation queries:

**Check for loconyms without place type:**
```sparql
SELECT ?person ?place WHERE {
  ?person gmn:P1_4_has_loconym ?place .
  FILTER NOT EXISTS { ?place a cidoc:E53_Place }
}
```

**Check for orphaned loconym appellations:**
```sparql
SELECT ?appellation WHERE {
  ?appellation a cidoc:E41_Appellation ;
               cidoc:P2_has_type <https://www.wikidata.org/wiki/Q17143070> .
  FILTER NOT EXISTS {
    ?person cidoc:P1_is_identified_by ?appellation .
  }
}
```

---

## Summary Checklist

### Implementation Verification
- [ ] Property defined in `gmn_ontology.ttl`
- [ ] Transformation function exists in `gmn_to_cidoc_transform.py`
- [ ] Function called in `transform_item()`
- [ ] `WIKIDATA_LOCONYM` constant defined correctly

### Testing Completion
- [ ] Basic transformation test passed
- [ ] Multiple loconyms test passed
- [ ] Combined properties test passed
- [ ] Empty/missing property test passed
- [ ] Format variations test passed

### Documentation
- [ ] Usage examples added to project documentation
- [ ] Place resources documented
- [ ] Naming conventions established
- [ ] Query patterns documented

### Data Quality
- [ ] Place URIs are persistent and meaningful
- [ ] All places properly typed as E53_Place
- [ ] Ambiguous identifications documented
- [ ] No duplicate loconym resources

---

**End of Implementation Guide**
