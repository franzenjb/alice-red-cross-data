# 🗺️ Red Cross Choropleth Maps - Complete Data Package

**Last Updated:** October 26, 2025
**Status:** ✅ Ready for ArcGIS Online Upload

---

## 🎯 **WHAT YOU HAVE**

This folder contains **complete, verified, ready-to-upload** Red Cross demographic and ALICE vulnerability data for creating choropleth maps in ArcGIS Online.

### **✅ WORKING FILES (Upload These!)**

1. **redcross-counties.zip** (11.8 MB) ⭐ **RECOMMENDED**
   - 3,140 US counties
   - 82 fields with complete Red Cross + ALICE + Census data
   - Shapefile format (10-char field names)
   - **BEST FOR:** Most users, complete organizational analysis

2. **alice_counties_2023_CORRECTED.zip** (1.9 MB)
   - 3,221 US counties (complete coverage)
   - 67 essential fields
   - Smaller file size
   - **BEST FOR:** Complete US coverage, compact datasets

3. **redcross-chapters.geojson** (11 MB)
   - 218 Red Cross Chapters
   - Aggregated statistics
   - **BEST FOR:** Chapter-level comparisons

4. **redcross-regions.geojson** (7.4 MB)
   - 47 Red Cross Regions
   - Aggregated statistics
   - **BEST FOR:** Regional analysis

5. **redcross-divisions.geojson** (5.6 MB)
   - 6 Red Cross Divisions
   - Aggregated statistics
   - **BEST FOR:** National overview

6. **redcross-counties-arcgis.csv** (1.7 MB)
   - CSV backup of county data
   - **BEST FOR:** Spreadsheet analysis, data joining

---

## 🚀 **QUICK START - UPLOAD TO ARCGIS**

### **Step 1: Upload redcross-counties.zip**

1. Go to https://www.arcgis.com → Sign In
2. **Content** → **New Item** → **From your computer**
3. Select **redcross-counties.zip**
4. ✅ Check **"Publish this file as a hosted layer"**
5. Title: "Red Cross Counties - ALICE Vulnerability 2023"
6. Tags: `red-cross, demographics, alice, vulnerability, 2023`
7. Click **Publish**
8. Wait 1-2 minutes ✅

### **Step 2: Create Your First Choropleth**

1. Open the layer → **Open in Map Viewer**
2. Click **Styles** → **Choose field:** `ALICE_Be_1`
3. **Method:** Natural Breaks
4. **Classes:** 5
5. **Colors:** Green → Red (low to high vulnerability)
6. Save your map!

---

## 📊 **KEY FIELDS FOR MAPPING**

### **Primary Vulnerability Metrics:**

| Field Name | Full Name | Description |
|------------|-----------|-------------|
| **`ALICE_Be_1`** | ALICE_Below_ALICE_Threshold_Percentage | **🎯 PRIMARY** - Combined poverty + ALICE rate % |
| `ALICE_Po_1` | ALICE_Poverty_Percentage | Poverty rate % |
| `ALICE_AL_3` | ALICE_ALICE_Percentage | ALICE rate % (working poor) |

### **Key Demographics:**

| Field Name | Full Name | Description |
|------------|-----------|-------------|
| `Pop_2023` | Pop_2023 | Total population |
| `Med_HH_Inc` | Med_HH_Inc_2023 | Median household income |
| `Median_Age` | Median_Age_2023 | Median age |
| `Unemp_Rate` | Unemp_Rate_2023 | Unemployment rate % |
| `Diversity_` | Diversity_Index_2023 | Diversity index |

### **Red Cross Organization:**

| Field Name | Full Name | Description |
|------------|-----------|-------------|
| `Chapter` | Chapter | Red Cross Chapter name |
| `Region` | Region | Red Cross Region name |
| `Division` | Division | Red Cross Division name |
| `FEMA_Regio` | FEMA_Region | FEMA Region number |

---

## 📖 **DOCUMENTATION**

- **WORKING_FILES_README.md** - Detailed file descriptions and upload guide
- **ARCGIS_CHOROPLETH_COMPLETE_GUIDE.md** - Complete tutorial for creating maps
- **DATA_SUMMARY.md** - Data coverage and statistics
- **QUICK_START.md** - 10-minute getting started guide

---

## ⚠️ **IMPORTANT: Sub-County Files Not Available**

**ZIP code and Places files have been removed** due to data quality issues:
- 68% of records had missing Chapter/Region assignments
- Remaining 32% had incorrect assignments (e.g., Michigan ZIPs showing Texas chapters)

**For now:** Use county-level data as the finest geographic granularity.

---

## ✅ **WHAT'S INCLUDED IN THE DATA**

### **Red Cross Organization (All Files):**
- Chapter name, Region name, Division name
- RCODE, ECODE, DCODE
- FEMA Region
- Contact information (phone, address, time zone)

### **Census Demographics 2023 (Counties Only):**
- Population (total, male, female, by age groups)
- Race/ethnicity (White, Black, Hispanic, Asian, etc.)
- Housing (owner, renter, vacant, median value, average value)
- Income (median household, per capita, average household)
- Employment (employed, unemployed, unemployment rate)
- Geography (area in sq mi, population density)

### **ALICE Vulnerability Data:**
- Total households
- Poverty households & percentage
- ALICE households & percentage (working poor)
- Above ALICE households & percentage
- **Combined rate** (poverty + ALICE) - PRIMARY METRIC
- ALICE thresholds by age group

---

## 🎨 **RECOMMENDED VISUALIZATIONS**

### **1. Vulnerability Hotspots Map**
- **Layer:** redcross-counties.zip
- **Field:** `ALICE_Be_1` (Combined vulnerability %)
- **Colors:** Green → Yellow → Orange → Red
- **Filter:** By `Chapter` or `Region`

### **2. Income vs Vulnerability Dashboard**
- **Map:** `Med_HH_Inc` (Median income)
- **Chart:** Top 10 counties by `ALICE_Be_1`
- **Indicator:** Average `ALICE_Po_1` (Poverty %)

### **3. Chapter Comparison**
- **Layer:** redcross-chapters.geojson
- **Field:** Chapter-level aggregated `ALICE_Below_ALICE_Threshold_Percentage`
- **Chart:** Bar chart comparing all chapters

---

## 📞 **NEXT STEPS**

1. ✅ **Upload** redcross-counties.zip to ArcGIS Online
2. 🎨 **Create** your first choropleth using `ALICE_Be_1` field
3. 🔍 **Filter** by Chapter/Region/Division
4. 📊 **Build** a dashboard with maps, charts, and indicators
5. 📤 **Share** with your team!

---

## 🎉 **YOU'RE READY!**

All files are verified, clean, and ready for upload. Start with **redcross-counties.zip** for the best experience.

**Questions?** See the detailed guides in this folder.

---

**Repository:** https://github.com/franzenjb/arc-relationship-manager

**Last Verified:** October 26, 2025
