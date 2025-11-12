# Quick Start Guide

## Installation (5 minutes)

### 1. Install Tesseract OCR
Download and run installer: https://github.com/UB-Mannheim/tesseract/wiki

**Use default installation path:** `C:\Program Files\Tesseract-OCR`

### 2. Install Python Packages
Open Command Prompt in the script folder and run:
```bash
pip install -r requirements.txt
```

### 3. Connect Android Device
```bash
# Check if device is connected
C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe devices
```

If your device doesn't appear, enable USB debugging:
- Settings → About Phone → Tap "Build Number" 7 times
- Settings → Developer Options → Enable "USB Debugging"

## Usage

### Method 1: Interactive (Easiest)
```bash
python kindle_capture.py
```
Follow the prompts to enter book title and page range.

### Method 2: Command Line (Fastest)
```bash
python kindle_capture_cli.py --book "Book Title" --start 1 --end 50
```

### Method 3: Batch File (No Typing)
1. Edit `quick_capture.bat`
2. Change the book title and page numbers
3. Double-click to run

## Before You Start

1. **Open Kindle app** on your Android device
2. **Navigate to the starting page** you want to capture
3. **Keep the device awake** (optional: plug into power)

## What Happens

1. Script launches scrcpy (full resolution mirror)
2. Captures screenshot of current page
3. Runs OCR to extract text
4. Turns page automatically
5. Repeats until all pages captured
6. Generates markdown file with formatted text

## Output

Check the `kindle_captures` folder:
```
kindle_captures/
├── BookTitle_1-50_timestamp.md    ← Your formatted book text
├── BookTitle_1-50_timestamp.json  ← Metadata
├── screenshots/                   ← Page images
│   ├── page_0001.png
│   ├── page_0002.png
│   └── ...
└── text_data/                     ← Raw OCR text
    ├── page_0001.txt
    ├── page_0002.txt
    └── ...
```

## Customization

Edit `config.json` to adjust:
- **page_turn_delay**: Time to wait after turning page (default: 2.5s)
- **max_size**: Screen resolution (default: 1920)
- **ocr language**: Change from "eng" to other languages

## Tips

- **First run?** Test with just 2-3 pages to verify timing
- **Pages not turning?** Increase `page_turn_delay` in config.json
- **OCR quality poor?** Check that Kindle app is in fullscreen mode
- **Device sleeping?** Enable "Stay Awake" in Developer Options

## Troubleshooting

### "Tesseract not found"
- Reinstall Tesseract to default location
- Or update path in config.json

### "scrcpy window not found"
- Increase `initial_delay` in config.json to 5.0
- Check if scrcpy launched successfully (you should see a window)

### "ADB not found"
- Script uses: `C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe`
- Update path in config.json if different

### Page turning too fast/slow
Edit `config.json`:
```json
"capture": {
  "page_turn_delay": 3.5  // Increase this number
}
```

## Advanced Features

### Different Page Turn Methods
Edit `config.json`:
```json
"capture": {
  "page_turn_method": "tap"  // or "swipe"
}
```

### Adjust Swipe/Tap Coordinates
If page turns don't work on your device screen size:
```json
"page_turn_swipe": {
  "x1": 800,  // Start X
  "y1": 500,  // Start Y
  "x2": 200,  // End X
  "y2": 500,  // End Y
  "duration": 200
}
```

### Batch Processing Script
Create a file `batch_capture.bat`:
```batch
python kindle_capture_cli.py --book "Book 1" --start 1 --end 50 --no-confirm
python kindle_capture_cli.py --book "Book 2" --start 1 --end 100 --no-confirm
python kindle_capture_cli.py --book "Book 3" --start 1 --end 75 --no-confirm
```

### Custom Output Location
```bash
python kindle_capture_cli.py --book "Book Title" --start 1 --end 50 --output "D:\MyBooks"
```

## Need Help?

1. Check the main README.md for detailed documentation
2. Run with `--verbose` flag for detailed error messages:
   ```bash
   python kindle_capture_cli.py --book "Test" --start 1 --end 5 --verbose
   ```
3. Test individual components:
   ```bash
   # Test ADB connection
   adb devices
   
   # Test scrcpy
   scrcpy --max-size 1920
   
   # Test Tesseract
   tesseract --version
   ```
