# Building a Powerful ALICE Data Filter & Analysis Tool

## Overview
This guide will help you build a comprehensive ArcGIS Experience Builder application with:
- ✅ Multi-level filtering (County, Chapter, Region, Division)
- ✅ Toggle between ZIP code and County views
- ✅ ALICE data filtering (poverty %, ALICE %, combined %)
- ✅ Bivariate choropleth analysis
- ✅ Interactive dashboards and statistics

---

## STEP 1: Upload All Layers to ArcGIS Online

### A. Upload County Layer (Already Done?)
**File:** `/Desktop/Alice Chloropleth Maps/redcross-counties-ARCGIS-UPLOAD.zip` (11.7 MB)

1. Go to https://www.arcgis.com → Content → New Item
2. Upload: `redcross-counties-ARCGIS-UPLOAD.zip`
3. **Title:** Red Cross Counties - Demographics & ALICE
4. **Tags:** red cross, counties, demographics, alice, poverty
5. Publish as hosted feature layer

### B. Upload ZIP Code Layers by Division
**Location:** `/Desktop/Alice and Demographic Data/ArcGIS Outputs/zip_by_division/`

Upload each division separately:

| File | Size | ZIP Codes |
|------|------|-----------|
| alice-zipcodes-Central_Atlantic_Division.zip | 335 KB | ~1,500 |
| alice-zipcodes-North_Central_Division.zip | 948 KB | ~4,000 |
| alice-zipcodes-Northeast_Division.zip | 479 KB | ~2,000 |
| alice-zipcodes-Pacific_Division.zip | 234 KB | ~1,000 |
| alice-zipcodes-Southeast_and_Caribbean_Division.zip | 27 KB | ~100 |

**For each file:**
1. Content → New Item → Upload
2. **Title:** ALICE ZIP Codes - [Division Name]
3. **Tags:** alice, zip codes, [division name], financial hardship
4. Publish as hosted feature layer

**Skip "Not_Assigned" for now** (25 MB - too large, mostly unmapped territories)

### C. Upload Chapter/Region/Division Boundary Layers
**Location:** `/Desktop/Alice Chloropleth Maps/`

These provide aggregated statistics:

1. **redcross-chapters.geojson** (11 MB) - 218 chapters
2. **redcross-regions.geojson** (7.4 MB) - 47 regions
3. **redcross-divisions.geojson** (5.6 MB) - 6 divisions

Upload each as GeoJSON (under 50 MB limit):
- Content → New Item → Upload → Publish as feature layer

---

## STEP 2: Create Web Map with Multiple Layers

1. Go to **Content** → **Create** → **Map**
2. Add all layers:
   - Counties layer
   - All 5 ZIP code division layers (we'll filter these)
   - Chapters layer
   - Regions layer
   - Divisions layer

3. **Configure Layer Visibility:**
   - Set Counties layer as **visible by default**
   - Set all ZIP layers as **hidden by default**
   - Set Chapter/Region/Division as **reference layers** (outline only)

4. **Style the Layers:**

### County Layer Styling:
- Click layer → Styles → Choose an attribute
- **Primary Field:** `ALICE_Be_1` (Below ALICE Threshold %)
- **Style:** Counts and Amounts (Color)
- **Color Ramp:** Yellow to Red (low to high hardship)
- **Classification:** Natural Breaks, 5 classes
- **Label:** "Financial Hardship - Below ALICE Threshold %"

### ZIP Code Layers Styling:
For each ZIP division layer:
- **Primary Field:** `Combined_R` (Combined Rate %)
- **Style:** Counts and Amounts (Color)
- **Color Ramp:** Yellow to Red
- **Classification:** Natural Breaks, 5 classes

5. **Configure Popups:**

### County Popup Template:
```
Title: {County}, {County_ST}

Content:
RED CROSS ORGANIZATION
Chapter: {Chapter}
Region: {Region}
Division: {Division}

ALICE DATA (Financial Hardship)
Below ALICE Threshold: {ALICE_Be_1}%
Poverty Rate: {ALICE_Po_1}%
ALICE Rate: {ALICE_AL_3}%

DEMOGRAPHICS
Population (2023): {Pop_2023}
Median Household Income: ${Med_HH_Inc}
Unemployment Rate: {Unemp_Rate}%
Median Age: {Median_Age}
```

### ZIP Code Popup Template:
```
Title: ZIP Code {ZCTA5CE20}

Content:
LOCATION
County: {RC_County_}
Chapter: {RC_Chapter}
Division: {RC_Divisio}

ALICE DATA
Combined Rate: {Combined_R}%
Poverty Rate: {Poverty_Ra}%
ALICE Rate: {ALICE_Rate}%
Total Households: {Total_Hous}
```

6. **Save Map:**
   - Name: "Red Cross ALICE Analysis - Master Map"
   - Tags: red cross, alice, analysis, counties, zip codes
   - Summary: "Comprehensive ALICE financial hardship data with multi-level filtering"

---

## STEP 3: Create Experience Builder App

1. Go to **Content** → Find your map → **Create Web Experience**
2. Choose **Experience Builder**
3. Select template: **Dart** (has sidebar for filters) or **Sidebar** template

### Layout Structure:
```
┌─────────────────────────────────────────────┐
│  HEADER: Red Cross ALICE Analysis Tool     │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ SIDEBAR  │         MAP VIEW                 │
│ FILTERS  │    (Counties or ZIP codes)       │
│          │                                  │
│          │                                  │
├──────────┴──────────────────────────────────┤
│  STATISTICS PANEL (Charts & Indicators)     │
└─────────────────────────────────────────────┘
```

---

## STEP 4: Add Filter Widgets

### Filter 1: Geographic Level Toggle
**Widget:** Tabs or Button widget

```
Tab 1: County View (default)
  - Shows county layer
  - Hides all ZIP layers

Tab 2: ZIP Code View
  - Hides county layer
  - Shows ZIP layers for selected division
```

**Configuration:**
1. Add **Tabs widget** to sidebar
2. Create 2 tabs: "Counties" and "ZIP Codes"
3. For each tab, configure **Actions**:
   - County tab: Show Counties layer, Hide ZIP layers
   - ZIP tab: Show ZIP layers, Hide Counties layer

### Filter 2: Red Cross Organization Filter
**Widget:** Filter widget (cascading)

```
Dropdown 1: Division
  → Filters → Dropdown 2: Region
    → Filters → Dropdown 3: Chapter
      → Filters → Counties
```

**Configuration:**
1. Add **Filter widget**
2. **Connect to:** Counties layer (or active layer)
3. **Filter by:**
   - Division (field: `Division`)
   - Region (field: `Region`) - cascades from Division
   - Chapter (field: `Chapter`) - cascades from Region
4. **Style:** Dropdowns
5. **Allow multiple:** Yes

### Filter 3: ALICE Data Range Sliders
**Widget:** Filter widget with sliders

**Configuration:**
1. Add another **Filter widget**
2. **Connect to:** Active layer (Counties or ZIP)
3. **Add filters for:**

   - **Below ALICE Threshold %** (0-100%)
     - Field: `ALICE_Be_1` (counties) or `Combined_R` (ZIP)
     - Widget type: Slider
     - Min: 0, Max: 100
     - Label: "Below ALICE Threshold %"

   - **Poverty Rate %** (0-100%)
     - Field: `ALICE_Po_1` (counties) or `Poverty_Ra` (ZIP)
     - Widget type: Slider
     - Min: 0, Max: 100

   - **ALICE Only Rate %** (0-100%)
     - Field: `ALICE_AL_3` (counties) or `ALICE_Rate` (ZIP)
     - Widget type: Slider
     - Min: 0, Max: 100

4. **Display:** Show values, allow manual input

### Filter 4: Demographic Filters (Optional)
Add sliders for:
- Population range
- Median Income range
- Unemployment Rate range

---

## STEP 5: Add Statistics & Charts

### Widget 1: Summary Statistics
**Widget:** Indicator widget (multiple)

Show real-time stats based on filtered data:

1. **Total Population** (sum of Pop_2023)
2. **Total Households** (sum of Total_HH_2)
3. **Average Below ALICE %** (average of ALICE_Be_1)
4. **Counties/ZIPs Displayed** (count)

**Configuration:**
- Add 4 **Indicator widgets**
- Connect each to map layer
- Use **Statistics** → Sum or Average
- **Update on:** Map extent change + filter change

### Widget 2: ALICE Distribution Chart
**Widget:** Chart widget - Bar chart

**Configuration:**
- Type: Bar chart
- X-axis: ALICE categories (Poverty, ALICE, Above ALICE)
- Y-axis: Number of households
- Data: From filtered layer
- Categories:
  - Poverty: `ALICE_Pove` field
  - ALICE: `ALICE_ALIC` field
  - Above ALICE: `ALICE_Abov` field

### Widget 3: Top 10 Highest Hardship
**Widget:** List widget or Table widget

**Configuration:**
- Connect to active layer
- Sort by: `ALICE_Be_1` descending
- Show top 10 counties/ZIPs
- Display: County name, Below ALICE %, Population
- Click to zoom to feature

---

## STEP 6: Bivariate Choropleth Setup

Bivariate choropleths show TWO variables at once using color mixing.

### Option A: Pre-create Bivariate Categories (Recommended)

**Before uploading**, add a calculated field:

1. Go back to your GeoJSON files
2. Create a new field: `Bivariate_Class`
3. Calculate based on two variables:
   - Variable 1: Below ALICE Threshold % (Low/Med/High)
   - Variable 2: Median Income (Low/Med/High)

**Logic:**
```
Low ALICE + High Income = Class 1 (light yellow)
Low ALICE + Med Income = Class 2
Low ALICE + Low Income = Class 3 (orange)

Med ALICE + High Income = Class 4
Med ALICE + Med Income = Class 5
Med ALICE + Low Income = Class 6

High ALICE + High Income = Class 7
High ALICE + Med Income = Class 8 (red)
High ALICE + Low Income = Class 9 (dark red) ← HIGHEST NEED
```

**Then in ArcGIS:**
1. Style by `Bivariate_Class`
2. Use **Unique Values** renderer
3. Assign custom colors for each class
4. Create legend showing 3x3 grid

### Option B: Use ArcGIS Smart Mapping (Easier)

**Coming in 2024 - ArcGIS Pro only for now**

ArcGIS Online doesn't natively support bivariate choropleths yet, but you can:

1. Create the map in **ArcGIS Pro**
2. Use **Relationship** renderer
3. Variable 1: Below ALICE %
4. Variable 2: Median Income
5. Publish to ArcGIS Online
6. Use in Experience Builder

### Option C: Create Custom Web App

I can build a custom web app using:
- ArcGIS JavaScript API
- Custom bivariate color scheme
- Interactive legend with 3x3 grid

Would you like me to create this?

---

## STEP 7: Advanced Features

### Feature 1: Compare Two Areas
**Widget:** Comparison widget

1. Add **Side by Side widget**
2. Load same map twice
3. Filter each side differently
4. Compare statistics

### Feature 2: Export Filtered Data
**Widget:** Export widget

Allow users to download filtered results as CSV or Excel

### Feature 3: Print/Share
**Widget:** Print widget

Generate PDF reports of current view with filters applied

---

## FILE SUMMARY

### Ready to Upload NOW:

**Counties:**
- `/Desktop/Alice Chloropleth Maps/redcross-counties-ARCGIS-UPLOAD.zip` (11.7 MB)

**ZIP Codes by Division:**
- `/ArcGIS Outputs/zip_by_division/alice-zipcodes-Central_Atlantic_Division.zip` (335 KB)
- `/ArcGIS Outputs/zip_by_division/alice-zipcodes-North_Central_Division.zip` (948 KB)
- `/ArcGIS Outputs/zip_by_division/alice-zipcodes-Northeast_Division.zip` (479 KB)
- `/ArcGIS Outputs/zip_by_division/alice-zipcodes-Pacific_Division.zip` (234 KB)
- `/ArcGIS Outputs/zip_by_division/alice-zipcodes-Southeast_and_Caribbean_Division.zip` (27 KB)

**Aggregated Boundaries:**
- `/Desktop/Alice Chloropleth Maps/redcross-chapters.geojson` (11 MB)
- `/Desktop/Alice Chloropleth Maps/redcross-regions.geojson` (7.4 MB)
- `/Desktop/Alice Chloropleth Maps/redcross-divisions.geojson` (5.6 MB)

---

## NEXT STEPS

**Choose your path:**

### Path 1: Full Experience Builder (Recommended for most users)
1. Upload all layers above
2. Create web map
3. Build Experience Builder app following this guide
4. No coding required!

### Path 2: Custom Web App with Bivariate Choropleths
I can build you a custom JavaScript web app with:
- Advanced bivariate choropleth visualization
- Custom filter controls
- Modern, responsive design
- Embedded statistics
- Would you like me to create this?

### Path 3: ArcGIS Dashboards (Simpler, less flexible)
- Faster to build
- Great for executives/stakeholders
- Limited interaction compared to Experience Builder

**Which path would you like to take?**
