# Kindle Capture & OCR Tool - Project Overview

## What This Tool Does

Automatically captures pages from Kindle books on your Android device and converts them to formatted markdown files using OCR. Operates autonomously in the background without requiring manual interaction.

## Key Features

✓ **Full resolution** page capture via scrcpy  
✓ **Autonomous operation** - works in background  
✓ **Automatic page turning** via ADB commands  
✓ **OCR text extraction** using Tesseract  
✓ **Formatted markdown** output with page numbers  
✓ **Complete archiving** - saves screenshots, text, and metadata  

---

## Quick Start (First Time Users)

1. **Run System Test** (verifies everything is installed correctly)
   ```
   Double-click: run_test.bat
   ```

2. **If test passes**, you're ready! If not, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

3. **Capture Your First Book**
   - Open Kindle app on your Android device
   - Navigate to page 1 (or your starting page)
   - Run: `python kindle_capture.py`
   - Follow the prompts

📖 **Detailed instructions:** See [QUICKSTART.md](QUICKSTART.md)

---

## Project Structure

```
kindle-capture-tool/
│
├── 📄 kindle_capture.py          Main script (interactive)
├── 📄 kindle_capture_cli.py      CLI version (automated)
├── 📄 test_system.py             System verification
│
├── 📋 config.json                User configuration
├── 📋 requirements.txt           Python dependencies
│
├── 🪟 quick_capture.bat          Quick launch script
├── 🪟 run_test.bat               System test launcher
│
├── 📖 README.md                  Complete documentation
├── 📖 QUICKSTART.md             Fast setup guide
├── 📖 TROUBLESHOOTING.md        Problem solving
└── 📖 PROJECT_OVERVIEW.md       This file
```

---

## Documentation Guide

### For First-Time Users
1. **Start here:** [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
2. **Run test:** Double-click `run_test.bat`
3. **Start capturing:** Follow QUICKSTART instructions

### For Detailed Information
- **Full documentation:** [README.md](README.md)
- **Configuration options:** Edit [config.json](config.json)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### For Advanced Users
- **API/Programmatic use:** See examples in [kindle_capture.py](kindle_capture.py)
- **Customization:** Modify classes in main script
- **Batch processing:** See README Advanced Usage section

---

## Installation Summary

### Required Software

| Tool | Status | Installation |
|------|--------|--------------|
| **Python 3.7+** | Must install | https://python.org |
| **scrcpy** | ✓ Already installed | - |
| **ADB Platform Tools** | ✓ Already installed | - |
| **Tesseract OCR** | Must install | https://github.com/UB-Mannheim/tesseract/wiki |

### Python Packages
```bash
pip install -r requirements.txt
```

Installs:
- pywin32 (Windows API access)
- Pillow (Image processing)
- pytesseract (OCR interface)

---

## Usage Methods

### Method 1: Interactive (Easiest)
```bash
python kindle_capture.py
```
- Prompts for book title and page range
- Best for one-off captures
- User-friendly

### Method 2: Command Line (Fastest)
```bash
python kindle_capture_cli.py --book "My Book" --start 1 --end 50
```
- No prompts needed
- Perfect for automation
- Scriptable

### Method 3: Batch File (Simplest)
1. Edit `quick_capture.bat`
2. Set book title and page range
3. Double-click to run

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│ 1. Start scrcpy                                         │
│    • Connects to Android device                         │
│    • Opens full-resolution mirror window                │
└───────────────┬─────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────┐
│ 2. Capture Loop (for each page)                         │
│    ┌────────────────────────────────────────────┐      │
│    │ • Capture window screenshot                │      │
│    │ • Save as PNG (page_XXXX.png)             │      │
│    └───────────┬────────────────────────────────┘      │
│                │                                         │
│    ┌───────────▼────────────────────────────────┐      │
│    │ • Run OCR on screenshot                    │      │
│    │ • Extract text                             │      │
│    │ • Save raw text (page_XXXX.txt)           │      │
│    └───────────┬────────────────────────────────┘      │
│                │                                         │
│    ┌───────────▼────────────────────────────────┐      │
│    │ • Send ADB command to turn page            │      │
│    │ • Wait for page to load                    │      │
│    └────────────────────────────────────────────┘      │
│                                                          │
│    (Repeat until last page)                             │
└───────────────┬─────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────┐
│ 3. Generate Output                                      │
│    • Create markdown file with formatted text           │
│    • Include page numbers and metadata                  │
│    • Save JSON metadata file                            │
└─────────────────────────────────────────────────────────┘
```

---

## Output Files

After capture completes, check `kindle_captures/` folder:

### Main Output
- **`BookTitle_1-50_timestamp.md`** - Your formatted book text (THIS IS WHAT YOU WANT)
- **`BookTitle_1-50_timestamp.json`** - Metadata (page numbers, timestamps, etc.)

### Supporting Files
- **`screenshots/page_XXXX.png`** - High-quality page images
- **`text_data/page_XXXX.txt`** - Raw OCR output per page

---

## Configuration Overview

Edit `config.json` to customize:

### Paths (UPDATE THESE FIRST)
```json
"paths": {
  "platform_tools": "C:\\Users\\...\\platform-tools",
  "tesseract": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
  "output_folder": "kindle_captures"
}
```

### Capture Settings (TUNE FOR YOUR DEVICE)
```json
"capture": {
  "page_turn_delay": 2.5,        // Increase if pages load slowly
  "page_turn_method": "swipe"    // or "tap"
}
```

### Quality Settings
```json
"scrcpy": {
  "max_size": 1920,              // Higher = better OCR, slower
  "bitrate": "8M"                // Higher = better quality
}
```

---

## Typical Workflow

### First Time Setup (10 minutes)
1. Install Tesseract OCR
2. Install Python packages: `pip install -r requirements.txt`
3. Run system test: `run_test.bat`
4. Fix any issues (see TROUBLESHOOTING.md)

### Per-Book Capture (varies)
1. Open Kindle app on Android to starting page
2. Run capture script
3. Wait for completion (automatic)
4. Check output in `kindle_captures/` folder

**Time estimate:** ~3-5 seconds per page (depends on device, resolution, OCR speed)
- 50 pages = ~3-5 minutes
- 100 pages = ~6-10 minutes

---

## Common Adjustments

### If pages turn too fast/slow
Edit `config.json`:
```json
"capture": {
  "page_turn_delay": 3.5  // Increase this number
}
```

### If OCR quality is poor
1. Increase resolution:
   ```json
   "scrcpy": {
     "max_size": 2560
   }
   ```
2. Increase Kindle font size on device
3. Use cleaner font in Kindle app

### If page turning fails
Adjust coordinates in `config.json`:
```json
"page_turn_swipe": {
  "x1": 1000,  // Right side of screen
  "x2": 100,   // Left side of screen
  "y1": 600,   // Middle of screen
  "y2": 600    // Same Y for horizontal swipe
}
```

---

## Safety & Legal Notes

⚠️ **Important:**
- This tool is for **personal backup and accessibility** purposes only
- Requires you to **legally own** the books you capture
- Respects **Kindle Terms of Service** - operates like manual screenshots
- All processing is **local** - no data sent to external servers
- Generated files are for **your personal use only**

---

## Support & Help

### Something Not Working?

1. **Run system test first:**
   ```bash
   python test_system.py
   ```

2. **Check troubleshooting guide:**
   See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues

3. **Test with small range:**
   Try capturing just 2-3 pages first to verify setup

4. **Enable verbose mode:**
   ```bash
   python kindle_capture_cli.py --book "Test" --start 1 --end 2 --verbose
   ```

### Can't Find the Answer?

- Check all documentation files
- Verify configuration in `config.json`
- Test each component individually (ADB, scrcpy, Tesseract)
- Review error messages carefully

---

## Performance Tips

🚀 **Speed up captures:**
- Reduce `max_size` to 1280 or 1600
- Reduce `page_turn_delay` to 2.0 or 1.5
- Disable image preprocessing in OCR

🎯 **Improve quality:**
- Increase `max_size` to 2560
- Use cleaner fonts in Kindle
- Increase Kindle font size
- Ensure good device screen brightness

---

## Advanced Features

### Batch Processing Multiple Books
Create a script:
```batch
python kindle_capture_cli.py --book "Book 1" --start 1 --end 100 --no-confirm
python kindle_capture_cli.py --book "Book 2" --start 1 --end 150 --no-confirm
```

### Custom Output Location
```bash
python kindle_capture_cli.py --book "My Book" --start 1 --end 50 --output "D:\Books"
```

### Different Languages
Install language pack, then:
```json
"ocr": {
  "language": "fra"  // French, German (deu), Spanish (spa), etc.
}
```

---

## Version Information

**Version:** 1.0  
**Date:** 2025  
**Compatibility:**
- Windows 10/11
- Python 3.7+
- Android 5.0+
- Kindle app (any version)

---

## Quick Command Reference

```bash
# System test
python test_system.py

# Interactive capture
python kindle_capture.py

# CLI capture
python kindle_capture_cli.py --book "Title" --start 1 --end 50

# CLI with options
python kindle_capture_cli.py --book "Title" --start 1 --end 50 \
  --delay 3.0 --output "D:\Books" --no-confirm

# Test individual components
adb devices                    # Check device
scrcpy --max-size 1920         # Test scrcpy
tesseract --version            # Check Tesseract
```

---

## Files You Can Safely Edit

- ✅ `config.json` - Edit freely (your settings)
- ✅ `quick_capture.bat` - Edit for custom quick launches
- ⚠️ `kindle_capture.py` - Advanced users only
- ⚠️ `kindle_capture_cli.py` - Advanced users only
- ❌ Other Python files - Don't edit unless you know what you're doing

---

## Getting Started Checklist

- [ ] Install Tesseract OCR
- [ ] Install Python packages (`pip install -r requirements.txt`)
- [ ] Update `config.json` with your paths
- [ ] Run `run_test.bat` to verify setup
- [ ] Connect Android device and enable USB debugging
- [ ] Run a test capture with 2-3 pages
- [ ] Adjust timing if needed
- [ ] Start capturing your books!

---

**Ready to start?** → See [QUICKSTART.md](QUICKSTART.md)

**Need help?** → See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Want details?** → See [README.md](README.md)
