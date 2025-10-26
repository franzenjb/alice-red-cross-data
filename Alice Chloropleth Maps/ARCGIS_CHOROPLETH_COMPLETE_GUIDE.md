# 🗺️ COMPLETE GUIDE: ArcGIS Online Choropleth Mapping for Red Cross

## 📦 FILES CREATED (All on your Desktop)

1. **redcross-counties-arcgis.csv** - Cleaned tabular data
2. **redcross-counties.geojson** - County polygons with all data
3. **redcross-chapters.geojson** - Chapter boundary polygons
4. **redcross-regions.geojson** - Region boundary polygons
5. **redcross-divisions.geojson** - Division boundary polygons

---

## 🚀 PART 1: UPLOADING TO ARCGIS ONLINE

### Method A: Upload GeoJSON Files (RECOMMENDED - Fastest!)

1. **Login to ArcGIS Online**
   - Go to https://www.arcgis.com
   - Click "Sign In"

2. **Upload Each GeoJSON File**
   - Click "Content" → "New Item" → "Your device"
   - Drag **redcross-counties.geojson**
   - Title: "Red Cross Counties with Demographics & ALICE"
   - Tags: red cross, counties, demographics, ALICE
   - Click "Save"

3. **Repeat for Other Files:**
   - Upload **redcross-chapters.geojson** → Title: "Red Cross Chapter Boundaries"
   - Upload **redcross-regions.geojson** → Title: "Red Cross Region Boundaries"
   - Upload **redcross-divisions.geojson** → Title: "Red Cross Division Boundaries"

4. **Enable Pop-ups (Important!)**
   - Open each layer
   - Click "Visualization" → "Configure Pop-ups"
   - Configure which fields to show

---

## 🎨 PART 2: CREATING CHOROPLETHS

### County-Level Choropleth

1. **Create New Map**
   - Content → New → Map
   - Title: "Red Cross County Analysis"

2. **Add Your County Layer**
   - Click "+ Add" → "Search for layers" → "My Content"
   - Find "Red Cross Counties with Demographics & ALICE"
   - Click "Add to map"

3. **Configure Choropleth Styling**
   - Click the layer → "Styles"
   - Choose "Field to map by": Select your variable

   **KEY VARIABLES FOR CHOROPLETHS:**
   - `ALICE_Below_ALICE_Threshold_Percentage` - Financial hardship %
   - `ALICE_Poverty_Percentage` - Poverty rate
   - `ALICE_ALICE_Percentage` - ALICE households %
   - `Pop_2023` - Total population
   - `Median_Age_2023` - Median age
   - `Med_HH_Inc_2023` - Median household income
   - `Unemp_Rate_2023` - Unemployment rate

4. **Choose Classification Method**
   - **Natural Breaks** - Best for most data (groups similar values)
   - **Equal Interval** - Equal-sized ranges
   - **Quantile** - Equal number of counties in each class
   - **Standard Deviation** - Shows how far from average

   💡 **TIP:** Natural Breaks is usually best for ALICE and demographic data

5. **Pick Color Scheme**
   - **Sequential** (light → dark): Use for single variables (population, income)
   - **Diverging** (low-mid-high): Use for data with meaningful midpoint
   - **ColorBrewer** schemes are color-blind friendly

   💡 **PRO TIP:** For financial hardship, use red gradient (light red = low hardship, dark red = high hardship)

6. **Set Number of Classes**
   - **3-5 classes** - Simple, easy to understand
   - **6-7 classes** - More detail
   - **8+ classes** - Very detailed but can be confusing

   💡 **SWEET SPOT:** 5 classes for most choropleths

### Chapter/Region/Division Choropleths

**Same process as counties, but:**
- Use the dissolved boundary files (chapters.geojson, etc.)
- These have **aggregated statistics** already calculated
- Fewer features = cleaner map at broader scale

---

## 🎯 PART 3: EXPERIENCE BUILDER

### Creating an Interactive Experience

1. **Create Experience**
   - Content → New → Experience Builder → Start from scratch
   - Choose a template (Grid, Panel, Scroll)

2. **Add Map Widget**
   - Click "+" → "Map"
   - Select your choropleth map
   - Configure: Enable zoom, pan, pop-ups

3. **Add Filter Widgets (THIS IS THE MAGIC!)**

   **A) Dropdown Filter for Chapter:**
   - Add widget: "Filter" or "Dropdown"
   - Connect to: Counties layer
   - Filter field: `Chapter`
   - Label: "Select Red Cross Chapter"
   - This lets users filter to specific chapters!

   **B) Dropdown Filter for Region:**
   - Add another Filter widget
   - Filter field: `Region`
   - Label: "Select Region"

   **C) Dropdown Filter for Division:**
   - Filter field: `Division`
   - Label: "Select Division"

4. **Add Data Display Widgets**
   - **List Widget** - Show filtered counties
   - **Table Widget** - Show detailed data
   - **Chart Widget** - Bar charts, pie charts
   - **Indicator Widget** - Show summary stats

5. **Connect Widgets to Each Other**
   - Set up "Actions" → "Filter" between widgets
   - When user clicks county on map → Table updates
   - When user selects Chapter filter → Map filters

### PRO Experience Builder Tips:

💡 **Layout Strategy:**
- Left panel: Filters (Chapter, Region, Division)
- Center: Map with choropleth
- Right panel: Charts/Stats for selected area
- Bottom: Data table

💡 **Performance:**
- Use "Extent" filter to only load visible features
- Limit table rows to 50-100 for speed
- Use cached layers for fast loading

---

## 📊 PART 4: DASHBOARDS

### Creating a Dashboard

1. **Create Dashboard**
   - Content → New → Dashboard
   - Choose layout template

2. **Add Elements:**

   **MAP Element:**
   - Add Map → Select your choropleth
   - Enable "Actions" → "Filter" other elements

   **INDICATOR Elements (Top Row):**
   - Total Population (sum of Pop_2023)
   - Total Households Below ALICE (sum of Below_ALICE_Threshold_Total)
   - Average Poverty Rate (average of Poverty_Percentage)
   - Add filters to show selected area only

   **CHART Elements:**
   - **Pie Chart:** Counties by Division
   - **Bar Chart:** Top 10 counties by ALICE Percentage
   - **Serial Chart:** Population vs ALICE Households

   **LIST Element:**
   - Show counties with actions
   - Click county → Filters map

   **TABLE Element:**
   - All data fields
   - Enable sorting, search

3. **Configure Filtering/Actions:**
   - Map → Actions → "Filter" other elements
   - List → Actions → "Zoom" and "Flash" on map
   - Enable cross-filtering between all elements

### Dashboard Layout Best Practices:

💡 **Dashboard Design Patterns:**

**Option 1: Executive Summary**
```
+------------------+------------------+------------------+
|  Total Pop       |  Below ALICE %   |  Avg Income      |
+------------------+------------------+------------------+
|                                                         |
|              CHOROPLETH MAP                             |
|                                                         |
+------------------+------------------+------------------+
| Top 10 Chart     | Distribution Pie | Trend Line       |
+------------------+------------------+------------------+
```

**Option 2: Detailed Analysis**
```
+------------------+------------------------------------+
|                  |                                    |
|   FILTERS        |        CHOROPLETH MAP              |
|   - Chapter      |                                    |
|   - Region       |                                    |
|   - Division     |                                    |
|                  +------------------------------------+
|                  |                                    |
|   INDICATORS     |        DATA TABLE                  |
|   - Total        |                                    |
|   - ALICE %      |                                    |
|                  |                                    |
+------------------+------------------------------------+
```

---

## 🎨 PART 5: CHOROPLETH STYLING TIPS & TRICKS

### Color Schemes by Data Type:

**Financial Hardship Data (ALICE):**
- Use: **Red Sequential** (light → dark red)
- Why: Red = warning/concern, darker = worse
- Classes: 5 (0-10%, 10-20%, 20-30%, 30-40%, 40%+)

**Income Data:**
- Use: **Green Sequential** (dark → light green)
- Why: Green = money, darker = more
- OR: **Diverging** (red-yellow-green) around median

**Population Data:**
- Use: **Blue Sequential** (light → dark blue)
- Why: Blue is neutral, familiar from population maps
- OR: **Purple Sequential** for variety

**Age Data:**
- Use: **Orange-Brown Sequential**
- Why: Warm colors suggest age/maturity
- OR: **Diverging** around state median

**Unemployment:**
- Use: **Red Sequential** (light → dark)
- Why: Red = problem, darker = worse

### Classification Methods by Use Case:

| Data Type | Best Method | Why |
|-----------|-------------|-----|
| Financial hardship % | Natural Breaks | Groups counties with similar issues |
| Population counts | Quantile | Equal # counties per class |
| Income | Natural Breaks | Captures natural groupings |
| Rates/Percentages | Equal Interval | Easy to understand (0-20%, 20-40%, etc.) |

### Advanced Styling:

**Transparency:**
- Use 70-80% opacity for choropleths
- Allows seeing basemap beneath
- Helps with overlapping layers

**Outlines:**
- Light gray (0.5pt) for county boundaries
- White (1pt) for chapter/region/division boundaries
- Darker (2pt) for state boundaries

**Labels:**
- Show labels only at certain zoom levels
- Use "Label" expression to show key data
- Example: `$feature.County + "\n" + $feature.ALICE_Below_ALICE_Threshold_Percentage + "%"`

---

## 🔥 PART 6: ADVANCED TIPS & TRICKS

### Multi-Layer Choropleths

**Layer Stack:**
1. **Bottom:** Division boundaries (thick outlines, no fill, labels ON)
2. **Middle:** County choropleth (data fill, thin outlines)
3. **Top:** Major cities points layer (for context)

### Dynamic Choropleths (ARCADE EXPRESSIONS)

**Custom Classification in Arcade:**

```arcade
// Color counties by ALICE threshold levels
var pct = $feature.ALICE_Below_ALICE_Threshold_Percentage;

when(
  pct < 15, '#fee5d9',    // Light red - Low hardship
  pct < 25, '#fcae91',    // Medium red
  pct < 35, '#fb6a4a',    // Orange-red
  pct < 45, '#de2d26',    // Red
  pct >= 45, '#a50f15',   // Dark red - High hardship
  '#cccccc'                // Gray - No data
);
```

**Dynamic Labels:**

```arcade
// Show county name and ALICE %
$feature.County + " (" + Round($feature.ALICE_Below_ALICE_Threshold_Percentage, 1) + "%)"
```

### Performance Optimization:

💡 **For Large Datasets:**
- Publish as **Hosted Feature Layer** (not GeoJSON)
- Enable **caching** on layer
- Set **scale ranges** (don't show county details at world scale)
- Use **generalized** geometries (500k is good)

💡 **For Faster Loading:**
- Limit visible fields in pop-ups (only show what's needed)
- Use **definition queries** to filter data
- Enable **clustering** for point layers

### Filtering Best Practices:

**Definition Queries:**
- Filter layer permanently: `Chapter = 'DFW East'`
- Show only counties with high ALICE: `ALICE_Below_ALICE_Threshold_Percentage > 30`

**Filter Widget Logic:**
- Use `OR` logic for multiple selections
- Enable "Select All" / "Clear All" buttons
- Show count of filtered features

---

## 📋 PART 7: RECOMMENDED WORKFLOWS

### Workflow 1: Simple County Explorer

**Goal:** Let users explore counties by Red Cross organization

**Steps:**
1. Create map with county choropleth (ALICE %)
2. Add Experience Builder with:
   - Chapter dropdown filter
   - Region dropdown filter
   - Map (connected to filters)
   - Table showing filtered counties

**Time:** 30 minutes

### Workflow 2: Executive Dashboard

**Goal:** High-level overview for leadership

**Steps:**
1. Create dashboard with:
   - 4 indicator widgets (Total Pop, Total ALICE HH, Avg ALICE %, # Counties)
   - Choropleth map (Division level)
   - Bar chart (Top 10 chapters by ALICE %)
   - Regional comparison chart

**Time:** 1 hour

### Workflow 3: Detailed Analysis Tool

**Goal:** Deep-dive analysis for analysts

**Steps:**
1. Create Experience Builder with:
   - Left panel: All filters (Chapter, Region, Division, custom ranges)
   - Center: Map with layer switcher (Counties/Chapters/Regions/Divisions)
   - Right panel: Charts (multiple types)
   - Bottom: Full data table with export
   - Enable all cross-filtering

**Time:** 2-3 hours

---

## 🐛 TROUBLESHOOTING

### Issue: Map is blank after upload
**Fix:** Check that GeoJSON has valid CRS (should be EPSG:4326 WGS84)

### Issue: Colors don't look right
**Fix:** Go to Layer → Styles → Change Classification method

### Issue: Pop-ups show weird field names
**Fix:** Layer → Configure Pop-up → Configure Attributes → Set aliases

### Issue: Dashboard won't filter
**Fix:** Check Actions are configured: Element → Actions → Filter

### Issue: Experience Builder is slow
**Fix:** Enable caching, limit table rows, use extent filtering

### Issue: Can't see small counties
**Fix:** Add outline color, increase outline width to 1-2pt

---

## 📚 QUICK REFERENCE

### Most Useful Choropleth Variables:

| Variable | Description | Use Case |
|----------|-------------|----------|
| `ALICE_Below_ALICE_Threshold_Percentage` | % below ALICE threshold | **Primary hardship metric** |
| `ALICE_Poverty_Percentage` | % in poverty | Extreme hardship |
| `ALICE_ALICE_Percentage` | % ALICE (not poverty) | Working but struggling |
| `Med_HH_Inc_2023` | Median household income | Economic capacity |
| `Pop_2023` | Total population | Service area size |
| `Unemp_Rate_2023` | Unemployment rate | Job market health |

### Color Schemes Quick Pick:

- **Red Sequential:** ALICE %, Poverty %, Unemployment
- **Blue Sequential:** Population, Households
- **Green Sequential:** Income, Economic indicators
- **Diverging:** Age, Income (around median)

---

## ✅ CHECKLIST: Creating Your First Choropleth

- [ ] Upload GeoJSON files to ArcGIS Online
- [ ] Create new map
- [ ] Add county layer
- [ ] Configure choropleth (pick variable, method, colors)
- [ ] Save map
- [ ] Test in Experience Builder OR Dashboard
- [ ] Add filters for Chapter/Region/Division
- [ ] Configure pop-ups
- [ ] Add additional widgets (charts, tables)
- [ ] Test all interactions
- [ ] Share with team

---

## 🎓 NEXT STEPS

1. **Start Simple:** Create one county choropleth showing ALICE %
2. **Add Interactivity:** Create Experience Builder with Chapter filter
3. **Build Dashboard:** Add indicators and charts
4. **Refine:** Adjust colors, add labels, optimize performance
5. **Share:** Set sharing permissions and distribute link

**You now have everything you need to create professional Red Cross choropleths!**

Questions? Refer to this guide or ArcGIS Online documentation.

**GOOD LUCK!** 🎉
