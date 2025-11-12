# Simple Batch Screen Capture Tool

**SIMPLIFIED VERSION** - Focus on reliable screen capture with page turning, no OCR complexity.

## What This Does

✅ **Captures entire screen** from scrcpy/Phone Mirror window  
✅ **Automatically turns pages** using ADB swipe commands  
✅ **Batch processing** - capture multiple pages in sequence  
✅ **Auto-crop black bars** - removes status bars and padding  
✅ **Clean PNG output** - ready for OCR processing later  

## Quick Start

1. **Test your setup first:**
   ```
   Double-click: test_simple.bat
   ```

2. **If test passes, run batch capture:**
   ```
   Double-click: run_simple_capture.bat
   ```

3. **Follow the prompts:**
   - Starting page number
   - Total pages to capture
   - Confirm and wait for completion

## Prerequisites

### Required Software
- ✅ **scrcpy** (already installed)
- ✅ **ADB** (already configured)
- ⚠️ **Python packages:** `pip install pywin32 Pillow numpy`

### Setup Steps
1. Connect Android device via USB
2. Enable USB debugging
3. Start scrcpy: `scrcpy`
4. Open Kindle app to starting page
5. Run the capture tool

## How It Works

```
1. Find scrcpy window → 2. Capture screenshot → 3. Save as PNG
                     ↑                                    ↓
6. Wait for page load ← 5. Turn page via ADB ← 4. Auto-crop bars
```

**For each page:**
1. Captures the full scrcpy window content (no borders)
2. Auto-crops black bars (status bar, navigation)
3. Saves as `page_XXXX.png` 
4. Sends ADB swipe command to turn page
5. Waits for page to load
6. Repeats for specified range

## Output

Screenshots saved to `batch_captures/`:
```
batch_captures/
├── page_0001.png
├── page_0002.png  
├── page_0003.png
└── ...
```

## Configuration

### Page Turn Speed
Edit `simple_batch_capture.py`:
```python
self.page_turn_delay = 2.5  # Increase if pages load slowly
```

### Page Turn Method
Current method: Right-to-left swipe
```python
# Swipe coordinates in turn_page() method
"800", "500",  # Start position (right side)
"200", "500",  # End position (left side)
```

Adjust coordinates based on your device screen size if needed.

## Troubleshooting

### "No window found"
- Make sure scrcpy is running
- Ensure window is visible (not minimized)
- Try: `scrcpy --window-title "Kindle"`

### "Page turn failed"
- Check ADB connection: `adb devices`
- Adjust swipe coordinates in script
- Increase page turn delay

### "Capture failed"
- Install missing packages: `pip install pywin32 Pillow numpy`
- Restart scrcpy
- Try bringing window to foreground manually

## Testing

### Quick Test (Recommended)
```bat
test_simple.bat
```

This tests all components and captures a single screenshot for verification.

### Manual Test
1. Start scrcpy with Kindle
2. Run: `python test_simple_capture.py`
3. Check output image quality

## Advanced Usage

### Command Line
```python
from simple_batch_capture import SimpleBatchCapture

capture = SimpleBatchCapture()
capture.batch_capture(start_page=1, total_pages=50)
```

### Custom Output Folder
Edit the script:
```python
self.output_folder = Path("my_book_captures")
```

### Different Page Turn Direction
For backwards/previous page, swap coordinates:
```python
"200", "500",  # Start position (left side)  
"800", "500",  # End position (right side)
```

## Next Steps

After capturing screenshots:

1. **Review captures** in `batch_captures/` folder
2. **Run OCR separately** using existing OCR tools
3. **Combine text** into final document

## Safety Notes

- ⚠️ **Personal use only** - respect copyright laws
- 📱 **Keep device plugged in** for long captures
- 🔇 **Disable notifications** to avoid interruptions
- 💡 **Use consistent lighting** for better image quality

## Files

| File | Purpose |
|------|---------|
| `simple_batch_capture.py` | Main capture script |
| `test_simple_capture.py` | Setup verification |
| `run_simple_capture.bat` | Quick launch |
| `test_simple.bat` | Quick test |
| `SIMPLE_CAPTURE_README.md` | This file |

---

**Ready to start?**
1. Run `test_simple.bat` to verify setup
2. Run `run_simple_capture.bat` to capture pages
3. Check `batch_captures/` folder for results