# Kindle Capture & OCR Tool - Installation

## 📦 You've Downloaded All Required Files!

This package contains a complete automated Kindle page capture and OCR system for Windows.

---

## 📋 What's Included

### Core Scripts
- **`kindle_capture.py`** - Main interactive script
- **`kindle_capture_cli.py`** - Command-line interface version
- **`test_system.py`** - System verification tool

### Configuration
- **`config.json`** - Settings (EDIT THIS FIRST)
- **`requirements.txt`** - Python dependencies

### Quick Launch Files
- **`quick_capture.bat`** - Windows quick launch
- **`run_test.bat`** - System test launcher

### Documentation
- **`PROJECT_OVERVIEW.md`** - **START HERE** - Overview and guide
- **`QUICKSTART.md`** - 5-minute setup guide
- **`README.md`** - Complete documentation
- **`TROUBLESHOOTING.md`** - Problem solving
- **`START_HERE.md`** - This file

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Install Tesseract OCR
Download and install: https://github.com/UB-Mannheim/tesseract/wiki

**Important:** Use default installation path: `C:\Program Files\Tesseract-OCR`

### 2️⃣ Install Python Packages
Open Command Prompt in this folder and run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Test Your Setup
Double-click: **`run_test.bat`**

If all tests pass ✅, you're ready!

If any tests fail ❌, see **TROUBLESHOOTING.md**

---

## 📖 What to Read First

### New Users
1. **PROJECT_OVERVIEW.md** - Read this first for complete understanding
2. **QUICKSTART.md** - Follow this for setup
3. Run **`run_test.bat`**

### Experienced Users
1. Edit **`config.json`** with your paths
2. Run **`run_test.bat`**
3. Start capturing: `python kindle_capture.py`

---

## ⚙️ Your Configuration

Before running, edit **`config.json`**:

```json
{
  "paths": {
    "platform_tools": "C:\\Users\\WORK_ADMIN\\Projects\\01_TOOLS\\ADB_Tools\\platform-tools",
    "tesseract": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    "output_folder": "kindle_captures"
  }
}
```

✅ **platform_tools** path is already set for your system  
⚠️ **Update tesseract path** if you install elsewhere

---

## 🎯 How to Use

### Method 1: Interactive
```bash
python kindle_capture.py
```
Enter book title and page range when prompted.

### Method 2: Command Line
```bash
python kindle_capture_cli.py --book "My Book" --start 1 --end 50
```

### Method 3: Batch File
1. Edit `quick_capture.bat`
2. Set your book title and page numbers
3. Double-click to run

---

## 📁 Output Location

All captures save to: **`kindle_captures/`** folder

Structure:
```
kindle_captures/
├── BookTitle_1-50_timestamp.md    ← Your formatted text
├── BookTitle_1-50_timestamp.json  ← Metadata
├── screenshots/                   ← Page images
└── text_data/                     ← Raw OCR text
```

---

## 🔧 System Requirements

### Already Installed ✅
- scrcpy (globally available)
- ADB Platform Tools (at specified path)

### Need to Install
- **Tesseract OCR** - Download from link above
- **Python 3.7+** - If not already installed
- **Python Packages** - Run: `pip install -r requirements.txt`

---

## 🐛 Having Issues?

1. **Run the system test:**
   ```bash
   python test_system.py
   ```

2. **Check troubleshooting guide:**
   Open **TROUBLESHOOTING.md**

3. **Verify configuration:**
   Make sure `config.json` has correct paths

4. **Test with 2-3 pages first:**
   ```bash
   python kindle_capture_cli.py --book "Test" --start 1 --end 3
   ```

---

## 📚 Documentation Index

| File | Purpose | When to Read |
|------|---------|--------------|
| **PROJECT_OVERVIEW.md** | Complete overview | Read first |
| **QUICKSTART.md** | Fast setup | Installation |
| **README.md** | Full documentation | Reference |
| **TROUBLESHOOTING.md** | Problem solving | When stuck |
| **START_HERE.md** | This file | Right now! |

---

## ⚡ Quick Commands

```bash
# Verify setup
python test_system.py

# Interactive mode
python kindle_capture.py

# Command line mode
python kindle_capture_cli.py --book "Title" --start 1 --end 50

# Check ADB connection
C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe devices

# Test scrcpy
scrcpy --max-size 1920
```

---

## ✅ Installation Checklist

- [ ] Downloaded all files
- [ ] Installed Tesseract OCR
- [ ] Installed Python packages (`pip install -r requirements.txt`)
- [ ] Edited `config.json` with correct paths
- [ ] Ran `run_test.bat` successfully
- [ ] Connected Android device
- [ ] Enabled USB debugging on Android
- [ ] Tested with 2-3 pages
- [ ] Ready to capture books!

---

## 🎓 What This Tool Does

1. **Connects** to your Android device via scrcpy (full resolution)
2. **Captures** screenshots of Kindle pages automatically
3. **Turns pages** using ADB commands (no manual interaction)
4. **Extracts text** using Tesseract OCR
5. **Creates** formatted markdown files with page numbers

**All automatically, in the background!**

---

## 🚨 Important Notes

- ✅ Works with books you own
- ✅ Personal backup and accessibility
- ✅ Fully local - no internet required
- ✅ Respects Kindle Terms of Service
- ⚠️ For personal use only

---

## 🎯 Next Steps

1. **Read PROJECT_OVERVIEW.md** for complete understanding
2. **Follow QUICKSTART.md** for installation
3. **Run run_test.bat** to verify everything works
4. **Start capturing** your first book!

---

**Need help?** → See TROUBLESHOOTING.md  
**Want details?** → See README.md  
**Ready to start?** → See QUICKSTART.md

**Questions?** All answers are in the documentation files! 📚
