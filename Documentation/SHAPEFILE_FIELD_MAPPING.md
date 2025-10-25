# Shapefile Field Name Mapping

**Created:** October 25, 2025
**File:** alice_counties_2023_CORRECTED.zip

---

## ⚠️ SHAPEFILE LIMITATION

Shapefiles have a **10-character maximum** for field names. All longer field names were automatically truncated when converting from GeoJSON.

---

## 📋 COMPLETE FIELD NAME MAPPING

### Geographic Identifiers (No Truncation)
- `FIPS` → FIPS (5-digit county code)
- `GeoID` → GeoID
- `County` → County
- `State` → State
- `County_ST` → County_ST

### Geographic Identifiers (Truncated)
- `County_Lon` → **County_Long** (County long name)
- `County_ST_` → **County_ST_Long** (County, State long name)

### Red Cross Organization
- `RC_Chapter` → RC_Chapter
- `RC_Chapt_1` → **RC_Chapter_Code** (Chapter ECODE)
- `RC_Region` → RC_Region
- `RC_Region_` → **RC_Region_Code** (Region RCODE)
- `RC_Divisio` → **RC_Division** (Division name)
- `RC_Divis_1` → **RC_Division_Code** (Division DCODE)
- `RC_FEMA_Re` → **RC_FEMA_Region** (FEMA Region)

### Red Cross Contact
- `RC_Address` → RC_Address
- `RC_City` → RC_City
- `RC_State` → RC_State
- `RC_Zip` → RC_Zip
- `RC_Phone` → RC_Phone
- `RC_Time_Zo` → **RC_Time_Zone** (Time zone)

### Geography
- `Acres` → Acres
- `SQ_MI` → SQ_MI

### Population (2023)
- `Pop_2023` → Pop_2023
- `Pop_2028` → Pop_2028
- `Male_Pop_2` → **Male_Pop_2023** (Male population)
- `Female_Pop` → **Female_Pop_2023** (Female population)
- `HH_Pop_202` → **HH_Pop_2023** (Household population)
- `Fam_Pop_20` → **Fam_Pop_2023** (Family population)
- `Pop_Den_20` → **Pop_Den_2023** (Population density)

### Households (2023)
- `Total_HH_2` → **Total_HH_2023** (Total households from demographics)
- `Avg_HH_Siz` → **Avg_HH_Size_2023** (Average household size)
- `Avg_Fam_Si` → **Avg_Fam_Size_2023** (Average family size)
- `Total_HU_2` → **Total_HU_2023** (Total housing units)
- `Owner_2023` → Owner_2023
- `Renter_202` → **Renter_2023** (Renter-occupied)
- `Vacant_202` → **Vacant_2023** (Vacant units)

### Housing Values (2023)
- `Med_Home_V` → **Med_Home_Val_2023** (Median home value)
- `Avg_Home_V` → **Avg_Home_Val_2023** (Average home value)

### Age Demographics (2023)
- `Median_Age` → **Median_Age_2023** (Median age)
- `Youth_0_14` → **Youth_0_14_Pop_2023** (Youth 0-14)
- `Yng_Adult_` → **Yng_Adult_15_24_Pop_2023** (Young adults 15-24)
- `Adult_25_6` → **Adult_25_64_Pop_2023** (Adults 25-64)
- `Seniors_65` → **Seniors_65_up_Pop_2023** (Seniors 65+)

### Race/Ethnicity (2023)
- `Pop_White_` → **Pop_White_2023** (White population)
- `Pop_Black_` → **Pop_Black_2023** (Black population)
- `Pop_Am_Ind` → **Pop_Am_Indian_2023** (American Indian)
- `Pop_Asian_` → **Pop_Asian_2023** (Asian population)
- `Pop_Pacifi` → **Pop_Pacific_2023** (Pacific Islander)
- `Pop_Other_` → **Pop_Other_2023** (Other races)
- `Pop_2_Plus` → **Pop_2_Plus_Races_2023** (Two or more races)
- `Hisp_Pop_2` → **Hisp_Pop_2023** (Hispanic population)
- `Diversity_` → **Diversity_Index_2023** (Diversity index)

### Income (2023)
- `Med_HH_Inc` → **Med_HH_Inc_2023** (Median household income)
- `Avg_HH_Inc` → **Avg_HH_Inc_2023** (Average household income)
- `Per_Cap_In` → **Per_Cap_Inc_2023** (Per capita income)

### Employment (2023)
- `Emp_Pop_20` → **Emp_Pop_2023** (Employed population)
- `Unemp_Pop_` → **Unemp_Pop_2023** (Unemployed population)
- `Unemp_Rate` → **Unemp_Rate_2023** (Unemployment rate %)

### ALICE Data (2023)
- `ALICE_Year` → ALICE_Year
- `ALICE_Tota` → **ALICE_Total_Households** (Total households from ALICE)
- `ALICE_Pove` → **ALICE_Poverty_Households** (Households in poverty)
- `ALICE_ALIC` → **ALICE_ALICE_Households** (ALICE households)
- `ALICE_Abov` → **ALICE_Above_ALICE_Households** (Above ALICE threshold)
- `Poverty_Ra` → **Poverty_Rate_Pct** (Poverty rate %)
- `ALICE_Rate` → **ALICE_Rate_Pct** (ALICE rate %)
- `Combined_R` → **Combined_Rate_Pct** (Combined poverty + ALICE rate %)
- `ALICE_Data` → **ALICE_Data_Source** (Data source)

---

## 🎯 QUICK REFERENCE FOR COMMON FIELDS

### For Choropleths (Most Used)
- **Combined_R** = Combined_Rate_Pct (Poverty + ALICE %)
- **ALICE_Rate** = ALICE_Rate_Pct (ALICE rate %)
- **Male_Pop_2** = Male_Pop_2023
- **Female_Pop** = Female_Pop_2023
- **Med_HH_Inc** = Med_HH_Inc_2023 (Median household income)
- **Diversity_** = Diversity_Index_2023

### For Filtering
- **RC_Chapter** = RC_Chapter
- **RC_Region** = RC_Region
- **RC_Divisio** = RC_Division

---

## ✅ UPLOAD INSTRUCTIONS

**File:** `alice_counties_2023_CORRECTED.zip` (1.9 MB)

**ArcGIS Online Upload Steps:**
1. Go to **Content** → **Add Item** → **From your computer**
2. Select `alice_counties_2023_CORRECTED.zip`
3. ✅ **Check "Publish this file as a hosted layer"**
4. Set **Title:** "ALICE County Vulnerability 2023 - Complete US (Shapefile)"
5. Add **Tags:** alice, vulnerability, demographics, red-cross, counties, 2023
6. Click **Publish**
7. Wait 2-3 minutes for processing

**Why This Should Work:**
- Shapefile format (industry standard for Esri)
- Only 1.9 MB (well under limits)
- 3,221 features (published layers handle this)
- All components included in ZIP

---

## 📊 WHAT YOU GET

- **3,221 US counties** with complete coverage
- **67 data fields** (with truncated names in shapefile)
- **All ALICE vulnerability data** where available
- **Complete Red Cross demographics** for all counties
- **Ready for choropleth mapping and filtering**

---

*Note: If you need the full field names preserved, use the GeoJSON version in ArcGIS Pro desktop application, or use the file geodatabase (.gdb) format instead of shapefile.*
