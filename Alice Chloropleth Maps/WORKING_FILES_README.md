# ✅ WORKING ARCGIS FILES - READY FOR UPLOAD

**Last Updated:** October 26, 2025

---

## 📦 **AVAILABLE FILES FOR ARCGIS UPLOAD**

### **1. redcross-counties.zip** (11.8 MB) ⭐ RECOMMENDED
- **Format:** Shapefile (compressed ZIP)
- **Coverage:** 3,140 US counties
- **Fields:** 82 fields (truncated to 10 characters for shapefile)
- **Status:** ✅ Ready for ArcGIS Online upload

**What's Included:**
- **Red Cross Organization:** Chapter, Region, Division, FEMA Region
- **Census Demographics 2023:** Population, income, housing, age, race, employment
- **ALICE Vulnerability Data:** Poverty rate, ALICE rate, combined rate, household counts
- **Geographic Data:** County names, state, FIPS codes, area

**Use This For:**
- County-level choropleth maps
- Filtering by Chapter/Region/Division
- Complete Red Cross organizational analysis
- Primary mapping layer

---

### **2. alice_counties_2023_CORRECTED.zip** (1.9 MB)
- **Format:** Shapefile (compressed ZIP)
- **Coverage:** 3,221 US counties (complete coverage)
- **Fields:** 67 fields (truncated to 10 characters)
- **Status:** ✅ Ready for ArcGIS Online upload

**What's Included:**
- **ALICE Vulnerability Data:** Combined rate, ALICE rate, poverty rate, household counts
- **Red Cross Organization:** Chapter, Region, Division (where available)
- **Census Demographics 2023:** Key demographics from parent county

**Differences from redcross-counties.zip:**
- ✅ **Complete US coverage** (81 more counties)
- ✅ **Smaller file size** (1.9 MB vs 11.8 MB)
- ⚠️ Fewer fields (67 vs 82)
- ⚠️ Some counties may have missing Red Cross assignments

---

## 🚀 **HOW TO UPLOAD TO ARCGIS ONLINE**

### **Recommended: Start with redcross-counties.zip**

1. Go to **ArcGIS Online** → **Content** → **Add Item**
2. Select **"From your computer"**
3. Choose **redcross-counties.zip**
4. ✅ **IMPORTANT:** Check **"Publish this file as a hosted layer"**
5. Set title: "Red Cross Counties - Demographics & ALICE 2023"
6. Set tags: red-cross, demographics, alice, vulnerability, 2023
7. Click **Publish**
8. Wait 1-2 minutes for processing

### **Alternative: Use alice_counties_2023_CORRECTED.zip**

- Use if you need complete US coverage (all 3,221 counties)
- Follow same upload steps as above
- Title: "ALICE County Vulnerability 2023 - Complete US"

---

## 🎨 **CREATING CHOROPLETH MAPS**

### **Key Fields for Mapping:**

#### **redcross-counties.zip:**
- `ALICE_Be_1` = ALICE_Below_ALICE_Threshold_Percentage (Combined poverty + ALICE %)
- `ALICE_Po_1` = ALICE_Poverty_Percentage (Poverty rate %)
- `ALICE_AL_3` = ALICE_ALICE_Percentage (ALICE rate %)
- `Chapter` = Red Cross Chapter
- `Region` = Red Cross Region
- `Division` = Red Cross Division
- `Pop_2023` = Total population
- `Med_HH_Inc` = Median household income
- `Median_Age` = Median age
- `Unemp_Rate` = Unemployment rate
- `Diversity_` = Diversity index

#### **alice_counties_2023_CORRECTED.zip:**
- `Combined_R` = Combined_Rate_Pct (Poverty + ALICE %)
- `ALICE_Rate` = ALICE_Rate_Pct (ALICE only %)
- `Poverty_Ra` = Poverty_Rate_Pct (Poverty only %)
- `RC_Chapter` = Red Cross Chapter
- `RC_Region` = Red Cross Region
- `RC_Divisio` = Red Cross Division
- `Pop_2023` = Total population
- `Med_HH_Inc` = Median household income

### **Recommended Choropleth Settings:**

**For Vulnerability Analysis:**
- **Field:** `ALICE_Be_1` (redcross) or `Combined_R` (alice)
- **Method:** Natural Breaks
- **Classes:** 5
- **Colors:** Green (low) → Red (high)

**For Income Analysis:**
- **Field:** `Med_HH_Inc`
- **Method:** Natural Breaks
- **Classes:** 5
- **Colors:** Red (low) → Green (high)

**For Population:**
- **Field:** `Pop_2023`
- **Method:** Quantile
- **Classes:** 5
- **Colors:** Light Blue → Dark Blue

---

## 📊 **FIELD NAME REFERENCE**

### **Important: Shapefile 10-Character Limit**

Shapefiles truncate field names to 10 characters. Here's a quick reference:

| Truncated | Full Name | Description |
|-----------|-----------|-------------|
| `ALICE_Be_1` | ALICE_Below_ALICE_Threshold_Percentage | **PRIMARY METRIC** - Combined poverty + ALICE rate % |
| `ALICE_Po_1` | ALICE_Poverty_Percentage | Poverty rate % |
| `ALICE_AL_3` | ALICE_ALICE_Percentage | ALICE rate % (working poor) |
| `Med_HH_Inc` | Med_HH_Inc_2023 | Median household income |
| `Pop_2023` | Pop_2023 | Total population |
| `Median_Age` | Median_Age_2023 | Median age |
| `Unemp_Rate` | Unemp_Rate_2023 | Unemployment rate % |
| `Diversity_` | Diversity_Index_2023 | Diversity index |
| `Male_Pop_2` | Male_Pop_2023 | Male population |
| `Female_Pop` | Female_Pop_2023 | Female population |

---

## 🔍 **WHICH FILE SHOULD I USE?**

### **Use redcross-counties.zip when:**
✅ You need full Red Cross organizational data
✅ You want complete demographic fields (82 total)
✅ You're filtering by Chapter/Region/Division
✅ File size isn't a concern (11.8 MB is fine)
✅ **This is the RECOMMENDED file for most users**

### **Use alice_counties_2023_CORRECTED.zip when:**
✅ You need complete US coverage (all 3,221 counties including territories)
✅ You want smaller file size (1.9 MB)
✅ You only need key ALICE and demographic fields
✅ Some missing Red Cross assignments are acceptable

---

## ⚠️ **IMPORTANT NOTES**

### **ZIP Codes and Places Files - NOT AVAILABLE**

**The ZIP code and Places files have been removed because they contained incorrect data.**

- 68% of ZIP codes had "Not Assigned" for Chapter/Region
- The remaining 32% had **wrong chapter assignments** (e.g., Detroit ZIP showing Texas chapter)
- The County FIPS join logic was fundamentally flawed

**These files will NOT be recreated.** If you need sub-county analysis, consider:
1. Using county-level data as the finest granularity
2. Creating custom ZIP code aggregations in ArcGIS Online after upload
3. Waiting for proper ALICE ZIP code data with correct Red Cross assignments

---

## ✅ **VERIFICATION CHECKLIST**

Before uploading to ArcGIS Online:

- [x] Files are in ZIP format containing shapefiles
- [x] File sizes are under 100 MB
- [x] Field names are 10 characters or less
- [x] CRS is EPSG:4326 (WGS84)
- [x] No null geometries
- [x] Red Cross Chapter/Region/Division fields present
- [x] ALICE vulnerability data present

---

## 📞 **QUESTIONS?**

**For detailed field mapping:** See `SHAPEFILE_FIELD_MAPPING.md` in Alice and Demographic Data folder

**For complete analysis guide:** See `ARCGIS_CHOROPLETH_COMPLETE_GUIDE.md`

**For quick start:** See `QUICK_START.md`

---

**🎉 READY TO UPLOAD AND CREATE CHOROPLETH MAPS!**

*Last verified: October 26, 2025*
