# Troubleshooting Guide

## Installation Issues

### Python Package Installation Fails

**Problem:** `pip install` gives errors

**Solutions:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages one by one
pip install pywin32
pip install Pillow
pip install pytesseract

# Use --user flag if permission denied
pip install --user pywin32 Pillow pytesseract
```

### Tesseract Not Found

**Problem:** `✗ Tesseract not found at: C:\Program Files\Tesseract-OCR\tesseract.exe`

**Solutions:**
1. **Reinstall Tesseract** from: https://github.com/UB-Mannheim/tesseract/wiki
2. **Use default install location**: `C:\Program Files\Tesseract-OCR`
3. **If installed elsewhere**, update `config.json`:
   ```json
   "paths": {
     "tesseract": "C:\\Your\\Custom\\Path\\tesseract.exe"
   }
   ```

### scrcpy Not Found

**Problem:** `'scrcpy' is not recognized as an internal or external command`

**Solutions:**
1. **Verify scrcpy is installed**: Download from https://github.com/Genymobile/scrcpy
2. **Add to PATH**:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Environment Variables → System Variables → Path → Edit
   - Add scrcpy folder (e.g., `C:\Program Files\scrcpy`)
3. **Or use full path** in script (not recommended)

---

## Connection Issues

### No ADB Devices Found

**Problem:** `adb devices` shows no devices

**Step-by-step fix:**

1. **Enable Developer Options on Android:**
   - Settings → About Phone
   - Tap "Build Number" 7 times
   - Go back → Developer Options

2. **Enable USB Debugging:**
   - Developer Options → USB Debugging → ON

3. **Check USB Connection:**
   - Use a data cable (not charge-only)
   - Try different USB ports
   - Try different cable

4. **Authorize Computer:**
   - Unlock your phone
   - Accept the "Allow USB debugging" prompt
   - Check "Always allow from this computer"

5. **Restart ADB Server:**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

### Device Shows as "Unauthorized"

**Problem:** `adb devices` shows device but says "unauthorized"

**Solution:**
1. Unlock your phone
2. Revoke USB debugging authorizations:
   - Developer Options → Revoke USB debugging authorizations
3. Disconnect and reconnect USB
4. Accept the new authorization prompt

### Device Shows as "Offline"

**Problem:** Device appears but is offline

**Solutions:**
```bash
# Restart ADB
adb kill-server
adb start-server

# Restart device in debugging mode
adb reconnect

# Reboot phone
adb reboot
```

---

## Capture Issues

### scrcpy Window Not Found

**Problem:** `✗ Failed to find scrcpy window`

**Solutions:**

1. **Increase initial delay** in `config.json`:
   ```json
   "scrcpy": {
     "initial_delay": 5.0
   }
   ```

2. **Check if scrcpy actually launched:**
   - You should see a window appear
   - If not, run manually: `scrcpy --max-size 1920`

3. **Window title mismatch:**
   - Note the actual window title
   - Update in `config.json`:
   ```json
   "scrcpy": {
     "window_title": "Actual Window Title Here"
   }
   ```

### Page Turning Not Working

**Problem:** Pages don't turn or turn to wrong page

**Solutions:**

1. **Increase page turn delay** in `config.json`:
   ```json
   "capture": {
     "page_turn_delay": 3.5
   }
   ```

2. **Adjust swipe coordinates** for your screen size:
   ```json
   "page_turn_swipe": {
     "x1": 1000,
     "y1": 600,
     "x2": 100,
     "y2": 600,
     "duration": 250
   }
   ```

   To find coordinates:
   - Run: `adb shell wm size` to get screen resolution
   - x1 should be 80-90% of width, x2 should be 10-20%
   - y1 and y2 should be 50% of height

3. **Try tap method instead**:
   ```json
   "capture": {
     "page_turn_method": "tap"
   },
   "page_turn_tap": {
     "x": 900,
     "y": 600
   }
   ```

4. **Check Kindle app settings:**
   - Disable page animations
   - Set taps to turn pages
   - Enable full screen mode

### Screenshots Are Blank

**Problem:** Screenshots captured but are blank/black

**Solutions:**

1. **Disable screen mirroring protection:**
   - Some devices block screenshots in certain apps
   - Try enabling "Force apps to be resizable" in Developer Options

2. **Check scrcpy capture method:**
   - Update scrcpy to latest version
   - Try different capture method: `scrcpy --no-display`

3. **Kindle app DRM:**
   - Some books have screenshot protection
   - Not much can be done programmatically

### Wrong Area Captured

**Problem:** Screenshot captures wrong part of screen

**Solutions:**

1. **Ensure scrcpy window is focused:**
   - Add delay before capture
   - Don't minimize the window

2. **Capture full screen instead:**
   - Modify script to use full screen capture
   - Crop to scrcpy window size

---

## OCR Issues

### Poor OCR Quality

**Problem:** Extracted text is garbled or inaccurate

**Solutions:**

1. **Increase screen resolution**:
   ```json
   "scrcpy": {
     "max_size": 2560
   }
   ```

2. **Preprocess images better:**
   - Edit `OCRProcessor.preprocess_image()` in script
   - Add contrast enhancement
   - Add denoising

3. **Try different PSM mode**:
   ```json
   "ocr": {
     "psm_mode": 3
   }
   ```
   
   PSM modes:
   - 3: Fully automatic page segmentation (default)
   - 6: Uniform block of text (current default)
   - 11: Sparse text
   - 13: Raw line

4. **Use better OCR engine:**
   - Install Tesseract 5.x (latest)
   - Download better trained data files

5. **Check Kindle font settings:**
   - Use cleaner fonts in Kindle
   - Increase font size
   - Increase line spacing

### OCR Too Slow

**Problem:** OCR takes forever

**Solutions:**

1. **Reduce image size before OCR:**
   ```python
   # In preprocess_image()
   img = img.resize((img.width // 2, img.height // 2))
   ```

2. **Use faster PSM mode:**
   ```json
   "ocr": {
     "psm_mode": 13
   }
   ```

3. **Disable preprocessing:**
   ```json
   "ocr": {
     "preprocess": false
   }
   ```

### Wrong Language Detected

**Problem:** OCR expects wrong language

**Solutions:**

1. **Install language pack:**
   - Download from: https://github.com/tesseract-ocr/tessdata
   - Place in: `C:\Program Files\Tesseract-OCR\tessdata\`

2. **Update config:**
   ```json
   "ocr": {
     "language": "fra"
   }
   ```

   Common codes:
   - eng: English
   - fra: French
   - deu: German
   - spa: Spanish
   - ita: Italian
   - jpn: Japanese
   - chi_sim: Chinese Simplified

---

## Performance Issues

### Script Runs Slow

**Problem:** Capture takes too long

**Solutions:**

1. **Reduce page turn delay:**
   ```json
   "capture": {
     "page_turn_delay": 1.5
   }
   ```

2. **Reduce scrcpy resolution:**
   ```json
   "scrcpy": {
     "max_size": 1280
   }
   ```

3. **Disable image preprocessing:**
   ```json
   "ocr": {
     "preprocess": false
   }
   ```

4. **Capture screenshots only (skip OCR):**
   - Comment out OCR calls in script
   - Run OCR separately later

### Device Gets Hot

**Problem:** Phone overheats during long captures

**Solutions:**

1. **Enable device sleep:**
   ```python
   # In scrcpy command, remove:
   "--stay-awake",
   "--turn-screen-off"
   ```

2. **Reduce bitrate:**
   ```json
   "scrcpy": {
     "bitrate": "2M"
   }
   ```

3. **Take breaks:**
   - Capture in smaller batches
   - Let device cool between batches

---

## Markdown Output Issues

### Formatting Is Bad

**Problem:** Markdown output is poorly formatted

**Solutions:**

1. **Improve OCR quality first** (see OCR Issues above)

2. **Post-process markdown:**
   - Edit `generate_markdown()` function
   - Add paragraph detection
   - Add heading detection

3. **Manual cleanup:**
   - Open markdown in editor
   - Use find/replace for common issues
   - Most markdown editors have cleanup tools

### Page Numbers Wrong

**Problem:** Page numbers don't match book

**Solutions:**

1. **Verify starting page:**
   - Make absolutely sure you're on the correct page
   - Account for cover/title pages

2. **Check page turn count:**
   - Verify each page turn is successful
   - Add logging to confirm page numbers

---

## Error Messages

### "ModuleNotFoundError: No module named 'win32gui'"

**Solution:**
```bash
pip install pywin32

# If that fails:
pip install --user pywin32

# Then run:
python Scripts/pywin32_postinstall.py -install
```

### "AttributeError: module 'pytesseract' has no attribute 'image_to_string'"

**Solution:**
```bash
# Reinstall pytesseract
pip uninstall pytesseract
pip install pytesseract
```

### "PermissionError: [WinError 5] Access is denied"

**Solution:**
- Run Command Prompt as Administrator
- Or use `--user` flag with pip
- Check antivirus isn't blocking

---

## Testing & Verification

### Run System Test

Before capturing, verify everything works:

```bash
python test_system.py
```

This will check:
- Python packages installed
- Tesseract OCR working
- ADB connection
- scrcpy launch
- OCR functionality

### Manual Component Tests

**Test ADB:**
```bash
adb devices
adb shell input tap 500 500
```

**Test scrcpy:**
```bash
scrcpy --max-size 1920
```

**Test Tesseract:**
```bash
tesseract --version
```

**Test Python imports:**
```python
python -c "import win32gui; import PIL; import pytesseract; print('All packages OK')"
```

---

## Still Having Issues?

1. **Run with verbose mode:**
   ```bash
   python kindle_capture_cli.py --book "Test" --start 1 --end 2 --verbose
   ```

2. **Check all paths in config.json**

3. **Try with just 1-2 pages first**

4. **Verify each component works individually**

5. **Update all tools to latest versions**

---

## Common Command Reference

```bash
# Check ADB devices
adb devices

# Restart ADB
adb kill-server
adb start-server

# Check device screen size
adb shell wm size

# Manual page turn test
adb shell input swipe 800 500 200 500 200

# Manual tap test
adb shell input tap 900 500

# Take manual screenshot via ADB
adb shell screencap -p /sdcard/test.png
adb pull /sdcard/test.png

# Test scrcpy
scrcpy --max-size 1920 --window-title TEST

# Check Python packages
pip list | findstr "pywin32 Pillow pytesseract"

# Test Tesseract
tesseract --list-langs
```
