# 🗺️ ArcGIS/Esri ALICE Dashboard Implementation Guide

**Created:** October 25, 2025
**Purpose:** Create choropleth maps and dashboards for Red Cross ALICE vulnerability data

---

## 📦 WHAT YOU HAVE NOW

### **7 Ready-to-Use Data Files**

#### **1. Spatial Files (For Choropleth Maps)** ✅
- **`alice_counties_2023.geojson`** (3,221 US counties)
  - 2023 ALICE data joined to county boundaries
  - 2,339 counties with ALICE data
  - Properties: Combined_Rate_Pct, ALICE_Rate_Pct, Chapter, Region, Division
  - **USE FOR:** Static choropleth map showing current vulnerability

- **`alice_counties_all_years.geojson`** (2,348 counties with time series)
  - Multi-year ALICE data (2010-2023)
  - Time series arrays embedded in properties
  - **USE FOR:** Time-slider animations showing trends over 9 years

#### **2. Aggregated Data Files (For Dashboards)**
- **`alice_county_all_years.csv`** (21,127 records)
  - County-level data for all years
  - One row per county per year

- **`alice_county_2023.csv`** (2,348 records)
  - County-level data for 2023 only

- **`alice_chapter_summary.csv`** (1,532 records)
  - Chapter totals by year
  - Total households, ALICE rates per chapter

- **`alice_region_summary.csv`** (353 records)
  - Region totals by year
  - Includes chapter counts, household totals

- **`alice_division_summary.csv`** (58 records)
  - Division-level rollups by year

---

## 🎯 THREE DASHBOARD APPROACHES

### **APPROACH 1: ArcGIS Online Web Dashboard** (Recommended for non-technical users)

#### Step 1: Upload Data
1. Go to **ArcGIS Online** (arcgis.com)
2. Sign in with Red Cross account
3. Click **Content** → **Add Item** → **From your computer**
4. Upload `alice_counties_2023.geojson`
5. Publish as **Hosted Feature Layer**

#### Step 2: Create Web Map
1. Go to **Map Viewer**
2. Add your feature layer
3. Style → **Graduated Colors**
   - Field: `Combined_Rate_Pct`
   - Method: Natural Breaks (Jenks)
   - Classes: 5
   - Colors: Green → Yellow → Red

#### Step 3: Configure Popups
```
Title: {Location_Name}, {State}
Content:
  ALICE + Poverty Rate: {Combined_Rate_Pct}%
  ALICE Only: {ALICE_Rate_Pct}%
  Total Households: {Total_Households}

  Red Cross Chapter: {RC_Chapter}
  Region: {RC_Region}
  Division: {RC_Division}
```

#### Step 4: Create Dashboard
1. Click **Create App** → **Dashboards**
2. Add widgets:
   - **Map**: Your choropleth
   - **Indicator**: Total counties, average ALICE rate
   - **Bar Chart**: Top 10 chapters by ALICE rate (from chapter CSV)
   - **Category Selector**: Filter by Division/Region
   - **Serial Chart**: Trend over time

---

### **APPROACH 2: ArcGIS Experience Builder** (More flexible, modern)

#### Advantages:
- More design freedom
- Better mobile responsiveness
- Easier to create multi-page apps

#### Setup:
1. Upload all CSV files as **Tables** (not feature layers)
2. Upload GeoJSON as **Feature Layer**
3. Create **Experience Builder** app
4. Add pages:
   - Page 1: County Choropleth Map
   - Page 2: Chapter Dashboard
   - Page 3: Regional Analysis

#### Widgets to Use:
- **Map**: County choropleth
- **List**: Chapter summary with filter
- **Chart**: Bar/line charts from aggregated data
- **Filter**: Division → Region → Chapter hierarchy

---

### **APPROACH 3: Custom JavaScript App** (Maximum control)

#### For developers who want full customization:

```javascript
// Load GeoJSON
const geojsonLayer = new GeoJSONLayer({
  url: "alice_counties_2023.geojson",
  renderer: {
    type: "class-breaks",
    field: "Combined_Rate_Pct",
    classBreakInfos: [
      { minValue: 0, maxValue: 25, symbol: { color: "#2ECC71" }, label: "Low (0-25%)" },
      { minValue: 25, maxValue: 50, symbol: { color: "#F39C12" }, label: "Medium (25-50%)" },
      { minValue: 50, maxValue: 75, symbol: { color: "#E74C3C" }, label: "High (50-75%)" },
      { minValue: 75, maxValue: 100, symbol: { color: "#ED1B2E" }, label: "Very High (75-100%)" }
    ]
  }
});
```

---

## 🎨 CHOROPLETH MAP STYLING

### **Recommended Color Schemes**

#### **Option 1: Red Cross Brand (Red = High Vulnerability)**
```
Low (0-25%):      #2ECC71 (Green)
Medium (25-50%):  #F39C12 (Orange)
High (50-75%):    #E74C3C (Red)
Very High (75%+): #ED1B2E (Red Cross Red)
```

#### **Option 2: Heat Map**
```
ColorBrewer YlOrRd (Yellow-Orange-Red)
Low:  #FFFFB2
      #FED976
      #FEB24C
      #FD8D3C
      #FC4E2A
High: #E31A1C
```

#### **Option 3: Accessibility-Friendly**
```
Use ColorBrewer schemes marked "colorblind safe"
Or ArcGIS built-in "Condition Number" scheme
```

### **Classification Methods**

| Method | When to Use | Result |
|--------|-------------|--------|
| **Natural Breaks (Jenks)** | Default - finds natural groupings | Recommended ✓ |
| **Quantile** | Equal number of counties per class | Good for comparison |
| **Equal Interval** | Even spacing of values | Good if data is evenly distributed |
| **Standard Deviation** | Show deviation from mean | Advanced analysis |

---

## 📊 DASHBOARD WIDGET RECOMMENDATIONS

### **Widget 1: County Choropleth Map**
- **Data Source:** `alice_counties_2023.geojson`
- **Style:** Graduated colors by `Combined_Rate_Pct`
- **Interactions:** Click to filter other widgets
- **Popup:** County details + Chapter info

### **Widget 2: Key Metrics Cards**
- **Total Counties with Data:** 2,348
- **Average ALICE Rate:** Calculate from data
- **Chapters Covered:** 171
- **Highest Vulnerability County:** MAX(Combined_Rate_Pct)

### **Widget 3: Top Chapters Bar Chart**
- **Data Source:** `alice_chapter_summary.csv` (filtered to 2023)
- **X-axis:** RC_Chapter
- **Y-axis:** Combined_Rate_Pct
- **Sort:** Descending by rate
- **Show:** Top 15

### **Widget 4: Regional Comparison**
- **Data Source:** `alice_region_summary.csv` (filtered to 2023)
- **Chart Type:** Bar or Column
- **Group By:** RC_Region
- **Color By:** RC_Division

### **Widget 5: Time Series Trend**
- **Data Source:** `alice_county_all_years.csv` OR chapter_summary
- **Chart Type:** Line chart
- **X-axis:** Year (2010-2023)
- **Y-axis:** Combined_Rate_Pct (average)
- **Series:** By Division or Region

### **Widget 6: Filter Panel**
```
Filters:
  ☐ Division (dropdown)
  ☐ Region (dropdown)
  ☐ Chapter (dropdown)
  ☐ State (dropdown)
  ☐ Year (slider: 2010-2023)
```

### **Widget 7: Data Table**
- **Data Source:** `alice_chapter_summary.csv`
- **Columns:** Chapter, Region, Total_Households, Combined_Rate_Pct
- **Features:** Sort, search, export to CSV
- **Action:** Click row to zoom map to chapter counties

---

## 🚀 QUICK START: 15-MINUTE DASHBOARD

### **Minimal Viable Dashboard:**

1. **Upload** `alice_counties_2023.geojson` to ArcGIS Online
2. **Create Web Map** with graduated colors
3. **Save Map**
4. **Create Dashboard** from template
5. **Add Map widget**
6. **Add 2-3 Indicator widgets** (total counties, avg rate, etc.)
7. **Publish** and share

**Time:** 15 minutes
**Result:** Working choropleth map with basic metrics

---

## 📈 ADVANCED FEATURES

### **Feature 1: Time Slider**

Using `alice_counties_all_years.geojson`:
1. Enable time in layer properties
2. Parse time series from `Time_Series_Years` field
3. Add time slider widget to dashboard
4. Animate through 2010-2023

### **Feature 2: Chapter Territory Visualization**

Create a separate layer showing Chapter boundaries:
1. Dissolve counties by `RC_Chapter` field
2. Style with outline only (no fill)
3. Label with Chapter name
4. Overlay on choropleth

### **Feature 3: Comparison Mode**

Allow users to compare:
- County vs County
- Chapter vs Chapter
- Region vs Region
- Year vs Year

Use side-by-side maps or before/after slider.

### **Feature 4: Export Reports**

Add "Generate Report" button that creates:
- PDF with maps and charts
- PowerPoint with dashboard screenshots
- Excel with filtered data tables

---

## 📋 FIELD DEFINITIONS

### **County GeoJSON Properties**

| Field | Type | Description | Use For |
|-------|------|-------------|---------|
| `FIPS` | String | 5-digit county FIPS code | Joining data |
| `Location_Name` | String | "County Name, State" | Labels |
| `State_Abbr` | String | 2-letter state code | Filtering |
| `Combined_Rate_Pct` | Float | ALICE + Poverty rate (0-100) | **Choropleth** ✓ |
| `ALICE_Rate_Pct` | Float | ALICE-only rate (0-100) | Alternative viz |
| `Poverty_Rate_Pct` | Float | Poverty-only rate (0-100) | Comparison |
| `Total_Households` | Integer | Number of households | Bubble size |
| `RC_Chapter` | String | Red Cross chapter name | Filtering |
| `RC_Region` | String | Red Cross region name | Filtering |
| `RC_Division` | String | Red Cross division name | Filtering |

---

## 🎯 USE CASE EXAMPLES

### **Use Case 1: National Leadership - Strategic Planning**

**Question:** "Which regions have the highest ALICE vulnerability?"

**Dashboard:**
- Choropleth map colored by Combined_Rate_Pct
- Bar chart: Regions ranked by average ALICE rate
- Indicator: Total vulnerable households by division
- Filter: Year slider to see trends

**Insight:** Identify regions needing more resources

---

### **Use Case 2: Chapter Leaders - Service Area Analysis**

**Question:** "What is ALICE vulnerability in my chapter's counties?"

**Dashboard:**
- Map zoomed to chapter territory
- List of counties with rates
- Comparison to peer chapters in same region
- Trend chart: Has it improved or worsened?

**Insight:** Prioritize outreach to highest-need counties

---

### **Use Case 3: Partnership Team - Grant Applications**

**Question:** "What data can support our funding request?"

**Dashboard:**
- Choropleth map (export as image)
- Data table with county-level statistics (export CSV)
- Charts showing vulnerability trends
- "Generate Report" button

**Insight:** Professional data package for grant applications

---

## 💡 BEST PRACTICES

### **Data Updates**
1. Run aggregation scripts monthly/quarterly
2. Upload new CSVs to ArcGIS Online
3. Overwrite existing hosted layers
4. Dashboards automatically update

### **Performance**
- Use 2023 GeoJSON for fast loading (not all years)
- Enable caching on hosted feature layers
- Simplify geometry if file too large (use `mapshaper` tool)
- Filter data before uploading (e.g., only counties with Red Cross presence)

### **Accessibility**
- Use colorblind-safe color schemes
- Add alt text to maps
- Ensure keyboard navigation works
- Test with screen readers

### **Mobile**
- Use ArcGIS Dashboards "Mobile-optimized" template
- Stack widgets vertically on small screens
- Simplify maps (fewer labels)
- Test on actual devices

---

## 🛠️ TROUBLESHOOTING

### **Problem: GeoJSON won't upload**
**Solution:** File too large. Use `mapshaper.org` to simplify geometry or filter to fewer counties.

### **Problem: Colors look wrong**
**Solution:** Check field type. Must be numeric (not string) for graduated colors.

### **Problem: Popups show "null"**
**Solution:** 882 counties don't have ALICE data. Add conditional popup: "if Combined_Rate_Pct is null, show 'No data available'"

### **Problem: Dashboard is slow**
**Solution:**
1. Enable caching
2. Use tiled basemap (not vector)
3. Reduce number of widgets
4. Filter data to smaller extent

### **Problem: Time series not working**
**Solution:** Time data is stored as comma-separated string. You'll need to parse it in JavaScript or use separate feature layers per year.

---

## 📞 RESOURCES

### **ArcGIS Online Documentation**
- Dashboards: https://doc.arcgis.com/en/dashboards/
- Web Maps: https://doc.arcgis.com/en/arcgis-online/create-maps/
- Styling: https://doc.arcgis.com/en/arcgis-online/create-maps/apply-styles-mv.htm

### **Sample Dashboards**
- COVID-19 Dashboard: https://coronavirus-disasterresponse.hub.arcgis.com/
- FEMA Disasters: https://fema.maps.arcgis.com/apps/dashboards/

### **Tools**
- **Mapshaper** (simplify geometry): https://mapshaper.org/
- **ColorBrewer** (color schemes): https://colorbrewer2.org/
- **GeoJSON.io** (validate GeoJSON): https://geojson.io/

### **Training**
- Esri Training: https://www.esri.com/training/
- ArcGIS Dashboards Tutorial: https://learn.arcgis.com/en/projects/get-started-with-dashboards/

---

## ✅ CHECKLIST FOR DEPLOYMENT

- [ ] Upload `alice_counties_2023.geojson` to ArcGIS Online
- [ ] Publish as Hosted Feature Layer
- [ ] Upload `alice_chapter_summary.csv` as Table
- [ ] Upload `alice_region_summary.csv` as Table
- [ ] Create Web Map with styled choropleth
- [ ] Configure popups with county details
- [ ] Create Dashboard with 5-7 widgets
- [ ] Add filters (Division, Region, State)
- [ ] Test interactivity (click county → update charts)
- [ ] Set up data refresh schedule (monthly)
- [ ] Share with Red Cross organization
- [ ] Create user guide for chapter leaders
- [ ] Train regional directors on usage

---

## 🎊 WHAT YOU'VE ACCOMPLISHED

**YOU NOW HAVE:**
1. ✅ **2,348 counties** with ALICE data and spatial boundaries
2. ✅ **Ready-to-use GeoJSON files** for immediate ArcGIS deployment
3. ✅ **Chapter/Region/Division aggregations** for dashboards
4. ✅ **Time series data** (9 years: 2010-2023)
5. ✅ **Complete documentation** for implementation

**YOU CAN NOW:**
- Create professional choropleth maps showing ALICE vulnerability
- Build interactive dashboards for chapter leaders
- Generate reports for grant applications
- Track trends over time
- Compare chapters, regions, and divisions
- Deploy to web or mobile with zero coding

---

**Ready to deploy? Start with the "15-Minute Dashboard" quick start above!**

**Questions? Check the troubleshooting section or Esri documentation.**

---

*Generated: October 25, 2025*
*Part of the Red Cross Community Vulnerability Atlas project*
