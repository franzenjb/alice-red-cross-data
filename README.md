# 🎯 ALICE & Red Cross Demographics Project

**Last Updated:** October 25, 2025
**Status:** ✅ Complete - All 3,221 US counties uploaded to ArcGIS Online

---

## 📊 **PROJECT SUMMARY**

This project combines **ALICE vulnerability data** with **Red Cross demographic information** to create comprehensive county-level analysis tools for ArcGIS Online.

### **What You Have:**
- ✅ **3,221 US counties** with complete demographic and ALICE data
- ✅ **67 data fields** per county (ALICE metrics + Red Cross demographics)
- ✅ **Shapefile uploaded** to ArcGIS Online as hosted feature layer
- ✅ **Time series data** (2010-2023) for trend analysis
- ✅ **Chapter, Region, Division** aggregations for organizational reporting

---

## 📁 **FOLDER STRUCTURE**

```
Alice and Demographic Data/
│
├── ArcGIS Outputs/          ⭐ PRIMARY FILES - USE THESE
│   ├── alice_counties_2023_CORRECTED.zip        (1.9 MB - UPLOADED TO ARCGIS ✅)
│   ├── alice_counties_2023_CORRECTED.geojson    (8.1 MB - Master with full field names)
│   ├── alice_Northeast_FIXED2.geojson           (Regional example)
│   ├── alice_counties_all_years.geojson         (Time series 2010-2023)
│   ├── alice_county_2023.csv                    (County-level 2023)
│   ├── alice_chapter_summary.csv                (Chapter aggregations)
│   ├── alice_region_summary.csv                 (Region aggregations)
│   ├── alice_division_summary.csv               (Division aggregations)
│   ├── alice_zipcodes_2023_COMPLETE.csv         (Sub-county ZIP codes)
│   └── red-cross-counties-with-alice-enriched.csv
│
├── Documentation/           📖 GUIDES & REFERENCES
│   ├── SHAPEFILE_FIELD_MAPPING.md               (Field name reference - IMPORTANT!)
│   ├── ARCGIS_POPUP_TEMPLATE.html               (Beautiful popup HTML - USE THIS!)
│   ├── COMPLETE_LAYERS_GUIDE.md                 (Complete analysis guide)
│   ├── ARCGIS_ALICE_DASHBOARD_GUIDE.md          (Dashboard creation guide)
│   ├── ALICE-Project-Summary.md
│   └── Other planning documents
│
├── Source Data/            💾 ORIGINAL DATA FILES
│   ├── alice_master_database.csv                (11 MB - Original ALICE data)
│   ├── alice_redcross_master_enriched.csv       (25 MB - Combined dataset)
│   ├── red-cross-counties-with-demographics.csv (1.5 MB - RC demographics)
│   └── Backup files
│
└── Scripts/                🔧 DATA PROCESSING SCRIPTS
    ├── create_complete_arcgis_layers.py
    ├── create_FIXED_complete_layers.py
    └── aggregate_alice_for_arcgis.py
```

---

## 🚀 **QUICK START - ARCGIS ONLINE**

### **1. Your Layer is Already Uploaded**
The file **`alice_counties_2023_CORRECTED.zip`** has been successfully uploaded to ArcGIS Online as a hosted feature layer.

### **2. Configure Beautiful Popups**
1. Open your layer in ArcGIS Online
2. Go to **Configure Popup**
3. Switch to **Custom** mode
4. Copy/paste the HTML from **`Documentation/ARCGIS_POPUP_TEMPLATE.html`**
5. Save

### **3. Create Choropleth Maps**

**Option A: ALICE Vulnerability**
- Style by: `Combined_R` (Combined poverty + ALICE rate %)
- Color scheme: Green (low) → Red (high)
- Filter by: `RC_Chapter`, `RC_Region`, or `RC_Divisio`

**Option B: Income Analysis**
- Style by: `Med_HH_Inc` (Median household income)
- Compare with `ALICE_Rate` in popup

**Option C: Demographics**
- Style by: `Diversity_` (Diversity index)
- Style by: `Median_Age` (Median age)
- Style by: `Pop_Den_20` (Population density)

---

## 📋 **IMPORTANT: FIELD NAMES**

Due to shapefile's 10-character limit, field names are truncated. **See `Documentation/SHAPEFILE_FIELD_MAPPING.md` for the complete reference.**

### **Most Common Fields (Quick Reference):**

| Truncated Name | Full Name | Description |
|---------------|-----------|-------------|
| `Combined_R` | Combined_Rate_Pct | Combined poverty + ALICE rate (%) |
| `ALICE_Rate` | ALICE_Rate_Pct | ALICE rate only (%) |
| `Male_Pop_2` | Male_Pop_2023 | Male population 2023 |
| `Female_Pop` | Female_Pop_2023 | Female population 2023 |
| `Med_HH_Inc` | Med_HH_Inc_2023 | Median household income |
| `Diversity_` | Diversity_Index_2023 | Diversity index |
| `RC_Chapter` | RC_Chapter | Red Cross Chapter |
| `RC_Region` | RC_Region | Red Cross Region |
| `RC_Divisio` | RC_Division | Red Cross Division |
| `Median_Age` | Median_Age_2023 | Median age |
| `Pop_Den_20` | Pop_Den_2023 | Population density per sq mi |
| `Unemp_Rate` | Unemp_Rate_2023 | Unemployment rate (%) |

---

## 💡 **ANALYSIS IDEAS**

### **1. Vulnerability Hotspots**
Filter to counties where `Combined_R` > 40% to identify areas with highest need.

### **2. Chapter Performance**
Group by `RC_Chapter` and calculate average `ALICE_Rate` to benchmark chapters.

### **3. Income vs Vulnerability**
Create scatter plot: X-axis = `Med_HH_Inc`, Y-axis = `Combined_R`

### **4. Aging Population Analysis**
Filter to `Median_Age` > 45 AND `ALICE_Rate` > 30% for vulnerable aging communities.

### **5. Urban vs Rural**
Classify by `Pop_Den_20`:
- Rural: < 100 people/sq mi
- Suburban: 100-1,000
- Urban: > 1,000

Compare average vulnerability rates.

---

## 📊 **DATA COVERAGE**

| Geographic Level | Records | Coverage | File |
|-----------------|---------|----------|------|
| **Counties** | 3,221 | All US counties | alice_counties_2023_CORRECTED.zip ✅ |
| **ZIP Codes** | 64,719 | Partial US | alice_zipcodes_2023_COMPLETE.csv |
| **Chapters** | 171 | All RC chapters | alice_chapter_summary.csv |
| **Regions** | 40 | All RC regions | alice_region_summary.csv |
| **Divisions** | 7 | All RC divisions | alice_division_summary.csv |

---

## 🎨 **POPUP TEMPLATE**

The **`ARCGIS_POPUP_TEMPLATE.html`** includes:

✅ **ALICE Vulnerability Section**
- Combined rate (poverty + ALICE)
- ALICE rate only
- Household breakdown (poverty, ALICE, above ALICE)

✅ **Demographics Section**
- Total population, male/female split
- Median age, diversity index
- Age distribution (4 groups)

✅ **Economic Indicators**
- Median household income
- Per capita income
- Unemployment rate

✅ **Housing Section**
- Median home value
- Total housing units
- Owner/renter/vacant breakdown

✅ **Red Cross Organization**
- Chapter, Region, Division
- FEMA Region
- Contact phone and time zone

**Design:** Modern gradient headers, color-coded sections, responsive grid layout

---

## 🔧 **TECHNICAL NOTES**

### **Why Shapefile Instead of GeoJSON?**
- GeoJSON (8.1 MB, 3,221 features) failed to upload via ArcGIS Online web interface
- Shapefile (1.9 MB ZIP) uploaded successfully
- Shapefile is Esri's native format = better compatibility

### **Field Name Truncation**
- Shapefiles have 10-character field name limit
- All longer names automatically truncated
- Use `SHAPEFILE_FIELD_MAPPING.md` as reference
- Original GeoJSON has full field names if needed

### **Data Sources**
- **ALICE Data:** ALICE Project (United For ALICE) 2023
- **Red Cross Demographics:** Red Cross internal database 2023
- **County Boundaries:** Plotly public datasets (GeoJSON)

---

## ✅ **SUCCESS METRICS**

✅ All 3,221 US counties with demographic data
✅ 67 fields per county (ALICE + demographics)
✅ Successfully uploaded to ArcGIS Online
✅ Beautiful popup template created
✅ Field mapping documentation complete
✅ Organized folder structure
✅ Time series data available (2010-2023)
✅ Chapter/Region/Division aggregations ready

---

## 📞 **NEXT STEPS**

1. **Apply the popup template** to your ArcGIS layer using the HTML file
2. **Create your first choropleth** using `Combined_R` field
3. **Build a dashboard** combining county map + chapter summary table
4. **Filter by Chapter/Region** to create targeted views
5. **Export high-need counties** (Combined_R > 40%) for grant applications

---

**🎊 PROJECT COMPLETE - READY FOR ANALYSIS!**

*All files organized, documented, and ready for ArcGIS Online use.*
