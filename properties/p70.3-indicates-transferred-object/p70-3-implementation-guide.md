# P70.3 Indicates Transferred Object - Omeka-S Implementation Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Conceptual Overview](#conceptual-overview)
4. [Resource Structure](#resource-structure)
5. [Step-by-Step Implementation](#step-by-step-implementation)
6. [Resource Templates](#resource-templates)
7. [Controlled Vocabularies](#controlled-vocabularies)
8. [Data Entry Workflow](#data-entry-workflow)
9. [Validation and Testing](#validation-and-testing)
10. [Troubleshooting](#troubleshooting)

## Introduction

This guide provides detailed instructions for implementing the `gmn:P70_3_indicates_transferred_object` property in Omeka-S. This property enables rich modeling of transferred objects in historical contracts using separate resource items for each object.

### Why Separate Resource Items?

Unlike simpler properties that embed data directly in the contract, this approach creates each object as its own resource item with full semantic structure. This enables:

- **Reusability**: Same object can appear in multiple contracts
- **Rich Attribution**: Each object has detailed properties (type, quantity, value, etc.)
- **Semantic Compliance**: Full CIDOC-CRM E13 Attribute Assignment pattern
- **Flexible Querying**: Objects can be searched and analyzed independently

## Prerequisites

### Required Omeka-S Components

- **Omeka-S Version**: 4.0 or higher
- **Modules**:
  - Custom Vocab (for controlled vocabularies)
  - Numeric Data Types (for measurements)
  - Value Suggest (for Getty AAT integration)
- **Vocabularies**:
  - CIDOC-CRM
  - GMN Ontology (with P70.3 additions)
  - Getty AAT (optional but recommended)

### Required Knowledge

- Basic Omeka-S administration
- Understanding of resource templates
- Familiarity with linked data concepts
- Basic understanding of CIDOC-CRM

## Conceptual Overview

### The E13 Attribute Assignment Pattern

When a contract documents a transfer, we need to record not just WHAT was transferred, but also the object's PROPERTIES as they were understood at the time of transfer:

```
Contract Document (E31)
  |
  ├─ refers to (P67)
  |    |
  |    └─ Transfer Activity (E8_Acquisition or E10_Transfer_of_Custody)
  |         |
  |         └─ was assigned by (P140i)
  |              |
  |              └─ Attribute Assignment (E13)
  |                   |
  |                   ├─ assigned property type (P177) → P24 or P30
  |                   ├─ assigned (P141) → Object Resource
  |                   └─ has type (P2) → Object Category
  |
  └─ [shortcut] P70.3 indicates transferred object → Object Resource
```

### Two-Layer Structure

1. **Shortcut Layer** (Omeka-S): Simple `gmn:P70_3_indicates_transferred_object` link from contract to object
2. **Semantic Layer** (Export): Full E13 pattern with E7/E8/E10 activity and attribute assignment

### Object Properties Architecture

Each object resource has properties organized by category:

```
Object Resource (E24_Physical_Human-Made_Thing)
├─ Identification
│   ├─ Name (P1_1)
│   └─ Type/Commodity (P2_1)
├─ Quantity
│   ├─ Count/Number (P54_1)
│   └─ Unit (embedded in dimension)
├─ Monetary Value
│   ├─ Value Amount (custom property)
│   ├─ Currency (custom property)
│   └─ Provenance (custom property)
├─ Physical Characteristics
│   ├─ Dimension/Measurement (P43_1)
│   │   ├─ Type (weight, volume, length)
│   │   ├─ Value (numeric)
│   │   └─ Unit (rubbi, minae, palmi)
│   └─ Color (P56_1)
└─ Provenance
    └─ Origin Place (P27_1)
```

## Resource Structure

### Required Resource Types

You'll need to create resources for:

1. **Contract Documents** (E31.2, E31.6, E31.7, E31.8)
   - The legal document that records the transaction
   
2. **Object Resources** (E24_Physical_Human-Made_Thing)
   - The things being transferred
   
3. **Dimension Resources** (E54_Dimension)
   - Measurements (weight, volume, length)
   
4. **Place Resources** (E53_Place)
   - Provenance/origin locations

### Resource Relationships

```
[Contract] --P70.3--> [Object]
[Object] --P43_1--> [Dimension]
[Object] --P27_1--> [Place]
```

## Step-by-Step Implementation

### Step 1: Import the GMN Ontology with P70.3

1. Navigate to **Vocabularies** in Omeka-S admin
2. Import the updated GMN ontology that includes:
   - `gmn:P70_3_indicates_transferred_object`
   - Supporting object properties
3. Verify import was successful

### Step 2: Set Up Controlled Vocabularies

#### Object Type/Commodity Vocabulary

Create a custom vocabulary for commodity types:

1. Go to **Modules** → **Custom Vocab**
2. Create new vocabulary: "Object Types"
3. Add terms (examples):
   ```
   Salt (sale)
   Wool (lana)
   Boards (axeres)
   Cloth (pannos)
   Wine (vinum)
   Wheat (granum/frumentum)
   Pepper (piper)
   Wax (cera)
   Oil (oleum)
   Leather (corium)
   ```
4. Map to Getty AAT URIs where possible

#### Color Vocabulary

Create a custom vocabulary for colors:

1. Create new vocabulary: "Colors"
2. Add terms:
   ```
   White (albus)
   Black (niger)
   Red (ruber)
   Blue (caeruleus)
   Green (viridis)
   Yellow (flavus)
   Brown (brunneus)
   Gray (griseus)
   ```

#### Measurement Unit Vocabulary

Create vocabulary for medieval units:

1. Create new vocabulary: "Medieval Units"
2. Add terms:
   ```
   Weight Units:
   - Rubbio/Rubbi (Genoese weight)
   - Mina/Minae
   - Cantaro/Cantari
   - Libra/Libre
   
   Volume Units:
   - Congio/Congii
   - Modio/Modii
   - Barile/Barili
   
   Length Units:
   - Palmo/Palmi
   - Canna/Canne
   - Braccio/Braccia
   ```

### Step 3: Create Resource Template for Objects

Create a comprehensive template for transferred objects:

**Template Name:** "Transferred Object"

**Resource Class:** `gmn:E24_Physical_Human-Made_Thing` or `cidoc:E18_Physical_Thing`

**Properties to Include:**

| Property | Type | Required | Controlled? | Notes |
|----------|------|----------|-------------|-------|
| `gmn:P1_1_has_name` | Text | No | No | Descriptive name |
| `gmn:P2_1_has_type` | Resource/URI | Yes | Yes | Object type/commodity |
| `gmn:P54_1_has_count` | Numeric | No | No | Quantity/number |
| `gmn:P43_1_has_dimension` | Resource | No | No | Links to dimension resource |
| `gmn:P56_1_has_color` | Text/URI | No | Yes | From color vocabulary |
| `gmn:P27_1_has_origin` | Resource | No | No | Links to place resource |
| Value Amount | Numeric | No | No | Monetary value (L.S.D) |
| Value Currency | Resource/URI | No | No | Currency type |
| Value Provenance | Text | No | No | Source of value info |

### Step 4: Create Resource Template for Dimensions

**Template Name:** "Object Dimension"

**Resource Class:** `cidoc:E54_Dimension`

**Properties:**

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `cidoc:P2_has_type` | Resource/URI | Yes | Dimension type (weight, volume, length) |
| `cidoc:P90_has_value` | Numeric | Yes | Measurement value |
| `cidoc:P91_has_unit` | Resource/URI | Yes | Unit from medieval units vocab |

### Step 5: Configure Contract Template

Update your contract templates to include:

**For Sales Contracts (E31.2):**

Add property: `gmn:P70_3_indicates_transferred_object`
- Type: Resource
- Allow multiple: Yes
- Required: No

**For Lease Contracts (E31.6):**

Add property: `gmn:P70_3_indicates_transferred_object`
- Type: Resource
- Allow multiple: Yes
- Required: No

**For Donation Contracts (E31.7):**

Add property: `gmn:P70_3_indicates_transferred_object`
- Type: Resource
- Allow multiple: Yes
- Required: No

**For Dowry Contracts (E31.8):**

Add property: `gmn:P70_3_indicates_transferred_object`
- Type: Resource
- Allow multiple: Yes
- Required: No

### Step 6: Set Up Value Extraction (Optional)

For Getty AAT integration:

1. Install **Value Suggest** module
2. Configure for AAT materials and commodities
3. Map to `gmn:P2_1_has_type` property

## Data Entry Workflow

### Creating an Object Resource

**Step-by-Step Process:**

1. **Navigate to Items** → **Add new item**

2. **Select Resource Template**: "Transferred Object"

3. **Set Resource Class**: `gmn:E24_Physical_Human-Made_Thing`

4. **Enter Basic Information:**
   - **Title**: Descriptive identifier (e.g., "100 rubbi of white salt from Ibiza")
   - **Name** (`P1_1`): "White salt from Ibiza"
   
5. **Set Object Type** (`P2_1`):
   - Click "Add value"
   - Select from vocabulary or link to AAT URI
   - Example: "Salt (sale)" or `aat:300010967`

6. **Enter Quantity** (`P54_1`):
   - Click "Add value"
   - Enter numeric value: `100`

7. **Add Dimension** (if applicable):
   - Click "Add value" for `P43_1`
   - Select existing dimension resource OR
   - Create new dimension inline:
     - Type: Weight
     - Value: 100
     - Unit: Rubbi
     
8. **Add Color** (`P56_1`) (if specified):
   - Click "Add value"
   - Select from color vocabulary: "White (albus)"

9. **Add Origin** (`P27_1`) (if known):
   - Click "Add value"
   - Link to place resource: `<place_ibiza>`

10. **Add Monetary Value** (if specified):
    - Value Amount: `500.00`
    - Currency: Lire Genovesi
    - Provenance: "Stated in contract line 15"

11. **Save** the object resource

### Linking Object to Contract

1. **Open the Contract Resource**

2. **Find** `gmn:P70_3_indicates_transferred_object` property

3. **Click "Add value"**

4. **Select the Object Resource** you just created

5. **Save** the contract

### Creating Complex Objects with Multiple Properties

**Example: Cloth with Multiple Attributes**

```
Title: "50 pieces of red Flemish cloth"

Properties:
- Name: "Flemish cloth"
- Type: Cloth (pannos) [aat:300014063]
- Count: 50
- Color: Red (ruber)
- Origin: Flanders [place resource]
- Dimension: 
  - Type: Length
  - Value: 25
  - Unit: Canne per piece
- Value Amount: 1250.5
- Value Currency: Lire Genovesi
- Value Provenance: "Contract text, folio 12r"
```

## Validation and Testing

### Data Quality Checklist

Before finalizing any object entry:

- [ ] Object type is assigned (required)
- [ ] Numeric values are properly formatted
- [ ] Units are specified for all measurements
- [ ] Controlled vocabulary terms are used consistently
- [ ] Links to place resources are valid
- [ ] Monetary values include provenance
- [ ] Object is linked to at least one contract

### Test Transformation

1. **Export Contract with Objects** to JSON-LD

2. **Run Transformation Script** on export

3. **Verify Output** includes:
   - E13_Attribute_Assignment nodes
   - P177_assigned_property_of_type (P24 or P30)
   - P141_assigned pointing to object
   - All object properties preserved

4. **Validate** against CIDOC-CRM schema

### Common Validation Issues

| Issue | Solution |
|-------|----------|
| Object type missing | Required field - add from vocabulary |
| Invalid numeric format | Use proper numeric data type |
| Broken resource links | Verify target resource exists |
| Missing units | Always specify unit for measurements |
| Inconsistent terminology | Use controlled vocabularies |

## Advanced Implementation Scenarios

### Scenario 1: Bulk Sale of Mixed Commodities

**Contract**: Sale of various goods

**Approach**: Create multiple object resources, each with their own properties

```
Contract_001
├─ P70.3 → Object_salt (100 rubbi, white, from Ibiza)
├─ P70.3 → Object_wool (50 sacks, from England)
└─ P70.3 → Object_wine (20 barrels, red, from Sicily)
```

### Scenario 2: Partial Transfer

**Contract**: Transfer of custody (lease) without ownership

**Approach**: Use P30 (custody) instead of P24 (ownership) in transformation

Object same as ownership transfer, but semantic layer uses:
- `P30_transferred_custody_of` instead of `P24_transferred_title_of`
- Activity type: `E10_Transfer_of_Custody` instead of `E8_Acquisition`

### Scenario 3: Object Reuse Across Contracts

**Scenario**: Same object appears in multiple transactions

**Approach**: Create one object resource, link to multiple contracts

```
Object_palazzo_001
├─ Linked from: Sale_contract_1450
├─ Linked from: Lease_contract_1452
└─ Linked from: Donation_contract_1455
```

### Scenario 4: Object with Missing Data

**Scenario**: Contract mentions object but provides minimal detail

**Approach**: Create object with available information only

```
Object_unknown_001
├─ Name: "Various goods" (res diverse)
├─ Type: [General merchandise category]
└─ Note: "Details not specified in contract"
```

## Troubleshooting

### Problem: Resource Link Not Appearing

**Symptoms**: When linking object to contract, object doesn't show in selection

**Solutions**:
1. Verify object resource class is compatible
2. Check visibility settings on object resource
3. Ensure object resource is saved and published
4. Clear Omeka-S cache

### Problem: Transformation Fails

**Symptoms**: Python script errors or incomplete output

**Solutions**:
1. Verify JSON-LD export is valid
2. Check property names match ontology exactly
3. Ensure all referenced resources exist
4. Review transformation script error messages

### Problem: Controlled Vocabulary Terms Not Available

**Symptoms**: Can't select terms from dropdown

**Solutions**:
1. Verify Custom Vocab module is active
2. Check vocabulary is properly imported
3. Ensure property is configured to use vocabulary
4. Re-save resource template

### Problem: Numeric Values Not Accepted

**Symptoms**: System rejects numeric input

**Solutions**:
1. Install Numeric Data Types module
2. Configure property to use numeric data type
3. Check format (use decimal point, not comma)
4. Verify no text mixed with numbers

### Problem: Getty AAT URIs Not Resolving

**Symptoms**: Value Suggest not working with AAT

**Solutions**:
1. Check internet connectivity
2. Verify Value Suggest module configuration
3. Test AAT endpoint manually
4. Fall back to custom vocabulary if needed

## Best Practices

### Naming Conventions

**Object Resources:**
- Use descriptive titles that include key attributes
- Format: `[Quantity] [Type] [Distinguishing Feature]`
- Examples:
  - "100 rubbi of white salt from Ibiza"
  - "50 pieces of red Flemish cloth"
  - "1 palazzo on Via Garibaldi"

**Dimension Resources:**
- Format: `[Value] [Unit] [Type] of [Object]`
- Examples:
  - "100 rubbi weight of salt"
  - "25 canne length of cloth"
  - "50 minae weight of pepper"

### Data Consistency

1. **Use Controlled Vocabularies** for all repeating values
2. **Standardize Units** within your project
3. **Document Conversions** if modernizing measurements
4. **Cite Sources** for monetary values
5. **Be Explicit** about uncertainty (use notes)

### Performance Optimization

1. **Batch Create** common object types
2. **Reuse Objects** when appropriate
3. **Index Properties** used in frequent searches
4. **Cache Results** of complex queries
5. **Archive** old/unused objects periodically

### Documentation

1. **Track Changes** to vocabularies
2. **Document Decisions** about ambiguous cases
3. **Maintain Examples** of complex scenarios
4. **Version Control** templates and configurations
5. **Share Knowledge** with team members

## Integration with Other GMN Properties

### Coordinating with Price Properties

When using `gmn:P70_16_documents_sale_price_amount`:

- Use for **overall transaction price**
- Use object monetary value for **individual object values**
- Document relationship in notes if needed

```
Contract:
├─ P70.16: Total price = 2000 lire
├─ P70.3 → Object_A (value: 1200 lire)
└─ P70.3 → Object_B (value: 800 lire)
```

### Working with Party Properties

Coordinate object transfers with buyer/seller:

```
Contract:
├─ P70.1 → Seller (Giovanni)
├─ P70.2 → Buyer (Paolo)
└─ P70.3 → Object (salt)
       └─ Origin: Ibiza (Giovanni's source)
```

### Linking to Events

For complex transactions:

```
Contract → E8_Acquisition → Objects
      ↓
   P4_has_time-span → Date
   P7_took_place_at → Place
```

## Migration from Simple to E13 Pattern

### If You've Been Using Simple References

**Old Approach** (object as text or simple reference):
```turtle
<contract001> gmn:P70_3_indicates_transferred_object "100 rubbi of salt" .
```

**New Approach** (object as resource):
```turtle
<contract001> gmn:P70_3_indicates_transferred_object <object_salt_001> .

<object_salt_001> a gmn:E24_Physical_Human-Made_Thing ;
    gmn:P2_1_has_type <aat:300010967> ;
    gmn:P54_1_has_count "100"^^xsd:integer .
```

### Migration Steps

1. **Audit Existing Data**: Identify contracts with simple object references
2. **Create Object Resources**: For each unique object type
3. **Extract Properties**: Parse existing text for type, quantity, etc.
4. **Link Resources**: Replace text values with resource links
5. **Validate**: Ensure all data migrated correctly
6. **Transform**: Test full CIDOC-CRM export

## Next Steps

After implementing this property:

1. **Train Data Entry Team** on new workflow
2. **Create Sample Objects** for testing
3. **Document Project-Specific** vocabularies
4. **Test Transformation** with real data
5. **Refine Templates** based on feedback
6. **Plan Expansion** to other contract types

## Additional Resources

- **CIDOC-CRM Documentation**: http://www.cidoc-crm.org/
- **Getty AAT**: http://www.getty.edu/research/tools/vocabularies/aat/
- **Omeka-S Manual**: https://omeka.org/s/docs/
- **GMN Project Documentation**: See `/mnt/project/` directory

## Support

For implementation support:
- Review the `Ontology_Documentation.md` for semantic details
- Check the `P70_3_Transformation.py` for transformation logic
- Consult project team for project-specific guidance

---

**Version**: 1.0  
**Last Updated**: October 28, 2025  
**Author**: Genoese Merchant Networks Project
