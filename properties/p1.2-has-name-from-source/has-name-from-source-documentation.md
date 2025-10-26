# has_name_from_source Property Documentation

**Property URI**: `gmn:P1_2_has_name_from_source`  
**Version**: 1.0  
**Status**: Active  
**Date**: October 26, 2025

## Executive Summary

The `gmn:P1_2_has_name_from_source` property provides a simplified way to record personal names exactly as they appear in historical source documents. This property serves as a shortcut that automatically transforms to the full CIDOC-CRM compliant structure during data processing, maintaining historical fidelity while ensuring semantic interoperability.

## Table of Contents

1. [Property Overview](#property-overview)
2. [Semantic Definition](#semantic-definition)
3. [CIDOC-CRM Alignment](#cidoc-crm-alignment)
4. [AAT Integration](#aat-integration)
5. [Use Cases](#use-cases)
6. [Data Entry Guidelines](#data-entry-guidelines)
7. [Transformation Process](#transformation-process)
8. [Relationship to Other Properties](#relationship-to-other-properties)
9. [Examples](#examples)
10. [Best Practices](#best-practices)
11. [Frequently Asked Questions](#frequently-asked-questions)

## Property Overview

### Basic Information

| Attribute | Value |
|-----------|-------|
| **URI** | `gmn:P1_2_has_name_from_source` |
| **Label** | "P1.2 has name from source" |
| **Type** | `owl:DatatypeProperty` |
| **Domain** | `cidoc:E21_Person` |
| **Range** | `cidoc:E62_String` |
| **Subproperty of** | `cidoc:P1_is_identified_by` |
| **Implicit Type** | `aat:300456607` (names found in historical sources) |
| **Created** | 2025-10-26 |

### Purpose

`P1_2_has_name_from_source` addresses a common challenge in historical data management: recording personal names as they actually appear in source documents while maintaining compatibility with formal ontological standards. Historical documents often present names in various forms, spellings, and formats that differ from modern standardized versions. This property enables researchers to:

- Preserve historical name variants exactly as documented
- Track orthographic variations across multiple sources
- Maintain source fidelity without compromising data quality
- Simplify data entry while ensuring CIDOC-CRM compliance
- Distinguish source-documented names from normalized forms

## Semantic Definition

### Formal Definition

`gmn:P1_2_has_name_from_source` is a simplified datatype property that expresses the name of a person as found in historical sources. It represents the following full CIDOC-CRM path:

```
E21_Person 
  → P1_is_identified_by → E41_Appellation
    → P2_has_type → E55_Type (aat:300456607)
    → P190_has_symbolic_content → E62_String
```

This property is provided as a convenience for data entry and is automatically transformed to the complete CIDOC-CRM structure during processing.

### Conceptual Model

**Input (Simplified)**:
```
Person ─── has_name_from_source ──→ "Name String"
```

**Output (CIDOC-CRM)**:
```
Person ─── P1_is_identified_by ──→ Appellation
                                      │
                                      ├── type: "names from sources"
                                      └── content: "Name String"
```

### Key Characteristics

1. **Source Authenticity**: Records names exactly as they appear in historical documents
2. **Automatic Typing**: Automatically applies AAT term 300456607 during transformation
3. **Multi-valued**: A person can have multiple names from different sources
4. **Historical Context**: Preserves temporal and documentary variations in naming
5. **Semantic Precision**: Explicitly marks these as source-documented names

## CIDOC-CRM Alignment

### CIDOC-CRM Classes Used

**E21_Person**
- Domain of the property
- Represents human beings, both living and deceased
- Identified by various forms of appellations

**E41_Appellation**
- Created during transformation
- Represents names, titles, and other identifiers
- Can be typed to distinguish different categories of names

**E55_Type**
- References the AAT term for classification
- Provides semantic context for the appellation
- Enables reasoning about different types of names

**E62_String**
- Range of the property (input)
- Also used for P190_has_symbolic_content (output)
- Contains the actual text of the name

### CIDOC-CRM Properties Used

**P1_is_identified_by**
- Links person to appellation
- Core identification property in CIDOC-CRM
- Domain: E1_CRM_Entity; Range: E41_Appellation
- Superclass of our simplified property

**P2_has_type**
- Classifies the appellation
- Links to AAT term for "names found in historical sources"
- Domain: E1_CRM_Entity; Range: E55_Type

**P190_has_symbolic_content**
- Contains the actual name string
- Provides the textual content of the appellation
- Domain: E90_Symbolic_Object; Range: E62_String

### Transformation Diagram

```
INPUT:
┌─────────────────────────────┐
│ E21_Person                  │
│ @id: person/spinola_123     │
│                             │
│ P1_2_has_name_from_source:  │
│   "Antonius Spinula"        │
└─────────────────────────────┘

TRANSFORMATION:
        ↓
        ↓
        ↓

OUTPUT:
┌─────────────────────────────────────────────────┐
│ E21_Person                                      │
│ @id: person/spinola_123                         │
│                                                 │
│ P1_is_identified_by ──→ E41_Appellation        │
│                          @id: appellation/xyz   │
│                          │                      │
│                          ├─ P2_has_type ──→     │
│                          │    E55_Type          │
│                          │    @id: aat:300456607│
│                          │                      │
│                          └─ P190_has_symbolic_  │
│                               content:          │
│                               "Antonius Spinula"│
└─────────────────────────────────────────────────┘
```

## AAT Integration

### AAT Term Details

**AAT ID**: 300456607  
**Getty URI**: http://vocab.getty.edu/page/aat/300456607  
**Preferred Label**: "names found in historical sources"  
**Term Type**: Guide term

**Scope Note**: 
> Names for people, places, and entities documented in historical records, manuscripts, and archival materials, particularly when those names differ from modern standardized forms or currently accepted designations. Used to distinguish historical attestations from contemporary or normalized name forms.

**Hierarchical Position**:
```
Objects Facet (300264092)
  → Object Genres (300431405)
    → information forms (300378935)
      → names (300404658)
        → names found in historical sources (300456607)
```

### Why AAT 300456607?

This specific AAT term is ideal for `P1_2_has_name_from_source` because:

1. **Explicit Source Documentation**: Clearly indicates the name comes from a historical source
2. **Historical Context**: Acknowledges temporal variation in naming practices
3. **Distinction from Normalized Forms**: Differentiates from modern standardized names
4. **Scholarly Recognition**: Aligns with academic practices in historical research
5. **Getty Authority**: Provides internationally recognized semantic classification

### Comparison with Related AAT Terms

| AAT Term | Purpose | Use with GMN Property |
|----------|---------|----------------------|
| 300404650 (names) | General, normalized names | `P1_1_has_name` |
| 300456607 (names from sources) | Names as documented in sources | `P1_2_has_name_from_source` |
| 300404651 (patronymics) | Names with ancestry | `P1_3_has_patrilineal_name` |

## Use Cases

### Use Case 1: Recording Name Variants Across Documents

**Context**: A researcher is working with multiple notarial contracts from different decades that mention the same person, but spell their name differently in each document.

**Data Entry**:
```turtle
<person/grimaldi_oberto>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Oberto Grimaldi" ;  # Normalized modern form
    gmn:P1_2_has_name_from_source "Obertus de Grimaldis" ;  # From 1345 contract
    gmn:P1_2_has_name_from_source "Oberti Grimaldi" ;  # From 1352 will
    gmn:P1_2_has_name_from_source "Obertus Grimaldus" .  # From 1347 letter
```

**Benefit**: Preserves all historical variants while maintaining a standardized reference form.

### Use Case 2: Tracking Orthographic Evolution

**Context**: Documenting how a family name's spelling changes over time in various documents.

**Data Entry**:
```turtle
<person/doria_branca>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Branca Doria" ;
    gmn:P1_2_has_name_from_source "Branca de Auria" ;  # 1330s spelling
    gmn:P1_2_has_name_from_source "Blancha Doria" ;  # 1340s spelling
    gmn:P1_2_has_name_from_source "Branca Aurie" ;  # 1350s spelling
    gmn:P1_2_has_name_from_source "Branca D'Oria" .  # 1360s spelling
```

**Benefit**: Enables analysis of naming patterns and orthographic conventions over time.

### Use Case 3: Distinguishing Latin and Vernacular Forms

**Context**: Historical documents use both Latin and Italian vernacular versions of names.

**Data Entry**:
```turtle
<person/spinola_giacomo>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giacomo Spinola" ;  # Modern Italian
    gmn:P1_2_has_name_from_source "Iacobus Spinula" ;  # Latin notarial form
    gmn:P1_2_has_name_from_source "Giacomo de Spinola" ;  # Vernacular form
    gmn:P1_2_has_name_from_source "Jacobus de Spinulis" .  # Alternative Latin
```

**Benefit**: Maintains linguistic context while providing normalized reference.

### Use Case 4: Recording Abbreviated Forms

**Context**: Documents often use abbreviated forms of names for common individuals.

**Data Entry**:
```turtle
<person/negro_giovanni>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giovanni de Nigro" ;
    gmn:P1_2_has_name_from_source "Iohannes de Nigro" ;  # Full Latin form
    gmn:P1_2_has_name_from_source "Ioh. de Nigro" ;  # Abbreviated form
    gmn:P1_2_has_name_from_source "Io. Nigro" .  # Highly abbreviated
```

**Benefit**: Documents scribal practices and abbreviation conventions.

### Use Case 5: Uncertain or Variant Readings

**Context**: Transcribing damaged or ambiguous manuscripts where name readings vary.

**Data Entry**:
```turtle
<person/malocello_uncertain>
    a cidoc:E21_Person ;
    gmn:P1_1_has_name "Lancelotto Malocello" ;  # Accepted reading
    gmn:P1_2_has_name_from_source "Lancelotus Malocellus" ;  # Clear reading
    gmn:P1_2_has_name_from_source "Lancelotus Mallocellus" ;  # Variant reading
    gmn:P1_2_has_name_from_source "Lancelotus Mal[...]ellus" .  # Damaged text
```

**Benefit**: Preserves scholarly uncertainty and alternative interpretations.

## Data Entry Guidelines

### When to Use P1_2_has_name_from_source

**Use this property when:**

✓ Recording names exactly as they appear in historical documents  
✓ Preserving spelling variations across multiple sources  
✓ Documenting Latin vs. vernacular name forms  
✓ Tracking orthographic evolution over time  
✓ Recording abbreviated or stylized name forms  
✓ Capturing uncertain or variant manuscript readings  

**Do NOT use this property when:**

✗ Entering modern normalized name forms (use `P1_1_has_name`)  
✗ Recording patronymic ancestry chains (use `P1_3_has_patrilineal_name`)  
✗ Adding place-based identifiers (use `P1_4_has_loconym`)  
✗ Creating modern standardized references  

### Input Format

**Standard Format**:
```turtle
gmn:P1_2_has_name_from_source "Name as in source" .
```

**Multiple Names**:
```turtle
gmn:P1_2_has_name_from_source "First variant" .
gmn:P1_2_has_name_from_source "Second variant" .
```

**In JSON-LD**:
```json
{
  "gmn:P1_2_has_name_from_source": [
    {"@value": "Name variant 1"},
    {"@value": "Name variant 2"}
  ]
}
```

### Character Handling

**Standard Characters**: Enter as-is
```turtle
gmn:P1_2_has_name_from_source "Antonius Spinula" .
```

**Special Characters**: Preserve exactly
```turtle
gmn:P1_2_has_name_from_source "Iohannes q. Petri de Nigro" .
```

**Unicode Characters**: Supported
```turtle
gmn:P1_2_has_name_from_source "João de Évora" .
```

**Abbreviations**: Use period notation
```turtle
gmn:P1_2_has_name_from_source "Ant. Doria" .
gmn:P1_2_has_name_from_source "Io. de Grimaldis" .
```

**Damaged Text**: Use brackets for editorial additions
```turtle
gmn:P1_2_has_name_from_source "Iaco[bus] Spinula" .
gmn:P1_2_has_name_from_source "Anton[ius?] Dori[a]" .
```

### Documentation Best Practices

1. **Source Citation**: Link names to specific documents
2. **Date Range**: Note when each variant appears
3. **Paleographic Notes**: Document unusual spellings or abbreviations
4. **Editorial Decisions**: Explain ambiguous readings
5. **Consistency**: Follow project transcription guidelines

## Transformation Process

### Step-by-Step Transformation

**Step 1: Input Recognition**

The transformation script identifies items with `gmn:P1_2_has_name_from_source`:

```python
if 'gmn:P1_2_has_name_from_source' in data:
    # Proceed with transformation
```

**Step 2: Appellation URI Generation**

For each name value, generate a unique URI:

```python
appellation_uri = generate_appellation_uri(
    subject_uri,
    name_value,
    'gmn:P1_2_has_name_from_source'
)
```

**Step 3: E41_Appellation Creation**

Create the appellation structure:

```python
appellation = {
    '@id': appellation_uri,
    '@type': 'cidoc:E41_Appellation',
    'cidoc:P2_has_type': {
        '@id': 'http://vocab.getty.edu/page/aat/300456607',
        '@type': 'cidoc:E55_Type'
    },
    'cidoc:P190_has_symbolic_content': name_value
}
```

**Step 4: Link to Person**

Add appellation to person's identification:

```python
if 'cidoc:P1_is_identified_by' not in data:
    data['cidoc:P1_is_identified_by'] = []
data['cidoc:P1_is_identified_by'].append(appellation)
```

**Step 5: Remove Shortcut Property**

Clean up by removing the simplified property:

```python
del data['gmn:P1_2_has_name_from_source']
```

### Transformation Example

**Input**:
```json
{
  "@id": "http://example.org/person/spinola_001",
  "@type": "cidoc:E21_Person",
  "gmn:P1_2_has_name_from_source": [
    {"@value": "Antonius Spinula"},
    {"@value": "Antonio de Spinola"}
  ]
}
```

**Output**:
```json
{
  "@id": "http://example.org/person/spinola_001",
  "@type": "cidoc:E21_Person",
  "cidoc:P1_is_identified_by": [
    {
      "@id": "http://example.org/appellation/001",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300456607",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Antonius Spinula"
    },
    {
      "@id": "http://example.org/appellation/002",
      "@type": "cidoc:E41_Appellation",
      "cidoc:P2_has_type": {
        "@id": "http://vocab.getty.edu/page/aat/300456607",
        "@type": "cidoc:E55_Type"
      },
      "cidoc:P190_has_symbolic_content": "Antonio de Spinola"
    }
  ]
}
```

## Relationship to Other Properties

### Name Property Family

The GMN ontology includes several properties for recording personal names, each serving a distinct purpose:

| Property | AAT Type | Purpose | Example |
|----------|----------|---------|---------|
| `P1_1_has_name` | 300404650 | Normalized modern form | "Giovanni Spinola" |
| `P1_2_has_name_from_source` | 300456607 | Historical source form | "Iohannes Spinula" |
| `P1_3_has_patrilineal_name` | 300404651 | Name with ancestry | "Iohannes Spinula q. Antonii" |
| `P1_4_has_loconym` | 300404651 | Place-based identifier | "Giovanni da Genova" |

### Semantic Distinctions

**P1_1_has_name vs P1_2_has_name_from_source**:
- `P1_1`: Modern, normalized, standardized form
- `P1_2`: Historical, as-documented, source-faithful form

**Example**:
```turtle
<person/doria>
    gmn:P1_1_has_name "Andrea Doria" ;  # Modern standard
    gmn:P1_2_has_name_from_source "Andreas de Auria" .  # 14th century Latin
```

**P1_2_has_name_from_source vs P1_3_has_patrilineal_name**:
- `P1_2`: Any name form from sources
- `P1_3`: Specifically names including ancestry

**Example**:
```turtle
<person/spinola>
    gmn:P1_2_has_name_from_source "Iohannes Spinula" ;  # Simple name
    gmn:P1_3_has_patrilineal_name "Iohannes Spinula q. Antonii" .  # With ancestry
```

### Combined Usage

These properties are designed to work together:

```turtle
<person/grimaldi_luca>
    a cidoc:E21_Person ;
    
    # Normalized modern reference
    gmn:P1_1_has_name "Luca Grimaldi" ;
    
    # Historical source variants
    gmn:P1_2_has_name_from_source "Lucas Grimaldus" ;
    gmn:P1_2_has_name_from_source "Luca de Grimaldis" ;
    gmn:P1_2_has_name_from_source "Luchas Grimaldi" ;
    
    # Patrilineal form with ancestry
    gmn:P1_3_has_patrilineal_name "Luca Grimaldi q. Nicolai q. Lucae" ;
    
    # Place-based identifier
    gmn:P1_4_has_loconym "Luca da Genova" .
```

### CIDOC-CRM Output Differences

After transformation, each property type creates E41_Appellation with different P2_has_type values:

```turtle
# From P1_1_has_name
<app1> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Luca Grimaldi" .

# From P1_2_has_name_from_source  
<app2> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Lucas Grimaldus" .

# From P1_3_has_patrilineal_name
<app3> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404651> ;
    cidoc:P190_has_symbolic_content "Luca Grimaldi q. Nicolai" .
```

## Examples

### Example 1: Basic Usage

**Scenario**: Recording a person's name as it appears in a 1345 notarial contract.

**Input**:
```turtle
@prefix cidoc: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix gmn: <http://example.org/gmn/ontology/> .

<person/spinola_antonio_001> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Antonius Spinula" .
```

**Transformed Output**:
```turtle
<person/spinola_antonio_001> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <appellation/spinola_001> .

<appellation/spinola_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Antonius Spinula" .
```

### Example 2: Multiple Source Variants

**Scenario**: A merchant appears in multiple documents with different name spellings.

**Input**:
```turtle
<person/doria_giacomo_002> a cidoc:E21_Person ;
    gmn:P1_1_has_name "Giacomo Doria" ;
    gmn:P1_2_has_name_from_source "Iacobus de Auria" ;
    gmn:P1_2_has_name_from_source "Giacomo d'Oria" ;
    gmn:P1_2_has_name_from_source "Jacobus Aurie" .
```

**Transformed Output**:
```turtle
<person/doria_giacomo_002> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <appellation/doria_001> ;
    cidoc:P1_is_identified_by <appellation/doria_002> ;
    cidoc:P1_is_identified_by <appellation/doria_003> ;
    cidoc:P1_is_identified_by <appellation/doria_004> .

<appellation/doria_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Giacomo Doria" .

<appellation/doria_002> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Iacobus de Auria" .

<appellation/doria_003> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Giacomo d'Oria" .

<appellation/doria_004> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Jacobus Aurie" .
```

### Example 3: Names with Special Characters

**Scenario**: Recording names with abbreviations and patronymic indicators.

**Input**:
```turtle
<person/grimaldi_oberto_003> a cidoc:E21_Person ;
    gmn:P1_2_has_name_from_source "Obertus q. Nicolai de Grimaldis" ;
    gmn:P1_2_has_name_from_source "Obert. Grimaldi" .
```

**Transformed Output**:
```turtle
<person/grimaldi_oberto_003> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <appellation/grimaldi_001> ;
    cidoc:P1_is_identified_by <appellation/grimaldi_002> .

<appellation/grimaldi_001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Obertus q. Nicolai de Grimaldis" .

<appellation/grimaldi_002> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Obert. Grimaldi" .
```

### Example 4: Complete Person Record

**Scenario**: Full person record with multiple name types.

**Input**:
```turtle
<person/spinola_luca_004> a cidoc:E21_Person ;
    # Normalized name
    gmn:P1_1_has_name "Luca Spinola" ;
    
    # Historical variants from sources
    gmn:P1_2_has_name_from_source "Lucas Spinula" ;
    gmn:P1_2_has_name_from_source "Luca de Spinola" ;
    gmn:P1_2_has_name_from_source "Luchas Spinole" ;
    
    # Patrilineal name
    gmn:P1_3_has_patrilineal_name "Luca Spinola q. Opicini q. Lucae" ;
    
    # Loconym
    gmn:P1_4_has_loconym "Luca da Genova" .
```

**Transformed Output**: (Abbreviated for clarity)
```turtle
<person/spinola_luca_004> a cidoc:E21_Person ;
    cidoc:P1_is_identified_by <app/001>, <app/002>, <app/003>, 
                              <app/004>, <app/005>, <app/006> .

# Modern name (AAT 300404650)
<app/001> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404650> ;
    cidoc:P190_has_symbolic_content "Luca Spinola" .

# Source variants (AAT 300456607)
<app/002> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Lucas Spinula" .

<app/003> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Luca de Spinola" .

<app/004> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300456607> ;
    cidoc:P190_has_symbolic_content "Luchas Spinole" .

# Patrilineal name (AAT 300404651)
<app/005> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404651> ;
    cidoc:P190_has_symbolic_content "Luca Spinola q. Opicini q. Lucae" .

# Loconym (special handling)
<app/006> a cidoc:E41_Appellation ;
    cidoc:P2_has_type <http://vocab.getty.edu/page/aat/300404651> ;
    cidoc:P190_has_symbolic_content "Luca da Genova" ;
    cidoc:P67_refers_to <place/genoa> .
```

## Best Practices

### Data Entry

1. **Transcribe Exactly**: Record names precisely as they appear in sources
2. **Include Diacritics**: Preserve all special characters and marks
3. **Note Abbreviations**: Use standard notation (periods) for abbreviations
4. **Document Uncertainty**: Use brackets for editorial additions or uncertainties
5. **Cite Sources**: Link each name variant to its source document
6. **Avoid Modernization**: Do not standardize spelling in P1_2 entries

### Data Management

1. **Consistent Transcription**: Follow project-wide transcription guidelines
2. **Regular Validation**: Check for data quality and consistency
3. **Source Linking**: Associate names with specific documents and dates
4. **Version Control**: Track changes to name data over time
5. **Quality Assurance**: Review entries for accuracy and completeness

### Analysis Considerations

1. **Variant Analysis**: Use source names to study orthographic patterns
2. **Temporal Tracking**: Analyze how names change across time periods
3. **Scribal Practices**: Study abbreviation and spelling conventions
4. **Identity Resolution**: Use multiple variants to confirm person identity
5. **Network Analysis**: Track name usage in different social contexts

## Frequently Asked Questions

### Q1: When should I use P1_2 vs P1_1?

**A:** Use `P1_1_has_name` for the modern, normalized form you want to use as a standard reference. Use `P1_2_has_name_from_source` for recording the exact forms that appear in historical documents. Use both together for best results.

### Q2: Can I use this property for place names?

**A:** No, `P1_2_has_name_from_source` is specifically for personal names (domain: E21_Person). For place names from sources, use appropriate place identification properties.

### Q3: How do I handle uncertain readings?

**A:** Use standard editorial notation with brackets:
- `"Iaco[bus]"` - damaged text with certain reconstruction
- `"Iaco[bus?]"` - uncertain reconstruction
- `"Iaco[...]"` - illegible portion

### Q4: Should I include titles or honorifics?

**A:** Only if they appear as part of the name in the source. Separate titles should be recorded using appropriate title/role properties, not as part of the name string.

### Q5: What about names in different languages?

**A:** Record each language variant separately. The property supports all Unicode characters, so Latin, Italian, and other language forms can be included.

### Q6: How many name variants should I record?

**A:** Record all significant variants that appear in sources. There's no limit, but focus on variants that represent meaningful orthographic, linguistic, or temporal differences.

### Q7: Can this property be used with organizations?

**A:** No, the domain is restricted to E21_Person. Organizations would use different identification properties appropriate to their class.

### Q8: How is this different from alternative labels?

**A:** `P1_2_has_name_from_source` specifically indicates the name is documented in a historical source and triggers transformation to CIDOC-CRM structure with specific AAT typing. Alternative labels are more generic.

### Q9: What if two different sources use the same spelling?

**A:** You can record the same spelling multiple times if it appears in multiple sources, or record it once and document both sources in associated metadata.

### Q10: How do I link names to specific documents?

**A:** While `P1_2_has_name_from_source` records the name itself, you should create separate relationships linking the person to documents that mention them, allowing you to track which names appear in which sources.

## Technical Notes

### URI Generation

Appellation URIs are generated using a consistent algorithm that:
- Ensures uniqueness for each name/person combination
- Produces stable, reproducible URIs
- Encodes special characters properly
- Maintains RDF validity

### Character Encoding

All string values support UTF-8 encoding, allowing:
- Unicode characters (è, ö, ñ, etc.)
- Special symbols (†, §, ‡, etc.)
- Diacritical marks
- Non-Latin scripts (if needed)

### Performance Considerations

The transformation process is optimized for:
- Batch processing of multiple items
- Efficient URI generation
- Minimal memory footprint
- Fast lookup of existing appellations

### Validation

Automated validation checks:
- Property domain/range compliance
- URI format correctness
- AAT term validity
- CIDOC-CRM structure compliance

## References

### Standards

- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **RDF/OWL**: https://www.w3.org/standards/semanticweb/
- **Getty AAT**: http://www.getty.edu/research/tools/vocabularies/aat/

### Related Documentation

- GMN Ontology: `gmn_ontology.ttl`
- Transformation Script: `gmn_to_cidoc_transform.py`
- Implementation Guide: `has-name-from-source-implementation-guide.md`

### Academic References

- Medieval naming practices and orthographic variation
- Historical prosopography and name identification
- Digital humanities and semantic data modeling
- CIDOC-CRM application in historical research

---

**Document Version**: 1.0  
**Last Updated**: October 26, 2025  
**Maintained By**: Genoese Merchant Networks Project
