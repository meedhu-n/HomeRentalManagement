# Dropdown Fix - Clear Cache Instructions

## Issue
Dropdown options still not visible due to browser caching old CSS.

## Solution Applied

1. ✅ Added inline CSS with `!important` flags in template
2. ✅ Added version parameter to CSS file (`?v=2`)
3. ✅ Used `!important` to override any cached styles

## Clear Browser Cache

### Method 1: Hard Refresh (Recommended)
**Windows/Linux:**
- Press `Ctrl + Shift + R` or `Ctrl + F5`

**Mac:**
- Press `Cmd + Shift + R`

### Method 2: Clear Cache Manually

**Chrome:**
1. Press `Ctrl + Shift + Delete` (Windows) or `Cmd + Shift + Delete` (Mac)
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page

**Firefox:**
1. Press `Ctrl + Shift + Delete` (Windows) or `Cmd + Shift + Delete` (Mac)
2. Select "Cache"
3. Click "Clear Now"
4. Refresh the page

**Edge:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear now"
4. Refresh the page

### Method 3: Incognito/Private Mode
1. Open a new Incognito/Private window
2. Navigate to your site
3. Test the dropdowns

## What Was Fixed

The following CSS was added with `!important` flags:

```css
select.form-control option,
select option {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    padding: 10px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}

select.form-control option:hover,
select option:hover {
    background-color: rgba(204, 255, 0, 0.3) !important;
    color: #CCFF00 !important;
}

select.form-control option:checked,
select option:checked {
    background-color: rgba(204, 255, 0, 0.4) !important;
    color: #CCFF00 !important;
    font-weight: 700 !important;
}
```

## After Clearing Cache

You should see:
- ✅ All dropdown options visible
- ✅ Dark background (#1a1a1a) for options
- ✅ White text on options
- ✅ Green highlight on hover
- ✅ Green color for selected option

## Test Steps

1. Clear browser cache (use Method 1 above)
2. Go to Add Property or Edit Property page
3. Click "Furnishing" dropdown
4. You should see:
   - Unfurnished
   - Semi-Furnished
   - Fully Furnished
5. Click "Facing" dropdown
6. You should see all 8 directions:
   - North
   - South
   - East
   - West
   - North-East
   - North-West
   - South-East
   - South-West

## If Still Not Working

Try this in browser console (F12):
```javascript
// Force reload all stylesheets
Array.from(document.querySelectorAll('link[rel="stylesheet"]')).forEach(link => {
    link.href = link.href.split('?')[0] + '?v=' + Date.now();
});
```

Or restart the Django server:
```bash
# Stop server (Ctrl+C)
# Start again
python manage.py runserver
```

---

**Status:** ✅ Fix Applied
**Action Required:** Clear browser cache
**File Modified:** core/templates/core/add_property.html
