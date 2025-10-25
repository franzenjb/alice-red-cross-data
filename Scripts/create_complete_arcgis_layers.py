#!/usr/bin/env python3
"""
Create COMPLETE ArcGIS layers with ALL demographics and ALICE data
Generates separate layers for Counties, ZIP codes, and Places
Includes ALL 58 demographic fields from Red Cross data
"""

import json
import csv
import urllib.request
from datetime import datetime
from collections import defaultdict

print("=" * 80)
print("CREATE COMPLETE ARCGIS LAYERS - ALL DEMOGRAPHICS + ALICE DATA")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Input files
enriched_master = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_redcross_master_enriched.csv'
rc_demographics = '/Users/jefffranzen/Desktop/Alice and Demographic Data/red-cross-counties-with-demographics.csv'

# Output files
output_counties_geojson = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_counties_2023_COMPLETE.geojson'
output_zipcodes_csv = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_zipcodes_2023_COMPLETE.csv'
output_places_csv = '/Users/jefffranzen/Desktop/Alice and Demographic Data/alice_places_2023_COMPLETE.csv'

print("=" * 80)
print("STEP 1: Load COMPLETE Red Cross Demographics (ALL 58 fields)")
print("=" * 80)

# Load full Red Cross demographics
rc_demographics_full = {}

with open(rc_demographics, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fips = row['FIPS'].strip().zfill(5)
        rc_demographics_full[fips] = row

print(f"✅ Loaded {len(rc_demographics_full)} counties with FULL demographics (58 fields)\n")

print("=" * 80)
print("STEP 2: Load and Separate ALICE Data by Geographic Level")
print("=" * 80)

county_data = {}
zipcode_data = []
place_data = []

with open(enriched_master, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        year = row.get('Year', '').strip()
        geo_level = row.get('Geographic_Level', '').strip().lower()

        # Only process 2023 data
        if year != '2023':
            continue

        if geo_level == 'county':
            fips = row['GeoID'].strip()[:5].zfill(5)
            county_data[fips] = row
        elif 'zip' in geo_level or 'zcta' in geo_level:
            zipcode_data.append(row)
        elif 'place' in geo_level or 'city' in geo_level or 'town' in geo_level:
            place_data.append(row)
        elif 'subcounty' in geo_level:
            # Also include subcounty with ZIP codes
            zipcode_data.append(row)

print(f"✅ County-level records (2023): {len(county_data)}")
print(f"✅ ZIP/Subcounty records (2023): {len(zipcode_data)}")
print(f"✅ Place records (2023): {len(place_data)}\n")

print("=" * 80)
print("STEP 3: Download US County Boundaries")
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
print("STEP 4: Create COMPLETE County GeoJSON (ALICE + ALL Demographics)")
print("=" * 80)

matched = 0
unmatched = 0

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

    # Get ALICE data for this county
    alice = county_data.get(fips, {})

    # Get FULL demographics for this county
    demo = rc_demographics_full.get(fips, {})

    if alice and demo:
        # Create comprehensive properties with ALL data
        feature['properties'] = {
            # Geographic identifiers
            'FIPS': fips,
            'GeoID': safe_str(alice.get('GeoID')),
            'County': safe_str(demo.get('County')),
            'County_Long': safe_str(demo.get('County_Long')),
            'County_ST': safe_str(demo.get('County_ST')),
            'County_ST_Long': safe_str(demo.get('County_ST_Long')),
            'State': safe_str(alice.get('State')),
            'State_Abbr': safe_str(alice.get('State_Abbr')),

            # ALICE Data (2023)
            'Year': 2023,
            'Total_Households': safe_int(alice.get('Total_Households')),
            'Poverty_Households': safe_int(alice.get('Poverty_Households')),
            'ALICE_Households': safe_int(alice.get('ALICE_Households')),
            'Above_ALICE_Households': safe_int(alice.get('Above_ALICE_Households')),
            'Poverty_Rate_Pct': safe_float(alice.get('Poverty_Rate_Pct')),
            'ALICE_Rate_Pct': safe_float(alice.get('ALICE_Rate_Pct')),
            'Combined_Rate_Pct': safe_float(alice.get('Combined_Rate_Pct')),

            # Red Cross Organization
            'RC_Chapter': safe_str(demo.get('Chapter')),
            'RC_Chapter_Code': safe_str(demo.get('ECODE')),
            'RC_Region': safe_str(demo.get('Region')),
            'RC_Region_Code': safe_str(demo.get('RCODE')),
            'RC_Division': safe_str(demo.get('Division')),
            'RC_Division_Code': safe_str(demo.get('DCODE')),
            'RC_FEMA_Region': safe_str(demo.get('FEMA_Region')),

            # Red Cross Contact
            'RC_Address': safe_str(demo.get('Address')),
            'RC_Address_2': safe_str(demo.get('Address_2')),
            'RC_City': safe_str(demo.get('City')),
            'RC_State': safe_str(demo.get('State')),
            'RC_Zip': safe_str(demo.get('Zip')),
            'RC_Phone': safe_str(demo.get('Phone')),
            'RC_Time_Zone': safe_str(demo.get('Time_Zone')),

            # Geography
            'Acres': safe_int(demo.get('Acres')),
            'SQ_MI': safe_float(demo.get('SQ_MI')),

            # Population (2023)
            'Pop_2023': safe_int(demo.get('Pop_2023')),
            'Pop_2028': safe_int(demo.get('Pop_2028')),
            'Male_Pop_2023': safe_int(demo.get('Male_Pop_2023')),
            'Female_Pop_2023': safe_int(demo.get('Female_Pop_2023')),
            'HH_Pop_2023': safe_int(demo.get('HH_Pop_2023')),
            'Fam_Pop_2023': safe_int(demo.get('Fam_Pop_2023')),
            'Pop_Den_2023': safe_float(demo.get('Pop_Den_2023')),

            # Households (2023)
            'Demo_Total_HH_2023': safe_int(demo.get('Total_HH_2023')),  # Prefix to avoid conflict
            'Avg_HH_Size_2023': safe_float(demo.get('Avg_HH_Size_2023')),
            'Avg_Fam_Size_2023': safe_float(demo.get('Avg_Fam_Size_2023')),
            'Total_HU_2023': safe_int(demo.get('Total_HU_2023')),
            'Owner_2023': safe_int(demo.get('Owner_2023')),
            'Renter_2023': safe_int(demo.get('Renter_2023')),
            'Vacant_2023': safe_int(demo.get('Vacant_2023')),

            # Housing Values (2023)
            'Med_Home_Val_2023': safe_int(demo.get('Med_Home_Val_2023')),
            'Avg_Home_Val_2023': safe_int(demo.get('Avg_Home_Val_2023')),

            # Age Demographics (2023)
            'Median_Age_2023': safe_float(demo.get('Median_Age_2023')),
            'Youth_0_14_Pop_2023': safe_int(demo.get('Youth_0_14_Pop_2023')),
            'Yng_Adult_15_24_Pop_2023': safe_int(demo.get('Yng_Adult_15_24_Pop_2023')),
            'Adult_25_64_Pop_2023': safe_int(demo.get('Adult_25_64_Pop_2023')),
            'Seniors_65_up_Pop_2023': safe_int(demo.get('Seniors_65_up_Pop_2023')),

            # Race/Ethnicity (2023)
            'Pop_White_2023': safe_int(demo.get('Pop_White_2023')),
            'Pop_Black_2023': safe_int(demo.get('Pop_Black_2023')),
            'Pop_Am_Indian_2023': safe_int(demo.get('Pop_Am_Indian_2023')),
            'Pop_Asian_2023': safe_int(demo.get('Pop_Asian_2023')),
            'Pop_Pacific_2023': safe_int(demo.get('Pop_Pacific_2023')),
            'Pop_Other_2023': safe_int(demo.get('Pop_Other_2023')),
            'Pop_2_Plus_Races_2023': safe_int(demo.get('Pop_2_Plus_Races_2023')),
            'Hisp_Pop_2023': safe_int(demo.get('Hisp_Pop_2023')),
            'Diversity_Index_2023': safe_float(demo.get('Diversity_Index_2023')),

            # Income (2023)
            'Med_HH_Inc_2023': safe_int(demo.get('Med_HH_Inc_2023')),
            'Avg_HH_Inc_2023': safe_int(demo.get('Avg_HH_Inc_2023')),
            'Per_Cap_Inc_2023': safe_int(demo.get('Per_Cap_Inc_2023')),

            # Employment (2023)
            'Emp_Pop_2023': safe_int(demo.get('Emp_Pop_2023')),
            'Unemp_Pop_2023': safe_int(demo.get('Unemp_Pop_2023')),
            'Unemp_Rate_2023': safe_float(demo.get('Unemp_Rate_2023'))
        }
        matched += 1
    else:
        # No data - set minimal properties
        feature['properties'] = {
            'FIPS': fips,
            'Combined_Rate_Pct': None,
            'ALICE_Rate_Pct': None,
            'RC_Chapter': None
        }
        unmatched += 1

print(f"✅ Matched {matched} counties with COMPLETE data")
print(f"⚠️  {unmatched} counties without data\n")

print("💾 Saving County GeoJSON...")
with open(output_counties_geojson, 'w', encoding='utf-8') as f:
    json.dump(county_boundaries, f)
print(f"✅ Saved: {output_counties_geojson}\n")

print("=" * 80)
print("STEP 5: Create ZIP Code CSV (with inherited demographics)")
print("=" * 80)

zip_output = []

for zip_rec in zipcode_data:
    # Get parent county FIPS
    geoid = zip_rec.get('GeoID', '')
    parent_fips = geoid[:5].zfill(5) if len(geoid) >= 5 else None

    # Get parent county demographics
    demo = rc_demographics_full.get(parent_fips, {}) if parent_fips else {}

    # Merge ALICE data with inherited demographics
    complete_record = {**zip_rec}  # Start with ALICE data

    # Add demographics with prefix to avoid conflicts
    if demo:
        for key, value in demo.items():
            if key not in complete_record:
                complete_record[f'RC_{key}'] = value

    zip_output.append(complete_record)

if zip_output:
    with open(output_zipcodes_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=zip_output[0].keys())
        writer.writeheader()
        writer.writerows(zip_output)
    print(f"✅ Saved {len(zip_output)} ZIP/subcounty records: {output_zipcodes_csv}\n")
else:
    print("⚠️  No ZIP code data for 2023\n")

print("=" * 80)
print("STEP 6: Create Place CSV (with inherited demographics)")
print("=" * 80)

place_output = []

for place_rec in place_data:
    # Get parent county FIPS
    geoid = place_rec.get('GeoID', '')
    parent_fips = geoid[:5].zfill(5) if len(geoid) >= 5 else None

    # Get parent county demographics
    demo = rc_demographics_full.get(parent_fips, {}) if parent_fips else {}

    # Merge ALICE data with inherited demographics
    complete_record = {**place_rec}  # Start with ALICE data

    # Add demographics with prefix
    if demo:
        for key, value in demo.items():
            if key not in complete_record:
                complete_record[f'RC_{key}'] = value

    place_output.append(complete_record)

if place_output:
    with open(output_places_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=place_output[0].keys())
        writer.writeheader()
        writer.writerows(place_output)
    print(f"✅ Saved {len(place_output)} place records: {output_places_csv}\n")
else:
    print("⚠️  No place data for 2023\n")

print("=" * 80)
print("✅ COMPLETE!")
print("=" * 80)
print(f"\n📁 FILES CREATED:")
print(f"\n1. alice_counties_2023_COMPLETE.geojson")
print(f"   • {matched} counties with FULL data")
print(f"   • ALL 58 demographic fields included")
print(f"   • ALICE vulnerability metrics")
print(f"   • Red Cross organizational data")
print(f"   • Ready for ArcGIS choropleth maps")

if zip_output:
    print(f"\n2. alice_zipcodes_2023_COMPLETE.csv")
    print(f"   • {len(zip_output)} ZIP/subcounty records")
    print(f"   • Inherits demographics from parent county")
    print(f"   • Ready for detailed local analysis")

if place_output:
    print(f"\n3. alice_places_2023_COMPLETE.csv")
    print(f"   • {len(place_output)} city/town records")
    print(f"   • Inherits demographics from parent county")
    print(f"   • Ready for urban area analysis")

print(f"\n🎯 WHAT YOU CAN NOW DO:")
print(f"   ✅ Select county → See ALICE + ALL 58 demographics")
print(f"   ✅ Filter by Chapter → See all data")
print(f"   ✅ Filter by Region/Division → Complete view")
print(f"   ✅ Analyze ZIP codes with demographic context")
print(f"   ✅ Compare places/cities with full data")

print(f"\n📊 EXAMPLE QUERIES NOW POSSIBLE:")
print(f"   • Show counties where Median_Age > 45 AND ALICE_Rate > 30%")
print(f"   • Filter to Diversity_Index > 50 in Southeast Division")
print(f"   • Compare Med_HH_Inc vs ALICE_Rate by Region")
print(f"   • Show all ZIP codes in Chapter X with demographics")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
