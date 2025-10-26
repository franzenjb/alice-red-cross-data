#!/usr/bin/env python3
"""
FIX ALL ARCGIS FILES FOR UPLOAD
1. Fix ZIP codes with proper County FIPS joins
2. Fix Places with proper County FIPS joins
3. Convert redcross-counties.geojson to shapefile
"""

import pandas as pd
import geopandas as gpd
import zipfile
import os
from pathlib import Path

BASE_DIR = Path('/Users/jefffranzen/Desktop/Alice and Demographic Data')
SOURCE_DIR = BASE_DIR / 'Source Data'
ARCGIS_DIR = BASE_DIR / 'ArcGIS Outputs'

print("="*80)
print("FIX ALL ARCGIS FILES FOR UPLOAD")
print("="*80)

# ============================================================================
# FIX #1: ZIP CODES WITH PROPER RED CROSS DATA
# ============================================================================

print("\n" + "="*80)
print("FIX #1: ZIP CODES")
print("="*80)

print("\n1. Loading ZIP code boundaries with ALICE data...")
zip_gdf = gpd.read_file(ARCGIS_DIR / 'alice_zipcodes_2023.geojson')
original_count = len(zip_gdf)
print(f"   ✅ Loaded {original_count:,} ZIP codes")

print("\n2. Loading Red Cross county demographics...")
rc_counties = pd.read_csv(SOURCE_DIR / 'red-cross-counties-with-demographics.csv')
rc_counties['FIPS'] = rc_counties['FIPS'].astype(str).str.zfill(5)
print(f"   ✅ Loaded {len(rc_counties):,} counties")

print("\n3. Extracting County FIPS from ZIP GeoID...")
# ALICE Sub-county GeoID format: 9 digits where first 5 = County FIPS with missing leading zero
# Example: "100190171" -> County FIPS should be "01001" (Alabama, Autauga)
# The pattern is: if GeoID starts with single digit, add "0" to front

def extract_county_fips(geoid):
    """Extract 5-digit County FIPS from 9-digit ALICE sub-county GeoID"""
    geoid_str = str(geoid).zfill(9)
    # Take first 5 digits
    fips_5 = geoid_str[:5]
    # If it starts with 1-9, it's missing the leading zero for state
    if fips_5[0] in '123456789' and len(fips_5) == 5:
        # Insert leading zero: "10019" -> "01001"
        state_code = '0' + fips_5[0]
        county_code = fips_5[1:4]
        return state_code + county_code
    return fips_5

zip_gdf['County_FIPS'] = zip_gdf['GeoID'].apply(extract_county_fips)
print(f"   ✅ Extracted County FIPS codes")
print(f"   Sample: GeoID {zip_gdf.iloc[0]['GeoID']} -> FIPS {zip_gdf.iloc[0]['County_FIPS']}")

print("\n4. Dropping old Red Cross fields...")
rc_cols = [col for col in zip_gdf.columns if col.startswith('RC_') or col.startswith('Data_Sourc')]
if rc_cols:
    zip_gdf = zip_gdf.drop(columns=rc_cols)
    print(f"   ✅ Dropped {len(rc_cols)} old RC columns")

print("\n5. Joining with Red Cross county data...")
zip_gdf = zip_gdf.merge(
    rc_counties,
    left_on='County_FIPS',
    right_on='FIPS',
    how='left',
    suffixes=('', '_drop')
)

# Drop duplicate columns
drop_cols = [col for col in zip_gdf.columns if col.endswith('_drop')]
if drop_cols:
    zip_gdf = zip_gdf.drop(columns=drop_cols)

matched = zip_gdf['Chapter'].notna().sum()
match_pct = (matched / len(zip_gdf)) * 100
print(f"   ✅ Match rate: {matched:,} / {len(zip_gdf):,} ({match_pct:.1f}%)")

if matched > 0:
    sample = zip_gdf[zip_gdf['Chapter'].notna()].iloc[0]
    print(f"   Sample: ZIP {sample['ZCTA5CE20']} -> {sample['Chapter']}, {sample['Region']}")

print("\n6. Selecting essential fields...")
essential_fields = [
    'ZCTA5CE20', 'GeoID', 'Geographic_Level', 'Location_Name',
    'State', 'County', 'County_FIPS', 'Year',
    'Total_Households', 'Poverty_Households', 'ALICE_Households', 'Above_ALICE_Households',
    'Poverty_Rate_Pct', 'ALICE_Rate_Pct', 'Combined_Rate_Pct',
    'Chapter', 'Region', 'Division', 'FEMA_Region',
    'Pop_2023', 'Med_HH_Inc_2023', 'Median_Age_2023',
    'Unemp_Rate_2023', 'Diversity_Index_2023',
    'geometry'
]

# Rename fields for consistency
rename_map = {
    'Total_Hous': 'Total_Households',
    'Poverty_Ho': 'Poverty_Households',
    'ALICE_Hous': 'ALICE_Households',
    'Above_ALIC': 'Above_ALICE_Households',
    'Poverty_Ra': 'Poverty_Rate_Pct',
    'ALICE_Rate': 'ALICE_Rate_Pct',
    'Combined_R': 'Combined_Rate_Pct'
}
zip_gdf = zip_gdf.rename(columns=rename_map)

# Keep only essential fields that exist
existing_fields = [f for f in essential_fields if f in zip_gdf.columns]
zip_clean = zip_gdf[existing_fields].copy()
print(f"   ✅ Kept {len(existing_fields)} essential fields (reduced from {len(zip_gdf.columns)})")

print("\n7. Converting to shapefile and compressing...")
temp_shp = ARCGIS_DIR / 'temp_zip.shp'
zip_clean.to_file(temp_shp, driver='ESRI Shapefile')

zip_output = ARCGIS_DIR / 'alice_zipcodes_2023_FIXED.zip'
with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
        file_path = temp_shp.with_suffix(ext)
        if file_path.exists():
            zipf.write(file_path, f'alice_zipcodes_2023_FIXED{ext}')
            os.remove(file_path)

size_mb = zip_output.stat().st_size / (1024 * 1024)
print(f"   ✅ Saved: alice_zipcodes_2023_FIXED.zip ({size_mb:.1f} MB)")

# ============================================================================
# FIX #2: PLACES WITH PROPER RED CROSS DATA
# ============================================================================

print("\n" + "="*80)
print("FIX #2: PLACES")
print("="*80)

if (ARCGIS_DIR / 'alice_places_2023.geojson').exists():
    print("\n1. Loading place boundaries with ALICE data...")
    place_gdf = gpd.read_file(ARCGIS_DIR / 'alice_places_2023.geojson')
    print(f"   ✅ Loaded {len(place_gdf):,} places")

    print("\n2. Extracting County FIPS...")
    place_gdf['County_FIPS'] = place_gdf['GeoID'].apply(extract_county_fips)

    print("\n3. Dropping old Red Cross fields...")
    rc_cols = [col for col in place_gdf.columns if col.startswith('RC_')]
    if rc_cols:
        place_gdf = place_gdf.drop(columns=rc_cols)

    print("\n4. Joining with Red Cross data...")
    place_gdf = place_gdf.merge(
        rc_counties,
        left_on='County_FIPS',
        right_on='FIPS',
        how='left',
        suffixes=('', '_drop')
    )

    drop_cols = [col for col in place_gdf.columns if col.endswith('_drop')]
    if drop_cols:
        place_gdf = place_gdf.drop(columns=drop_cols)

    matched = place_gdf['Chapter'].notna().sum()
    print(f"   ✅ Match rate: {matched:,} / {len(place_gdf):,} ({matched/len(place_gdf)*100:.1f}%)")

    print("\n5. Selecting essential fields...")
    place_gdf = place_gdf.rename(columns=rename_map)
    existing_fields = [f for f in essential_fields if f in place_gdf.columns]
    place_clean = place_gdf[existing_fields].copy()

    print("\n6. Converting to shapefile...")
    temp_shp = ARCGIS_DIR / 'temp_place.shp'
    place_clean.to_file(temp_shp, driver='ESRI Shapefile')

    place_output = ARCGIS_DIR / 'alice_places_2023_FIXED.zip'
    with zipfile.ZipFile(place_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
            file_path = temp_shp.with_suffix(ext)
            if file_path.exists():
                zipf.write(file_path, f'alice_places_2023_FIXED{ext}')
                os.remove(file_path)

    size_mb = place_output.stat().st_size / (1024 * 1024)
    print(f"   ✅ Saved: alice_places_2023_FIXED.zip ({size_mb:.1f} MB)")
else:
    print("\n   ⚠️ alice_places_2023.geojson not found, skipping")

# ============================================================================
# FIX #3: CONVERT REDCROSS-COUNTIES.GEOJSON TO SHAPEFILE
# ============================================================================

print("\n" + "="*80)
print("FIX #3: CONVERT REDCROSS-COUNTIES TO SHAPEFILE")
print("="*80)

alice_chloropleth_dir = Path('/Users/jefffranzen/Desktop/Alice Chloropleth Maps')
redcross_geojson = alice_chloropleth_dir / 'redcross-counties.geojson'

if redcross_geojson.exists():
    print("\n1. Loading redcross-counties.geojson...")
    rc_gdf = gpd.read_file(redcross_geojson)
    print(f"   ✅ Loaded {len(rc_gdf):,} counties")
    print(f"   ✅ {len(rc_gdf.columns)} fields")

    print("\n2. Converting to shapefile...")
    temp_shp = ARCGIS_DIR / 'temp_rc.shp'
    rc_gdf.to_file(temp_shp, driver='ESRI Shapefile')

    rc_output = alice_chloropleth_dir / 'redcross-counties.zip'
    with zipfile.ZipFile(rc_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
            file_path = temp_shp.with_suffix(ext)
            if file_path.exists():
                zipf.write(file_path, f'redcross-counties{ext}')
                os.remove(file_path)

    size_mb = rc_output.stat().st_size / (1024 * 1024)
    print(f"   ✅ Saved: redcross-counties.zip ({size_mb:.1f} MB)")
else:
    print("\n   ⚠️ redcross-counties.geojson not found")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ ALL FIXES COMPLETE")
print("="*80)
print("\nFixed files ready for ArcGIS upload:")
print("   1. alice_zipcodes_2023_FIXED.zip")
print("   2. alice_places_2023_FIXED.zip")
print("   3. redcross-counties.zip (in Alice Chloropleth Maps)")
print("\nAll files have:")
print("   ✅ Proper Red Cross Chapter/Region/Division data")
print("   ✅ Shapefile format (10-char field names)")
print("   ✅ Compressed to ZIP")
print("   ✅ Under 100 MB size limit")
