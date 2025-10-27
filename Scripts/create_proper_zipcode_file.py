#!/usr/bin/env python3
"""
Create properly functioning ZIP code file with:
1. ALICE data (where available)
2. Red Cross organizational data (Chapter, Region, Division) from parent county
3. Demographics from parent county
"""

import pandas as pd
import geopandas as gpd
import zipfile
import os
from pathlib import Path

BASE_DIR = Path('/Users/jefffranzen/Desktop/Alice and Demographic Data')
ARCGIS_DIR = BASE_DIR / 'ArcGIS Outputs'
ALICE_MAPS_DIR = Path('/Users/jefffranzen/Desktop/Alice and Demographic Data/Alice Chloropleth Maps')

print("="*80)
print("CREATE PROPER ZIP CODE FILE")
print("="*80)

# Step 1: Load Red Cross county data (has complete Chapter/Region/Division/Demographics)
print("\n1. Loading Red Cross county data with full demographics...")
redcross_counties = gpd.read_file(ALICE_MAPS_DIR / 'redcross-counties.geojson')
print(f"   ✅ Loaded {len(redcross_counties):,} counties")
print(f"   Fields: {len(redcross_counties.columns)}")

# Step 2: Load Census ZIP code boundaries
print("\n2. Loading US ZIP code boundaries...")
import urllib.request
import tempfile

url = "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip"
temp_zip = tempfile.mktemp(suffix='.zip')
urllib.request.urlretrieve(url, temp_zip)

with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
    temp_dir = tempfile.mkdtemp()
    zip_ref.extractall(temp_dir)

zip_boundaries = gpd.read_file(f'{temp_dir}/cb_2020_us_zcta520_500k.shp')
print(f"   ✅ Loaded {len(zip_boundaries):,} ZIP code boundaries")

# Step 3: Spatial join - find which county each ZIP centroid is in
print("\n3. Performing spatial join to match ZIP codes to counties...")
zip_boundaries = zip_boundaries.to_crs(redcross_counties.crs)

# Get centroids of ZIP codes for point-in-polygon test
zip_centroids = zip_boundaries.copy()
zip_centroids['geometry'] = zip_centroids.geometry.centroid

# Spatial join to find parent county
zip_with_county = gpd.sjoin(
    zip_centroids,
    redcross_counties[['FIPS', 'County', 'State', 'Chapter', 'Region', 'Division',
                       'Pop_2023', 'Med_HH_Inc_2023', 'Median_Age_2023',
                       'Unemp_Rate_2023', 'Diversity_Index_2023', 'geometry']],
    how='left',
    predicate='within'
)

print(f"   ✅ Matched {zip_with_county['FIPS'].notna().sum():,} ZIP codes to counties")

# Step 4: Load ALICE ZIP code data (where available)
print("\n4. Loading ALICE ZIP code data...")
# Check if ALICE has ZIP-level data
try:
    # The ALICE data might be at sub-county (CCD) level, not ZIP level
    # We'll create ZIP-level by inheriting county-level ALICE data
    alice_fields = [
        'FIPS',
        'ALICE_Below_ALICE_Threshold_Percentage',
        'ALICE_Poverty_Percentage',
        'ALICE_ALICE_Percentage',
        'ALICE_Households',
        'ALICE_Poverty_Households',
        'ALICE_ALICE_Households',
        'ALICE_Above_ALICE_Households'
    ]

    # Only select fields that exist
    existing_alice_fields = [f for f in alice_fields if f in redcross_counties.columns]
    alice_counties = redcross_counties[existing_alice_fields].copy()

    print(f"   ✅ Using county-level ALICE data for ZIP codes ({len(existing_alice_fields)-1} fields)")
except Exception as e:
    print(f"   ⚠️  Could not load ALICE data: {e}")
    alice_counties = None

# Step 5: Merge ZIP boundaries back with original geometry
print("\n5. Merging data with ZIP boundaries...")
zip_final = zip_boundaries.merge(
    zip_with_county[[
        'ZCTA5CE20', 'FIPS', 'County', 'State', 'Chapter', 'Region', 'Division',
        'Pop_2023', 'Med_HH_Inc_2023', 'Median_Age_2023',
        'Unemp_Rate_2023', 'Diversity_Index_2023'
    ]],
    on='ZCTA5CE20',
    how='left'
)

# Add ALICE data from parent county
if alice_counties is not None:
    zip_final = zip_final.merge(
        alice_counties,
        on='FIPS',
        how='left'
    )

# Step 6: Select essential fields
print("\n6. Selecting essential fields...")
essential_fields = [
    'ZCTA5CE20',  # ZIP code
    'County', 'State', 'FIPS',  # Geographic identifiers
    'Chapter', 'Region', 'Division',  # Red Cross org
    'Pop_2023', 'Med_HH_Inc_2023', 'Median_Age_2023',  # Demographics
    'Unemp_Rate_2023', 'Diversity_Index_2023',
    'ALICE_Below_ALICE_Threshold_Percentage',  # ALICE data
    'ALICE_Poverty_Percentage',
    'ALICE_ALICE_Percentage',
    'geometry'
]

existing_fields = [f for f in essential_fields if f in zip_final.columns]
zip_clean = zip_final[existing_fields].copy()

print(f"   ✅ Kept {len(existing_fields)} essential fields")

# Check data quality
print("\n" + "="*80)
print("DATA QUALITY CHECK")
print("="*80)

total_zips = len(zip_clean)
with_chapter = zip_clean['Chapter'].notna().sum()
with_alice = zip_clean['ALICE_Below_ALICE_Threshold_Percentage'].notna().sum()

print(f"\nTotal ZIP codes: {total_zips:,}")
print(f"With Chapter data: {with_chapter:,} ({with_chapter/total_zips*100:.1f}%)")
print(f"With ALICE data: {with_alice:,} ({with_alice/total_zips*100:.1f}%)")

# Show sample records
print("\nSample ZIP codes with data:")
sample = zip_clean[zip_clean['Chapter'].notna()].head(3)
for idx, row in sample.iterrows():
    print(f"  ZIP {row['ZCTA5CE20']}: {row['Chapter']}, {row['Region']}")

# Step 7: Save as shapefile
print("\n" + "="*80)
print("SAVING SHAPEFILE")
print("="*80)

output_shp = ARCGIS_DIR / 'alice_zipcodes_2023_PROPER.shp'
zip_clean.to_file(output_shp, driver='ESRI Shapefile')
print(f"   ✅ Saved shapefile: {output_shp.name}")

# Step 8: Compress to ZIP
print("\n8. Compressing to ZIP file...")
output_zip = ALICE_MAPS_DIR / 'alice_zipcodes_2023_PROPER.zip'

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
        file_path = output_shp.with_suffix(ext)
        if file_path.exists():
            zipf.write(file_path, f'alice_zipcodes_2023_PROPER{ext}')
            os.remove(file_path)

size_mb = output_zip.stat().st_size / (1024 * 1024)
print(f"   ✅ Compressed: {output_zip.name} ({size_mb:.1f} MB)")

print("\n" + "="*80)
print("✅ SUCCESS!")
print("="*80)
print(f"\nFile ready for ArcGIS upload:")
print(f"  {output_zip}")
print(f"\nData includes:")
print(f"  ✅ ZIP code boundaries")
print(f"  ✅ Red Cross Chapter/Region/Division (from parent county)")
print(f"  ✅ Demographics (from parent county)")
print(f"  ✅ ALICE vulnerability data (from parent county)")
print(f"\nMatch rate: {with_chapter/total_zips*100:.1f}% have Red Cross assignments")
