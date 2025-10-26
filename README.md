# 🗺️ ALICE & Red Cross Demographics Data Repository

**Repository Purpose:** Complete dataset combining ALICE (Asset Limited, Income Constrained, Employed) economic vulnerability data with American Red Cross organizational boundaries and US Census demographics.

**Last Updated:** October 26, 2025
**Repository:** https://github.com/franzenjb/alice-red-cross-data

---

## 🎯 **WHAT THIS REPOSITORY CONTAINS**

This repository combines three critical datasets to create comprehensive geographic analysis tools for the American Red Cross:

1. **ALICE Vulnerability Data** - Economic hardship metrics showing households struggling to afford basic necessities
2. **Red Cross Organizational Data** - Chapter, Region, and Division boundaries with contact information
3. **US Census Demographics** - Population, income, housing, employment, and demographic statistics

**Why This Matters:** The Red Cross can identify where vulnerable populations live, map them to organizational boundaries, and allocate resources effectively.

---

## 📁 **REPOSITORY STRUCTURE**

```
Alice and Demographic Data/
│
├── Alice Chloropleth Maps/          ⭐ PRIMARY FOLDER - READY-TO-USE FILES
│   ├── redcross-counties.zip        (11.8 MB) - Complete county shapefile for ArcGIS
│   ├── alice_counties_2023_CORRECTED.zip  (1.9 MB) - Compact county shapefile
│   ├── redcross-chapters.geojson    (218 chapters with aggregated stats)
│   ├── redcross-regions.geojson     (47 regions with aggregated stats)
│   ├── redcross-divisions.geojson   (6 divisions with aggregated stats)
│   ├── README.md                    (Quick start guide)
│   ├── WORKING_FILES_README.md      (Detailed file documentation)
│   └── Documentation files...
│
├── ArcGIS Outputs/                  🔧 PROCESSED DATA FILES
│   ├── alice_counties_2023_CORRECTED.*  (Shapefile components)
│   ├── red-cross-counties-with-alice-enriched.csv
│   ├── BROKEN_FILES/                (Archived files with data quality issues)
│   └── Other processed outputs...
│
├── Source Data/                     📊 ORIGINAL SOURCE FILES
│   ├── alice_master_database.csv    (11 MB - Original ALICE data)
│   ├── red-cross-counties-with-demographics.csv  (Red Cross + Census data)
│   ├── alice_redcross_master_enriched.csv  (25 MB - Combined dataset)
│   └── County/ZIP/Place boundary files...
│
├── Scripts/                         🐍 PYTHON PROCESSING SCRIPTS
│   ├── create_FIXED_complete_layers.py  (Main data processing)
│   ├── aggregate_alice_for_arcgis.py    (Aggregation logic)
│   ├── fix_all_arcgis_files.py          (File repair attempts)
│   └── create_complete_arcgis_layers.py
│
├── Documentation/                   📖 TECHNICAL DOCUMENTATION
│   ├── SHAPEFILE_FIELD_MAPPING.md   (Field name reference)
│   ├── COMPLETE_LAYERS_GUIDE.md     (Layer creation guide)
│   ├── ARCGIS_POPUP_TEMPLATE.html   (Popup HTML for ArcGIS)
│   └── Project planning docs...
│
└── README.md                        (This file)
```

---

## 🚀 **QUICK START - UPLOAD TO ARCGIS ONLINE**

### **Option 1: Use Pre-Built Files (Recommended)**

1. Navigate to `Alice Chloropleth Maps/` folder
2. Upload **redcross-counties.zip** to ArcGIS Online
3. Publish as hosted feature layer
4. Create choropleth map using `ALICE_Be_1` field (combined vulnerability %)
5. Filter by `Chapter`, `Region`, or `Division`

**Full instructions:** See `Alice Chloropleth Maps/README.md`

### **Option 2: Process Raw Data Yourself**

1. Review source files in `Source Data/`
2. Run `Scripts/create_FIXED_complete_layers.py`
3. Output files appear in `ArcGIS Outputs/`
4. Convert to shapefile and upload to ArcGIS

---

## 📊 **DATA SOURCES**

### **1. ALICE Data (United For ALICE)**
- **Source:** https://www.unitedforalice.org/
- **What It Is:** ALICE = Asset Limited, Income Constrained, Employed
- **Coverage:** County and sub-county level data showing households that earn above the Federal Poverty Level but below the actual cost of living
- **Years Available:** 2010-2023
- **Key Metrics:**
  - Poverty rate (% below federal poverty line)
  - ALICE rate (% above poverty but below survival budget)
  - Combined rate (poverty + ALICE = total struggling households)
  - Household counts and thresholds by age group

### **2. Red Cross Organizational Data**
- **Source:** American Red Cross internal databases
- **What It Is:** Geographic boundaries and organizational structure
- **Coverage:** 3,140+ US counties mapped to:
  - 218 Chapters
  - 47 Regions
  - 6 Divisions
- **Includes:**
  - Contact information (phone, address, time zone)
  - Organizational codes (RCODE, ECODE, DCODE)
  - FEMA region assignments

### **3. US Census Demographics (2023)**
- **Source:** US Census Bureau / Commercial data provider
- **What It Is:** Complete demographic profile for each county
- **Includes:**
  - Population (total, male, female, by age groups)
  - Race/ethnicity breakdowns
  - Housing (owner/renter/vacant, median values)
  - Income (median household, per capita, average)
  - Employment (employed, unemployed, unemployment rate)
  - Geographic data (area, population density)

---

## 🎨 **USE CASES**

### **1. Vulnerability Mapping**
- **Goal:** Identify counties with highest economic hardship
- **Method:** Map `ALICE_Below_ALICE_Threshold_Percentage` (combined poverty + ALICE rate)
- **Filter:** By Red Cross Chapter/Region/Division
- **Output:** Choropleth map showing where to focus resources

### **2. Chapter Benchmarking**
- **Goal:** Compare Red Cross chapters by vulnerability levels in their service areas
- **Method:** Use `Alice Chloropleth Maps/redcross-chapters.geojson`
- **Metrics:** Average ALICE rate, total vulnerable households, population served
- **Output:** Dashboard comparing all 218 chapters

### **3. Grant Targeting**
- **Goal:** Export high-need counties for grant applications
- **Method:** Filter counties where `Combined_Rate > 40%`
- **Export:** List of counties with ALICE data + demographics
- **Use:** Justify need in grant proposals

### **4. Resource Allocation**
- **Goal:** Determine where to open new service locations
- **Method:** Overlay high-vulnerability areas with current chapter boundaries
- **Analysis:** Identify gaps in coverage
- **Output:** Recommendations for new chapter locations

### **5. Demographic Analysis**
- **Goal:** Understand population characteristics in vulnerable areas
- **Method:** Cross-reference ALICE rate with age, race, income demographics
- **Insights:** Target specific vulnerable populations (seniors, families, etc.)
- **Output:** Customized outreach strategies

---

## 📈 **DATA QUALITY & COVERAGE**

### **Coverage Statistics:**

| Geographic Level | Total Features | With ALICE Data | With Red Cross Data | With Demographics |
|------------------|----------------|-----------------|---------------------|-------------------|
| **Counties** | 3,221 | 2,348 (72.9%) | 3,140 (97.5%) | 3,139 (97.5%) |
| **Chapters** | 218 | N/A (aggregated) | 218 (100%) | 218 (100%) |
| **Regions** | 47 | N/A (aggregated) | 47 (100%) | 47 (100%) |
| **Divisions** | 6 | N/A (aggregated) | 6 (100%) | 6 (100%) |

### **Data Quality Notes:**

✅ **High Quality - Ready to Use:**
- County-level data (redcross-counties.zip)
- Chapter/Region/Division aggregations
- All demographic fields validated

❌ **Removed Due to Quality Issues:**
- ZIP code files (68% missing Red Cross data, 32% with incorrect assignments)
- Place/City files (similar data quality issues)

**Why ZIP/Place Files Failed:**
- County FIPS extraction logic was flawed
- Cross-state county name ambiguity caused incorrect joins
- Example: Detroit ZIP 48225 was assigned to Texas chapter instead of Michigan
- Decision: Remove rather than publish incorrect data

---

## 🔧 **TECHNICAL DETAILS**

### **Data Processing Pipeline:**

1. **Load Source Data**
   - ALICE master database (11 MB CSV)
   - Red Cross counties with demographics (1.5 MB CSV)
   - US county boundaries (GeoJSON from Plotly)

2. **Join & Enrich**
   - Join ALICE to Red Cross using County FIPS codes
   - Validate all joins for accuracy
   - Handle missing data (nulls where ALICE unavailable)

3. **Create Geographic Files**
   - Merge data with county boundary geometries
   - Create GeoJSON files (full field names)
   - Convert to shapefiles (10-character field limit)
   - Compress to ZIP files for ArcGIS upload

4. **Aggregate Organizational Levels**
   - Dissolve county boundaries by Chapter/Region/Division
   - Calculate aggregated statistics (sum, average, weighted)
   - Create separate GeoJSON files for each organizational level

5. **Generate Documentation**
   - Field mapping tables (shapefile truncation reference)
   - Popup HTML templates for ArcGIS
   - Analysis guides and tutorials

### **File Formats:**

- **GeoJSON:** Full field names, large files, human-readable
- **Shapefile:** 10-character field names, compressed, ArcGIS native format
- **CSV:** Tabular data, backup/reference, easy to inspect

### **Coordinate Reference System:**
- **CRS:** EPSG:4326 (WGS84)
- **Why:** Standard for web mapping, required by ArcGIS Online
- **Units:** Decimal degrees

---

## 📋 **KEY FIELD NAMES**

### **ALICE Vulnerability Fields:**

| Field Name (Full) | Shapefile (Truncated) | Description |
|-------------------|----------------------|-------------|
| `ALICE_Below_ALICE_Threshold_Percentage` | `ALICE_Be_1` | **PRIMARY METRIC** - Combined poverty + ALICE rate % |
| `ALICE_Poverty_Percentage` | `ALICE_Po_1` | Poverty rate % |
| `ALICE_ALICE_Percentage` | `ALICE_AL_3` | ALICE rate % (working poor) |
| `ALICE_Total_Households` | `ALICE_Hous` | Total households |
| `ALICE_Poverty_Households` | `ALICE_Pove` | Households in poverty |
| `ALICE_ALICE_Households` | `ALICE_ALIC` | Households in ALICE |
| `ALICE_Above_ALICE_Households` | `ALICE_Abov` | Households above ALICE threshold |

### **Red Cross Organizational Fields:**

| Field Name | Description |
|------------|-------------|
| `Chapter` | Red Cross Chapter name |
| `Region` | Red Cross Region name |
| `Division` | Red Cross Division name |
| `FEMA_Region` | FEMA Region number |
| `RCODE` | Region code |
| `ECODE` | Chapter code |
| `DCODE` | Division code |

### **Key Demographics Fields:**

| Field Name (Full) | Shapefile (Truncated) | Description |
|-------------------|----------------------|-------------|
| `Pop_2023` | `Pop_2023` | Total population |
| `Med_HH_Inc_2023` | `Med_HH_Inc` | Median household income |
| `Median_Age_2023` | `Median_Age` | Median age |
| `Unemp_Rate_2023` | `Unemp_Rate` | Unemployment rate % |
| `Diversity_Index_2023` | `Diversity_` | Diversity index |
| `Male_Pop_2023` | `Male_Pop_2` | Male population |
| `Female_Pop_2023` | `Female_Pop` | Female population |

**Full Reference:** See `Documentation/SHAPEFILE_FIELD_MAPPING.md`

---

## ⚠️ **IMPORTANT NOTES**

### **Shapefile 10-Character Limit**
- Shapefiles truncate field names to 10 characters
- **Always refer to field mapping documentation** when working with shapefiles
- GeoJSON files retain full field names if needed

### **Missing ALICE Data**
- ~27% of counties do not have ALICE data (primarily territories, Alaska, some Alabama counties)
- These counties still have Red Cross assignments and demographics
- ALICE fields will be null/empty for these counties

### **File Sizes**
- Large GeoJSON files (35-209 MB) are **NOT tracked in Git**
- Compressed shapefiles (1.9-51 MB) ARE included
- Original CSVs (1.5-25 MB) ARE included
- See `.gitignore` for excluded files

### **Data Vintage**
- ALICE data: 2023 (most recent available)
- Census demographics: 2023
- Red Cross org data: Current as of October 2025
- County boundaries: 2020 Census (TIGER/Line)

---

## 🤝 **CONTRIBUTING**

This is primarily a data repository. If you need to update data:

1. **Update Source Files:**
   - Replace files in `Source Data/` folder
   - Maintain same file naming conventions
   - Ensure FIPS codes are consistent

2. **Run Processing Scripts:**
   - Execute `Scripts/create_FIXED_complete_layers.py`
   - Verify output in `ArcGIS Outputs/`
   - Check for errors in console output

3. **Update Documentation:**
   - If field names change, update `Documentation/SHAPEFILE_FIELD_MAPPING.md`
   - Update coverage statistics in this README
   - Update vintage dates

4. **Commit Changes:**
   - Commit source data updates
   - Commit processed outputs (under 100 MB)
   - Update .gitignore for large files
   - Push to repository

---

## 📞 **QUESTIONS & SUPPORT**

**For ArcGIS Upload Issues:**
- See `Alice Chloropleth Maps/WORKING_FILES_README.md`
- Check ArcGIS file size limits (100 MB for web upload, larger if using REST API)
- Verify shapefile components are all present (.shp, .shx, .dbf, .prj)

**For Data Quality Issues:**
- Review original source files in `Source Data/`
- Check processing logs from Python scripts
- Verify FIPS code matching in joins

**For Field Name Questions:**
- See `Documentation/SHAPEFILE_FIELD_MAPPING.md`
- GeoJSON files have full field names for reference

**Repository Issues:**
- Open an issue in GitHub: https://github.com/franzenjb/alice-red-cross-data/issues

---

## 📜 **LICENSE & ATTRIBUTION**

**Data Sources:**
- ALICE Data: © United For ALICE, used with permission for Red Cross internal analysis
- Red Cross Data: © American Red Cross, internal use only
- Census Data: Public domain (US Census Bureau)
- County Boundaries: Public domain (US Census TIGER/Line)

**Code:**
- Python scripts: MIT License (see LICENSE file)

**Usage Restrictions:**
- ALICE data: Internal Red Cross use only, do not redistribute
- Red Cross organizational data: Internal use only
- Combined datasets: Internal Red Cross use only
- Maps/visualizations created from this data: May be shared publicly with proper attribution

---

## 🎉 **READY TO USE!**

**Quick Links:**
- **Main Data Folder:** `Alice Chloropleth Maps/`
- **Quick Start Guide:** `Alice Chloropleth Maps/README.md`
- **Detailed Documentation:** `Documentation/`
- **Source Data:** `Source Data/`

**Next Steps:**
1. Navigate to `Alice Chloropleth Maps/`
2. Upload `redcross-counties.zip` to ArcGIS Online
3. Create your first vulnerability choropleth map
4. Start making data-driven decisions!

---

**Last Updated:** October 26, 2025
**Repository:** https://github.com/franzenjb/alice-red-cross-data
**Maintained By:** American Red Cross Data Team
