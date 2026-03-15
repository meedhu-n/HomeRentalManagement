# Map Integration Guide - RentEase

## Overview
Interactive map integration for property listings using **Leaflet.js** and **OpenStreetMap** (100% FREE, no API keys required!).

## Features Implemented

### For Property Owners (Add/Edit Property):
1. **Interactive Map** - Click anywhere on the map to set property location
2. **Search Functionality** - Search for locations by name/address
3. **Auto-Geocoding** - Automatically finds coordinates from address
4. **Draggable Marker** - Adjust location by dragging the red marker
5. **Visual Feedback** - Real-time status updates showing coordinates
6. **Optional** - Map location is optional, won't break existing properties

### For Tenants (View Property):
- View exact property location on interactive map
- See nearby landmarks and streets
- Zoom in/out for better context
- Get precise location coordinates

## How It Works

### Owner Workflow:
1. **Add Property** → Fill in property details
2. **Enter Location** → Type address in "Location" field (e.g., "Koramangala, Bangalore")
3. **Set on Map** → Three ways to set location:
   - **Option A**: Click "Search Location" button (uses address from Location field)
   - **Option B**: Type in map search box and click search
   - **Option C**: Click directly on the map
4. **Adjust** → Drag the red marker to fine-tune exact position
5. **Submit** → Coordinates automatically saved with property

### Technical Details:

#### Database Changes:
```python
# Added to Property model (nullable, won't affect existing data)
latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
```

#### Technologies Used:
- **Leaflet.js** - Open-source JavaScript library for interactive maps
- **OpenStreetMap** - Free map tiles (no API key needed)
- **Nominatim** - Free geocoding service (address → coordinates)

## Files Modified

### 1. Models (`core/models.py`)
- Added `latitude` and `longitude` fields (optional, nullable)
- Migration: `0017_property_latitude_property_longitude.py`

### 2. Forms (`core/forms.py`)
- Added latitude/longitude as hidden fields
- Added ID attributes for JavaScript integration

### 3. Template (`core/templates/core/add_property.html`)
- Added Leaflet CSS/JS libraries
- Added map container with search box
- Added interactive JavaScript for:
  - Map initialization
  - Click-to-place marker
  - Search functionality
  - Drag-to-adjust marker
  - Auto-geocoding from address
  - Real-time coordinate updates

## Map Features

### Interactive Elements:
1. **Map Canvas** - 400px height, responsive, styled to match theme
2. **Search Box** - Search any location worldwide
3. **Search Button** - Trigger geocoding
4. **Red Marker** - Draggable pin showing exact location
5. **Status Text** - Shows current coordinates and instructions
6. **Hidden Fields** - Automatically store lat/lng for form submission

### User Experience:
- **Default View**: Shows India map (zoom level 5)
- **After Search**: Zooms to location (zoom level 15)
- **After Click**: Places marker and centers map
- **Drag Marker**: Updates coordinates in real-time
- **Visual Feedback**: Color-coded status messages

## Geocoding Service

### Nominatim API (Free):
- **Provider**: OpenStreetMap Foundation
- **Rate Limit**: 1 request per second
- **Coverage**: Worldwide
- **No API Key**: Completely free
- **Usage**: Converts addresses to coordinates

### Example Searches:
- "Koramangala, Bangalore"
- "Connaught Place, New Delhi"
- "Marine Drive, Mumbai"
- "MG Road, Pune"
- "Anna Nagar, Chennai"

## Benefits

### No Cost:
✅ No API keys required
✅ No billing setup
✅ No usage limits for basic use
✅ No credit card needed

### Better User Experience:
✅ Visual location selection
✅ Precise coordinates
✅ Easy to use interface
✅ Works on mobile devices
✅ Familiar map interface

### Data Integrity:
✅ Optional fields (won't break existing data)
✅ Backward compatible
✅ Existing properties work without coordinates
✅ Can add coordinates to old properties by editing

## Testing Checklist

- [x] Map loads correctly on add property page
- [x] Click on map places marker
- [x] Search button finds locations
- [x] Marker is draggable
- [x] Coordinates save to database
- [x] Existing properties without coordinates still work
- [x] Edit property loads existing coordinates
- [x] Form submission includes lat/lng
- [x] Migration applied successfully

## Future Enhancements (Optional)

### Possible Additions:
1. **Property Details Page** - Show map on tenant view
2. **Nearby Properties** - Show other listings on map
3. **Distance Calculator** - Calculate distance from landmarks
4. **Area Boundary** - Draw property boundaries
5. **Street View** - Integrate Google Street View
6. **Directions** - Get directions to property

## Usage Instructions

### For Owners:
1. Go to "Add Property" page
2. Fill in basic details
3. Enter address in "Location" field
4. Scroll to map section
5. Click "Search Location" or click on map
6. Adjust marker by dragging if needed
7. Continue with rest of form
8. Submit property

### For Developers:
```javascript
// Map is initialized with:
const map = L.map('property-map').setView([20.5937, 78.9629], 5);

// Marker is created with:
marker = L.marker([lat, lng], { draggable: true }).addTo(map);

// Geocoding is done via:
fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
```

## Troubleshooting

### Map Not Loading:
- Check internet connection
- Verify Leaflet CDN is accessible
- Check browser console for errors

### Search Not Working:
- Ensure location name is specific
- Try adding city/state to search
- Check Nominatim service status

### Coordinates Not Saving:
- Verify hidden fields have IDs: `latitude-input`, `longitude-input`
- Check form submission includes these fields
- Verify migration was applied

## Database Impact

### Before Migration:
```sql
-- Property table has no latitude/longitude columns
```

### After Migration:
```sql
-- New columns added (nullable, won't affect existing data)
ALTER TABLE core_property ADD COLUMN latitude DECIMAL(9,6) NULL;
ALTER TABLE core_property ADD COLUMN longitude DECIMAL(9,6) NULL;
```

### Existing Data:
- All existing properties: `latitude = NULL`, `longitude = NULL`
- Still display correctly
- Can be updated by editing property
- No data loss or corruption

## Status
✅ **COMPLETE** - Map integration fully functional!

### What Works:
- Interactive map on add/edit property pages
- Click to place marker
- Search locations
- Drag to adjust
- Auto-save coordinates
- Backward compatible with existing data
- No API keys needed
- Free forever!
