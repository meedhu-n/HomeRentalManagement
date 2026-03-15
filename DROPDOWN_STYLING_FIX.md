# Dropdown Styling Fix

## Issue

Dropdown options for "Furnishing" and "Facing" fields were not visible because:
- Options had dark background matching the page
- No contrast between options and dropdown
- CSS wasn't styling the `<option>` elements properly

## Solution Applied

Added proper CSS styling for select dropdowns and their options in `add_property.css`:

### Changes Made:

```css
/* Select dropdown styling */
select.form-control {
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,...");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 12px;
    padding-right: 2.5rem;
}

/* Dropdown options styling */
select.form-control option {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 10px;
    font-weight: 500;
}

select.form-control option:hover {
    background-color: rgba(204, 255, 0, 0.2);
}

select.form-control option:checked {
    background-color: rgba(204, 255, 0, 0.3);
    color: #CCFF00;
}
```

## What's Fixed:

✅ **Visible Options** - All dropdown options now visible
✅ **Custom Arrow** - Green arrow icon for dropdowns
✅ **Hover Effect** - Options highlight on hover
✅ **Selected State** - Selected option shows in green
✅ **Better Contrast** - Dark background with white text

## Affected Fields:

- **Furnishing** dropdown (Unfurnished, Semi-Furnished, Fully Furnished)
- **Facing** dropdown (North, South, East, West, etc.)

## Visual Improvements:

- Custom green arrow indicator
- Dark background (#1a1a1a) for options
- White text for readability
- Green highlight on hover
- Green color for selected option

---

**Status:** ✅ Fixed
**File Modified:** core/static/core/css/add_property.css
**Testing:** Verified working
