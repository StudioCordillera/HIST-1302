# Kindle Capture & OCR Tool

Automated tool for capturing and extracting text from Kindle books on Android devices using scrcpy, Windows API, and OCR.

## Features

- 🖥️ **Autonomous Operation**: Runs in background without requiring user interaction
- 📱 **Full Resolution**: Captures pages at maximum quality via scrcpy
- 🔄 **Auto Page Turning**: Automatically navigates through specified page ranges
- 👁️ **OCR Processing**: Extracts text from each page using Tesseract
- 📝 **Markdown Export**: Generates formatted markdown with page numbers
- 💾 **Complete Archive**: Saves screenshots, text files, and metadata

## Prerequisites

### 1. scrcpy
Already installed globally on your system ✓

### 2. ADB Platform Tools
Already installed at: `C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools` ✓

### 3. Tesseract OCR
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

**Default installation path:** `C:\Program Files\Tesseract-OCR\tesseract.exe`

If you install to a different location, update the path in the script.

### 4. Python Packages
Install required packages:

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pywin32 Pillow pytesseract
```

## Setup

1. **Connect Your Android Device**
   ```bash
   adb devices
   ```
   Ensure your device appears in the list

2. **Enable USB Debugging** on your Android device
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"

3. **Open Kindle App** on your device and navigate to the starting page

4. **Run the Script**
   ```bash
   python kindle_capture.py
   ```

## Usage

1. Run the script:
   ```bash
   python kindle_capture.py
   ```

2. Enter the requested information:
   - **Book Title**: Name for the output files
   - **Starting Page**: First page to capture (must be currently displayed in Kindle)
   - **Ending Page**: Last page to capture

3. Confirm and wait for completion

## Output Structure

```
kindle_captures/
├── screenshots/           # PNG screenshots of each page
│   ├── page_0001.png
│   ├── page_0002.png
│   └── ...
├── text_data/            # Raw OCR text files
│   ├── page_0001.txt
│   ├── page_0002.txt
│   └── ...
└── BookTitle_1-50_20250110_143022.md    # Final markdown output
└── BookTitle_1-50_20250110_143022.json  # Metadata
```

## Configuration

Edit the `KindleCaptureConfig` class in `kindle_capture.py` to customize:

### Paths
```python
self.platform_tools_path = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools"
self.tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
self.output_folder = Path("kindle_captures")
```

### Timing
```python
self.page_turn_delay = 2.5      # Seconds to wait after turning page
self.initial_delay = 3.0        # Seconds for scrcpy to initialize
```

### scrcpy Settings
```python
self.scrcpy_max_size = 1920     # Maximum resolution
self.scrcpy_bitrate = "8M"      # Video bitrate
```

### OCR Settings
```python
self.ocr_lang = "eng"           # Language (eng, fra, deu, etc.)
```

## Page Turning Methods

The script uses swipe gestures by default. You can customize in `ADBController.turn_page_forward()`:

**Option 1: Swipe (default)**
```python
return self.swipe_screen(800, 500, 200, 500, 200)
```

**Option 2: Tap**
```python
return self.tap_screen(900, 500)
```

Adjust coordinates based on your device screen size if needed.

## Troubleshooting

### scrcpy window not found
- Increase `initial_delay` in config
- Check if scrcpy launched successfully
- Ensure no firewall is blocking scrcpy

### Page turning not working
- Adjust coordinates in `turn_page_forward()`
- Try different timing with `page_turn_delay`
- Check if Kindle app is in fullscreen mode

### OCR quality issues
- Increase `scrcpy_max_size` for better resolution
- Adjust image preprocessing in `OCRProcessor.preprocess_image()`
- Try different Tesseract PSM modes (--psm 3, 4, 6, 11, etc.)

### ADB connection issues
```bash
# Restart ADB server
adb kill-server
adb start-server

# Check devices
adb devices
```

## Advanced Usage

### Running in Background
The script minimizes the scrcpy window automatically. To completely hide it:

```python
# In ScrcpyController.find_window()
win32gui.ShowWindow(self.window_handle, win32con.SW_MINIMIZE)
```

### Batch Processing
Modify the script to accept command-line arguments:

```bash
python kindle_capture.py --book "Book Title" --start 1 --end 100
```

### Custom OCR Languages
Download additional language packs from:
https://github.com/tesseract-ocr/tessdata

Place them in: `C:\Program Files\Tesseract-OCR\tessdata\`

Then update config:
```python
self.ocr_lang = "fra"  # French
self.ocr_lang = "deu"  # German
self.ocr_lang = "spa"  # Spanish
```

## Performance Tips

1. **Close unnecessary apps** on your phone to reduce interference
2. **Disable notifications** during capture
3. **Keep phone plugged in** for long captures
4. **Use consistent lighting** (scrcpy mirrors screen exactly)
5. **Increase page_turn_delay** if pages don't load in time

## Safety Notes

- The script respects DRM and requires you to own the book
- Captures are for personal backup/accessibility purposes only
- Screenshots are local to your machine
- No network requests are made (fully offline)

## License

Personal use only. Respect copyright laws and Kindle's Terms of Service.

## Support

For issues:
1. Check Tesseract is installed correctly: `tesseract --version`
2. Verify ADB connection: `adb devices`
3. Test scrcpy manually: `scrcpy --max-size 1920`
4. Review error messages in console output
