#!/usr/bin/env python3
"""
ALICE Data Aggregation for ArcGIS/Esri Dashboards
Creates county, chapter, and region-level aggregated datasets
"""

import csv
import json
from collections import defaultdict
from datetime import datetime

print("=" * 80)
print("ALICE DATA AGGREGATION FOR ARCGIS/ESRI DASHBOARDS")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Input file
input_file = '/Users/jefffranzen/Desktop/alice_redcross_master_enriched.csv'

# Output files
output_county_all_years = '/Users/jefffranzen/Desktop/alice_county_all_years.csv'
output_county_latest = '/Users/jefffranzen/Desktop/alice_county_2023.csv'
output_chapter_summary = '/Users/jefffranzen/Desktop/alice_chapter_summary.csv'
output_region_summary = '/Users/jefffranzen/Desktop/alice_region_summary.csv'
output_division_summary = '/Users/jefffranzen/Desktop/alice_division_summary.csv'
output_statistics = '/Users/jefffranzen/Desktop/alice_aggregation_statistics.json'

print("📂 Input file:")
print(f"   {input_file}\n")

print("📊 Output files to be created:")
print(f"   1. {output_county_all_years}")
print(f"   2. {output_county_latest}")
print(f"   3. {output_chapter_summary}")
print(f"   4. {output_region_summary}")
print(f"   5. {output_division_summary}")
print(f"   6. {output_statistics}\n")

# Data structures for aggregation
county_data = []  # All years, all counties
chapter_aggregates = defaultdict(lambda: defaultdict(lambda: {
    'total_households': 0,
    'poverty_households': 0,
    'alice_households': 0,
    'above_alice_households': 0,
    'county_count': 0,
    'records': []
}))

region_aggregates = defaultdict(lambda: defaultdict(lambda: {
    'total_households': 0,
    'poverty_households': 0,
    'alice_households': 0,
    'above_alice_households': 0,
    'county_count': 0,
    'chapter_count': set(),
    'records': []
}))

division_aggregates = defaultdict(lambda: defaultdict(lambda: {
    'total_households': 0,
    'poverty_households': 0,
    'alice_households': 0,
    'above_alice_households': 0,
    'county_count': 0,
    'chapter_count': set(),
    'region_count': set(),
    'records': []
}))

statistics = {
    'processing_timestamp': datetime.now().isoformat(),
    'input_file': input_file,
    'total_records_processed': 0,
    'unique_counties': set(),
    'unique_chapters': set(),
    'unique_regions': set(),
    'unique_divisions': set(),
    'years_covered': set(),
    'geographic_levels': defaultdict(int)
}

print("🔄 Reading and processing data...\n")

# Read and process the enriched data
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for idx, row in enumerate(reader, 1):
        if idx % 10000 == 0:
            print(f"   Processed {idx:,} records...")

        try:
            # Clean and extract data
            geoid = row['GeoID'].strip()
            county_fips = geoid[:5] if len(geoid) >= 5 else geoid
            year = row.get('Year', '').strip()

            # Skip rows without essential data
            if not year or not county_fips:
                continue

            # Parse numeric fields (handle empty strings)
            def parse_float(value):
                try:
                    return float(value.strip()) if value.strip() else 0.0
                except:
                    return 0.0

            def parse_int(value):
                try:
                    return int(float(value.strip())) if value.strip() else 0
                except:
                    return 0

            total_hh = parse_int(row.get('Total_Households', '0'))
            poverty_hh = parse_int(row.get('Poverty_Households', '0'))
            alice_hh = parse_int(row.get('ALICE_Households', '0'))
            above_alice_hh = parse_int(row.get('Above_ALICE_Households', '0'))

            poverty_rate = parse_float(row.get('Poverty_Rate_Pct', '0'))
            alice_rate = parse_float(row.get('ALICE_Rate_Pct', '0'))
            combined_rate = parse_float(row.get('Combined_Rate_Pct', '0'))

            # Red Cross organizational data
            chapter = row.get('RC_Chapter', 'Not Assigned').strip()
            region = row.get('RC_Region', 'Not Assigned').strip()
            division = row.get('RC_Division', 'Not Assigned').strip()

            # Only process county-level records for aggregation (avoid double-counting)
            geo_level = row.get('Geographic_Level', '').strip().lower()

            # County-level data (for choropleth maps)
            if geo_level == 'county':
                county_record = {
                    'GeoID': county_fips,
                    'Location_Name': row.get('Location_Name', '').strip(),
                    'State': row.get('State', '').strip(),
                    'State_Abbr': row.get('State_Abbr', '').strip(),
                    'County': row.get('County', '').strip(),
                    'Year': year,
                    'Total_Households': total_hh,
                    'Poverty_Households': poverty_hh,
                    'ALICE_Households': alice_hh,
                    'Above_ALICE_Households': above_alice_hh,
                    'Poverty_Rate_Pct': poverty_rate,
                    'ALICE_Rate_Pct': alice_rate,
                    'Combined_Rate_Pct': combined_rate,
                    'RC_Chapter': chapter,
                    'RC_Chapter_Code': row.get('RC_Chapter_Code', '').strip(),
                    'RC_Region': region,
                    'RC_Region_Code': row.get('RC_Region_Code', '').strip(),
                    'RC_Division': division,
                    'RC_Division_Code': row.get('RC_Division_Code', '').strip(),
                    'RC_FEMA_Region': row.get('RC_FEMA_Region', '').strip()
                }
                county_data.append(county_record)

                # Aggregate for Chapter
                chapter_key = chapter if chapter and chapter != 'Not Assigned' else 'Not Assigned'
                chapter_aggregates[chapter_key][year]['total_households'] += total_hh
                chapter_aggregates[chapter_key][year]['poverty_households'] += poverty_hh
                chapter_aggregates[chapter_key][year]['alice_households'] += alice_hh
                chapter_aggregates[chapter_key][year]['above_alice_households'] += above_alice_hh
                chapter_aggregates[chapter_key][year]['county_count'] += 1
                chapter_aggregates[chapter_key][year]['records'].append({
                    'region': region,
                    'division': division,
                    'state': row.get('State', '').strip()
                })

                # Aggregate for Region
                region_key = region if region and region != 'Not Assigned' else 'Not Assigned'
                region_aggregates[region_key][year]['total_households'] += total_hh
                region_aggregates[region_key][year]['poverty_households'] += poverty_hh
                region_aggregates[region_key][year]['alice_households'] += alice_hh
                region_aggregates[region_key][year]['above_alice_households'] += above_alice_hh
                region_aggregates[region_key][year]['county_count'] += 1
                region_aggregates[region_key][year]['chapter_count'].add(chapter_key)
                region_aggregates[region_key][year]['records'].append({
                    'division': division,
                    'state': row.get('State', '').strip()
                })

                # Aggregate for Division
                division_key = division if division and division != 'Not Assigned' else 'Not Assigned'
                division_aggregates[division_key][year]['total_households'] += total_hh
                division_aggregates[division_key][year]['poverty_households'] += poverty_hh
                division_aggregates[division_key][year]['alice_households'] += alice_hh
                division_aggregates[division_key][year]['above_alice_households'] += above_alice_hh
                division_aggregates[division_key][year]['county_count'] += 1
                division_aggregates[division_key][year]['chapter_count'].add(chapter_key)
                division_aggregates[division_key][year]['region_count'].add(region_key)

                # Statistics
                statistics['unique_counties'].add(county_fips)
                statistics['unique_chapters'].add(chapter)
                statistics['unique_regions'].add(region)
                statistics['unique_divisions'].add(division)
                statistics['years_covered'].add(year)

            statistics['geographic_levels'][geo_level] += 1
            statistics['total_records_processed'] += 1

        except Exception as e:
            print(f"   ⚠️  Error processing row {idx}: {e}")
            continue

print(f"\n✅ Processed {statistics['total_records_processed']:,} records\n")

# ============================================================================
# OUTPUT 1: County-level data (ALL YEARS) - For time-series choropleth
# ============================================================================
print("📝 Writing Output 1: County-level data (all years)...")

with open(output_county_all_years, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'GeoID', 'Location_Name', 'State', 'State_Abbr', 'County', 'Year',
        'Total_Households', 'Poverty_Households', 'ALICE_Households',
        'Above_ALICE_Households', 'Poverty_Rate_Pct', 'ALICE_Rate_Pct',
        'Combined_Rate_Pct', 'RC_Chapter', 'RC_Chapter_Code', 'RC_Region',
        'RC_Region_Code', 'RC_Division', 'RC_Division_Code', 'RC_FEMA_Region'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(county_data)

print(f"   ✅ Wrote {len(county_data):,} county records (all years)")

# ============================================================================
# OUTPUT 2: County-level data (2023 ONLY) - For static choropleth
# ============================================================================
print("📝 Writing Output 2: County-level data (2023 only)...")

county_2023 = [rec for rec in county_data if rec['Year'] == '2023']

with open(output_county_latest, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'GeoID', 'Location_Name', 'State', 'State_Abbr', 'County', 'Year',
        'Total_Households', 'Poverty_Households', 'ALICE_Households',
        'Above_ALICE_Households', 'Poverty_Rate_Pct', 'ALICE_Rate_Pct',
        'Combined_Rate_Pct', 'RC_Chapter', 'RC_Chapter_Code', 'RC_Region',
        'RC_Region_Code', 'RC_Division', 'RC_Division_Code', 'RC_FEMA_Region'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(county_2023)

print(f"   ✅ Wrote {len(county_2023):,} county records (2023 only)")

# ============================================================================
# OUTPUT 3: Chapter-level aggregated summary
# ============================================================================
print("📝 Writing Output 3: Chapter-level summary...")

chapter_summary = []

for chapter, years_data in chapter_aggregates.items():
    for year, data in years_data.items():
        # Calculate weighted average rates
        total_hh = data['total_households']
        if total_hh > 0:
            poverty_rate = (data['poverty_households'] / total_hh) * 100
            alice_rate = (data['alice_households'] / total_hh) * 100
            combined_rate = ((data['poverty_households'] + data['alice_households']) / total_hh) * 100
        else:
            poverty_rate = alice_rate = combined_rate = 0.0

        # Get region and division from first record
        region = years_data[year]['records'][0]['region'] if years_data[year]['records'] else 'Unknown'
        division = years_data[year]['records'][0]['division'] if years_data[year]['records'] else 'Unknown'

        chapter_summary.append({
            'RC_Chapter': chapter,
            'RC_Region': region,
            'RC_Division': division,
            'Year': year,
            'Total_Counties': data['county_count'],
            'Total_Households': total_hh,
            'Poverty_Households': data['poverty_households'],
            'ALICE_Households': data['alice_households'],
            'Above_ALICE_Households': data['above_alice_households'],
            'Poverty_Rate_Pct': round(poverty_rate, 2),
            'ALICE_Rate_Pct': round(alice_rate, 2),
            'Combined_Rate_Pct': round(combined_rate, 2)
        })

# Sort by chapter and year
chapter_summary.sort(key=lambda x: (x['RC_Chapter'], x['Year']))

with open(output_chapter_summary, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'RC_Chapter', 'RC_Region', 'RC_Division', 'Year', 'Total_Counties',
        'Total_Households', 'Poverty_Households', 'ALICE_Households',
        'Above_ALICE_Households', 'Poverty_Rate_Pct', 'ALICE_Rate_Pct', 'Combined_Rate_Pct'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(chapter_summary)

print(f"   ✅ Wrote {len(chapter_summary):,} chapter-year combinations")

# ============================================================================
# OUTPUT 4: Region-level aggregated summary
# ============================================================================
print("📝 Writing Output 4: Region-level summary...")

region_summary = []

for region, years_data in region_aggregates.items():
    for year, data in years_data.items():
        # Calculate weighted average rates
        total_hh = data['total_households']
        if total_hh > 0:
            poverty_rate = (data['poverty_households'] / total_hh) * 100
            alice_rate = (data['alice_households'] / total_hh) * 100
            combined_rate = ((data['poverty_households'] + data['alice_households']) / total_hh) * 100
        else:
            poverty_rate = alice_rate = combined_rate = 0.0

        # Get division from first record
        division = years_data[year]['records'][0]['division'] if years_data[year]['records'] else 'Unknown'

        region_summary.append({
            'RC_Region': region,
            'RC_Division': division,
            'Year': year,
            'Total_Chapters': len(data['chapter_count']),
            'Total_Counties': data['county_count'],
            'Total_Households': total_hh,
            'Poverty_Households': data['poverty_households'],
            'ALICE_Households': data['alice_households'],
            'Above_ALICE_Households': data['above_alice_households'],
            'Poverty_Rate_Pct': round(poverty_rate, 2),
            'ALICE_Rate_Pct': round(alice_rate, 2),
            'Combined_Rate_Pct': round(combined_rate, 2)
        })

# Sort by region and year
region_summary.sort(key=lambda x: (x['RC_Region'], x['Year']))

with open(output_region_summary, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'RC_Region', 'RC_Division', 'Year', 'Total_Chapters', 'Total_Counties',
        'Total_Households', 'Poverty_Households', 'ALICE_Households',
        'Above_ALICE_Households', 'Poverty_Rate_Pct', 'ALICE_Rate_Pct', 'Combined_Rate_Pct'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(region_summary)

print(f"   ✅ Wrote {len(region_summary):,} region-year combinations")

# ============================================================================
# OUTPUT 5: Division-level aggregated summary
# ============================================================================
print("📝 Writing Output 5: Division-level summary...")

division_summary = []

for division, years_data in division_aggregates.items():
    for year, data in years_data.items():
        # Calculate weighted average rates
        total_hh = data['total_households']
        if total_hh > 0:
            poverty_rate = (data['poverty_households'] / total_hh) * 100
            alice_rate = (data['alice_households'] / total_hh) * 100
            combined_rate = ((data['poverty_households'] + data['alice_households']) / total_hh) * 100
        else:
            poverty_rate = alice_rate = combined_rate = 0.0

        division_summary.append({
            'RC_Division': division,
            'Year': year,
            'Total_Regions': len(data['region_count']),
            'Total_Chapters': len(data['chapter_count']),
            'Total_Counties': data['county_count'],
            'Total_Households': total_hh,
            'Poverty_Households': data['poverty_households'],
            'ALICE_Households': data['alice_households'],
            'Above_ALICE_Households': data['above_alice_households'],
            'Poverty_Rate_Pct': round(poverty_rate, 2),
            'ALICE_Rate_Pct': round(alice_rate, 2),
            'Combined_Rate_Pct': round(combined_rate, 2)
        })

# Sort by division and year
division_summary.sort(key=lambda x: (x['RC_Division'], x['Year']))

with open(output_division_summary, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'RC_Division', 'Year', 'Total_Regions', 'Total_Chapters', 'Total_Counties',
        'Total_Households', 'Poverty_Households', 'ALICE_Households',
        'Above_ALICE_Households', 'Poverty_Rate_Pct', 'ALICE_Rate_Pct', 'Combined_Rate_Pct'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(division_summary)

print(f"   ✅ Wrote {len(division_summary):,} division-year combinations")

# ============================================================================
# OUTPUT 6: Statistics and metadata
# ============================================================================
print("📝 Writing Output 6: Statistics and metadata...")

# Convert sets to lists and counts for JSON serialization
statistics['unique_counties'] = len(statistics['unique_counties'])
statistics['unique_chapters'] = len(statistics['unique_chapters'])
statistics['unique_regions'] = len(statistics['unique_regions'])
statistics['unique_divisions'] = len(statistics['unique_divisions'])
statistics['years_covered'] = sorted(list(statistics['years_covered']))
statistics['county_records_all_years'] = len(county_data)
statistics['county_records_2023'] = len(county_2023)
statistics['chapter_summary_records'] = len(chapter_summary)
statistics['region_summary_records'] = len(region_summary)
statistics['division_summary_records'] = len(division_summary)

with open(output_statistics, 'w', encoding='utf-8') as f:
    json.dump(statistics, f, indent=2)

print(f"   ✅ Wrote aggregation statistics")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ AGGREGATION COMPLETE!")
print("=" * 80)
print(f"\n📊 SUMMARY STATISTICS:")
print(f"   • Total records processed: {statistics['total_records_processed']:,}")
print(f"   • Unique counties: {statistics['unique_counties']:,}")
print(f"   • Unique chapters: {statistics['unique_chapters']:,}")
print(f"   • Unique regions: {statistics['unique_regions']:,}")
print(f"   • Unique divisions: {statistics['unique_divisions']:,}")
print(f"   • Years covered: {', '.join(statistics['years_covered'])}")
print(f"\n📁 OUTPUT FILES CREATED:")
print(f"   1. alice_county_all_years.csv - {len(county_data):,} records")
print(f"   2. alice_county_2023.csv - {len(county_2023):,} records")
print(f"   3. alice_chapter_summary.csv - {len(chapter_summary):,} records")
print(f"   4. alice_region_summary.csv - {len(region_summary):,} records")
print(f"   5. alice_division_summary.csv - {len(division_summary):,} records")
print(f"   6. alice_aggregation_statistics.json")
print(f"\n🗺️  READY FOR ARCGIS/ESRI:")
print(f"   ✓ County data ready for choropleth maps")
print(f"   ✓ Chapter data ready for chapter dashboards")
print(f"   ✓ Region data ready for regional dashboards")
print(f"   ✓ Division data ready for division dashboards")
print(f"\n💡 NEXT STEPS:")
print(f"   1. Join county CSV to county boundaries (GeoJSON/Shapefile)")
print(f"   2. Upload to ArcGIS Online as feature layers")
print(f"   3. Create dashboards with chapter/region data")
print(f"   4. Style choropleth by Combined_Rate_Pct or ALICE_Rate_Pct")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
