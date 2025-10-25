#!/usr/bin/env python3
"""
FIXED VERSION: Create ArcGIS layers with ALL counties
- ALL 3,152 counties get full Red Cross demographics
- ALICE data added WHERE AVAILABLE (2,348 counties)
- Counties without ALICE show demographics only (with nulls for ALICE fields)
"""

import json
import csv
import urllib.request
from datetime import datetime

print("=" * 80)
print("FIXED: ALL COUNTIES WITH DEMOGRAPHICS + ALICE WHERE AVAILABLE")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Input files
rc_demographics = '/Users/jefffranzen/Desktop/Alice and Demographic Data/red-cross-counties-with-demographics.csv'
enriched_master = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_redcross_master_enriched.csv'

# Output file
output_geojson = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_counties_2023_FIXED.geojson'

print("=" * 80)
print("STEP 1: Load ALL Red Cross Demographics (3,152 counties)")
print("=" * 80)

rc_data = {}

with open(rc_demographics, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fips = row['FIPS'].strip().zfill(5)
        rc_data[fips] = row

print(f"✅ Loaded {len(rc_data)} counties with FULL demographics\n")

print("=" * 80)
print("STEP 2: Load ALICE Data (2,348 counties) - OPTIONAL")
print("=" * 80)

alice_data = {}

with open(enriched_master, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = row.get('Year', '').strip()
        geo_level = row.get('Geographic_Level', '').strip().lower()

        # Only county-level 2023 data
        if year == '2023' and geo_level == 'county':
            fips = row['GeoID'].strip()[:5].zfill(5)
            alice_data[fips] = row

print(f"✅ Loaded {len(alice_data)} counties with ALICE data (optional)\n")

print("=" * 80)
print("STEP 3: Download US County Boundaries (ALL 3,221)")
print("=" * 80)

county_boundaries_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

try:
    print(f"   Downloading from: {county_boundaries_url}")
    with urllib.request.urlopen(county_boundaries_url) as response:
        county_boundaries = json.loads(response.read().decode())
    print(f"   ✅ Downloaded {len(county_boundaries['features'])} county boundaries\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    exit(1)

print("=" * 80)
print("STEP 4: Create COMPLETE GeoJSON - ALL Counties with Demographics")
print("=" * 80)
print("   Strategy:")
print("   • ALL counties get Red Cross demographics (where available)")
print("   • ALICE data added WHERE IT EXISTS")
print("   • Counties without demographics get minimal properties\n")

counties_with_rc_data = 0
counties_with_alice_data = 0
counties_with_both = 0
counties_with_neither = 0

# Helper functions
def safe_int(value):
    try:
        return int(float(value.strip().replace(',', ''))) if value and value.strip() else None
    except:
        return None

def safe_float(value):
    try:
        return round(float(value.strip().replace(',', '')), 2) if value and value.strip() else None
    except:
        return None

def safe_str(value):
    return value.strip() if value and value.strip() else None

for feature in county_boundaries['features']:
    fips = feature['id']

    # Get Red Cross demographics (if available)
    rc = rc_data.get(fips, {})

    # Get ALICE data (if available)
    alice = alice_data.get(fips, {})

    # Build complete properties
    properties = {
        # Geographic identifiers (always present)
        'FIPS': fips,
    }

    # Add Red Cross demographics if available
    if rc:
        properties.update({
            # Geographic
            'GeoID': safe_str(rc.get('GeoID')),
            'County': safe_str(rc.get('County')),
            'County_Long': safe_str(rc.get('County_Long')),
            'County_ST': safe_str(rc.get('County_ST')),
            'County_ST_Long': safe_str(rc.get('County_ST_Long')),
            'State': safe_str(rc.get('State')),

            # Red Cross Organization
            'RC_Chapter': safe_str(rc.get('Chapter')),
            'RC_Chapter_Code': safe_str(rc.get('ECODE')),
            'RC_Region': safe_str(rc.get('Region')),
            'RC_Region_Code': safe_str(rc.get('RCODE')),
            'RC_Division': safe_str(rc.get('Division')),
            'RC_Division_Code': safe_str(rc.get('DCODE')),
            'RC_FEMA_Region': safe_str(rc.get('FEMA_Region')),

            # Contact
            'RC_Address': safe_str(rc.get('Address')),
            'RC_City': safe_str(rc.get('City')),
            'RC_State': safe_str(rc.get('State')),
            'RC_Zip': safe_str(rc.get('Zip')),
            'RC_Phone': safe_str(rc.get('Phone')),
            'RC_Time_Zone': safe_str(rc.get('Time_Zone')),

            # Geography
            'Acres': safe_int(rc.get('Acres')),
            'SQ_MI': safe_float(rc.get('SQ_MI')),

            # Population
            'Pop_2023': safe_int(rc.get('Pop_2023')),
            'Pop_2028': safe_int(rc.get('Pop_2028')),
            'Male_Pop_2023': safe_int(rc.get('Male_Pop_2023')),
            'Female_Pop_2023': safe_int(rc.get('Female_Pop_2023')),
            'HH_Pop_2023': safe_int(rc.get('HH_Pop_2023')),
            'Fam_Pop_2023': safe_int(rc.get('Fam_Pop_2023')),
            'Pop_Den_2023': safe_float(rc.get('Pop_Den_2023')),

            # Households
            'Total_HH_2023': safe_int(rc.get('Total_HH_2023')),
            'Avg_HH_Size_2023': safe_float(rc.get('Avg_HH_Size_2023')),
            'Avg_Fam_Size_2023': safe_float(rc.get('Avg_Fam_Size_2023')),
            'Total_HU_2023': safe_int(rc.get('Total_HU_2023')),
            'Owner_2023': safe_int(rc.get('Owner_2023')),
            'Renter_2023': safe_int(rc.get('Renter_2023')),
            'Vacant_2023': safe_int(rc.get('Vacant_2023')),

            # Housing Values
            'Med_Home_Val_2023': safe_int(rc.get('Med_Home_Val_2023')),
            'Avg_Home_Val_2023': safe_int(rc.get('Avg_Home_Val_2023')),

            # Age Demographics
            'Median_Age_2023': safe_float(rc.get('Median_Age_2023')),
            'Youth_0_14_Pop_2023': safe_int(rc.get('Youth_0_14_Pop_2023')),
            'Yng_Adult_15_24_Pop_2023': safe_int(rc.get('Yng_Adult_15_24_Pop_2023')),
            'Adult_25_64_Pop_2023': safe_int(rc.get('Adult_25_64_Pop_2023')),
            'Seniors_65_up_Pop_2023': safe_int(rc.get('Seniors_65_up_Pop_2023')),

            # Race/Ethnicity
            'Pop_White_2023': safe_int(rc.get('Pop_White_2023')),
            'Pop_Black_2023': safe_int(rc.get('Pop_Black_2023')),
            'Pop_Am_Indian_2023': safe_int(rc.get('Pop_Am_Indian_2023')),
            'Pop_Asian_2023': safe_int(rc.get('Pop_Asian_2023')),
            'Pop_Pacific_2023': safe_int(rc.get('Pop_Pacific_2023')),
            'Pop_Other_2023': safe_int(rc.get('Pop_Other_2023')),
            'Pop_2_Plus_Races_2023': safe_int(rc.get('Pop_2_Plus_Races_2023')),
            'Hisp_Pop_2023': safe_int(rc.get('Hisp_Pop_2023')),
            'Diversity_Index_2023': safe_float(rc.get('Diversity_Index_2023')),

            # Income
            'Med_HH_Inc_2023': safe_int(rc.get('Med_HH_Inc_2023')),
            'Avg_HH_Inc_2023': safe_int(rc.get('Avg_HH_Inc_2023')),
            'Per_Cap_Inc_2023': safe_int(rc.get('Per_Cap_Inc_2023')),

            # Employment
            'Emp_Pop_2023': safe_int(rc.get('Emp_Pop_2023')),
            'Unemp_Pop_2023': safe_int(rc.get('Unemp_Pop_2023')),
            'Unemp_Rate_2023': safe_float(rc.get('Unemp_Rate_2023'))
        })
        counties_with_rc_data += 1
    else:
        # No RC data - set demographic fields to None
        properties.update({
            'County': None,
            'State': None,
            'Pop_2023': None,
            'Male_Pop_2023': None,
            'Female_Pop_2023': None,
            'RC_Chapter': None,
            'RC_Region': None,
            'RC_Division': None
        })

    # Add ALICE data if available
    if alice:
        properties.update({
            'ALICE_Year': 2023,
            'ALICE_Total_Households': safe_int(alice.get('Total_Households')),
            'ALICE_Poverty_Households': safe_int(alice.get('Poverty_Households')),
            'ALICE_ALICE_Households': safe_int(alice.get('ALICE_Households')),
            'ALICE_Above_ALICE_Households': safe_int(alice.get('Above_ALICE_Households')),
            'Poverty_Rate_Pct': safe_float(alice.get('Poverty_Rate_Pct')),
            'ALICE_Rate_Pct': safe_float(alice.get('ALICE_Rate_Pct')),
            'Combined_Rate_Pct': safe_float(alice.get('Combined_Rate_Pct')),
            'ALICE_Data_Source': safe_str(alice.get('Data_Source'))
        })
        counties_with_alice_data += 1

        if rc:
            counties_with_both += 1
    else:
        # No ALICE data - set ALICE fields to None
        properties.update({
            'ALICE_Year': None,
            'ALICE_Total_Households': None,
            'Poverty_Rate_Pct': None,
            'ALICE_Rate_Pct': None,
            'Combined_Rate_Pct': None,
            'ALICE_Data_Source': None
        })

    if not rc and not alice:
        counties_with_neither += 1

    feature['properties'] = properties

print(f"✅ Processing complete:\n")
print(f"   Counties with Red Cross demographics: {counties_with_rc_data}")
print(f"   Counties with ALICE data: {counties_with_alice_data}")
print(f"   Counties with BOTH: {counties_with_both}")
print(f"   Counties with NEITHER: {counties_with_neither}")
print(f"   TOTAL counties in GeoJSON: {len(county_boundaries['features'])}\n")

print("💾 Saving GeoJSON...")
with open(output_geojson, 'w', encoding='utf-8') as f:
    json.dump(county_boundaries, f)

print(f"✅ Saved: {output_geojson}\n")

print("=" * 80)
print("✅ SUCCESS!")
print("=" * 80)
print(f"\n📁 FILE CREATED: alice_counties_2023_FIXED.geojson")
print(f"\n📊 WHAT YOU CAN NOW DO:")
print(f"   ✅ View Male_Pop_2023 for ALL {counties_with_rc_data} counties with RC data")
print(f"   ✅ View ALICE data for {counties_with_alice_data} counties where available")
print(f"   ✅ Filter by Chapter/Region/Division and see demographics")
print(f"   ✅ Style by ANY demographic field (population, income, age, etc.)")
print(f"   ✅ Style by ALICE rates where available (shows null for others)")
print(f"\n💡 ARCGIS STYLING TIPS:")
print(f"   • Style by Male_Pop_2023 → Shows {counties_with_rc_data} counties")
print(f"   • Style by Combined_Rate_Pct → Shows {counties_with_alice_data} counties (others gray)")
print(f"   • Use 'Show features with no value' option to display all counties")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
