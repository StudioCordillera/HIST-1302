# Window Capture Fix - Applied ✅

## Problem Summary
The window capture was including window borders and titlebar, resulting in:
- Black borders around content
- Incomplete content area capture
- Extra padding that interfered with OCR

## Solution Applied

### 1. Changed Window Capture Method
**Before (incorrect):**
- Used `GetWindowRect()` - includes borders/titlebar
- Used `GetWindowDC()` - captures entire window

**After (correct):**
- Uses `GetClientRect()` - content area only
- Uses `GetDC()` - captures client area only

### 2. Added Auto-Crop Feature
Automatically detects and removes black bars from:
- Phone status bar at top
- Any navigation bars
- Black padding areas

Uses brightness threshold analysis to find actual content boundaries.

## Files Updated

1. **kindle_capture.py**
   - Updated `capture_window()` method
   - Added `auto_crop_black_bars()` method
   - Added numpy import

2. **requirements.txt**
   - Added numpy dependency

3. **kindle_capture_cli.py**
   - No changes needed (imports from kindle_capture.py)

## Testing the Fix

### Quick Test (Recommended)
1. Make sure scrcpy is running with Kindle open
2. Double-click: `test_fixed.bat`
3. Check `test_captures/fixed_test.png`

### Manual Test
```bash
# Activate venv (if using)
venv\Scripts\activate

# Install/update numpy
pip install numpy

# Run test
python test_fixed_capture.py
```

### Expected Results ✅
The captured screenshot should:
- Show FULL content area (no window borders)
- Have NO black bars (auto-cropped)
- Be clean page content ready for OCR
- Match the visible content in the scrcpy window

## Technical Details

### Client Area Capture
```python
# Get CLIENT area (not window)
left, top, right, bottom = win32gui.GetClientRect(hwnd)
width = right - left
height = bottom - top

# Use GetDC for client area (not GetWindowDC)
hwnd_dc = win32gui.GetDC(hwnd)
```

### Auto-Crop Algorithm
```python
# Analyze pixel brightness
row_brightness = image.mean(axis=(1, 2))
col_brightness = image.mean(axis=(0, 2))

# Find content boundaries
top = first_row_above_threshold
bottom = last_row_above_threshold
left = first_col_above_threshold
right = last_col_above_threshold

# Crop to content
cropped_image = image.crop((left, top, right, bottom))
```

## Benefits

1. **Better OCR Accuracy**
   - Only processes actual text content
   - No distraction from borders/bars

2. **Consistent Results**
   - Same content area every time
   - No manual adjustment needed

3. **Automatic Handling**
   - Works with different window sizes
   - Adapts to different phone screens
   - Removes status bars automatically

## Verification

After running the test, compare:
- **Old captures** in `test_captures/` (test_page_*.png)
- **Fixed captures** in `test_captures/` (fixed_page_*.png)
- **New test** in `test_captures/` (fixed_test.png)

The new captures should show clean, full content!

---

**Status:** ✅ **FIXED AND READY TO TEST**

Run `test_fixed.bat` to verify!
