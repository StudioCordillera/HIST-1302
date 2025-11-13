# OCR to XML Conversion - Usage Instructions

## For HIST-1302 Chapters 21-24 (Pages 515-617)

### What This Does

This system converts OCR-processed textbook images from Chapters 21-24 into structured XML format, following established quality control standards.

---

## Quick Setup (First Time Only)

### 1. Install Prerequisites

**Python 3.7+**
- Download from: https://python.org
- During installation, check "Add Python to PATH"

**Tesseract OCR**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Default install path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Note the installation path if you choose a different location

**Python Packages**
```bash
pip install Pillow pytesseract
```

### 2. Verify Installation

```bash
# Check Python
python --version

# Check Tesseract
tesseract --version

# Check packages
python -c "import PIL, pytesseract; print('OK')"
```

---

## How to Convert Your Images

### Step 1: Place Your Images

1. Navigate to: `01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/`
2. Copy all your chapter images there
3. Images should be named: `page_0515.png`, `page_0516.png`, etc.

**Supported formats:** PNG, JPG, JPEG

### Step 2: Run the Conversion

**Windows:**
```cmd
Double-click: convert_ocr_to_xml.bat
```

**Mac/Linux:**
```bash
./convert_ocr_to_xml.sh
```

**Manual (all platforms):**
```bash
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
```

### Step 3: Check the Results

The script will:
1. ✓ Convert all images to XML
2. ✓ Validate the XML output
3. ✓ Report any issues

**Output location:** `01_TEXTBOOK/OCR/01_XML_OUTPUT/`

---

## Understanding the Output

### XML File Structure

Each page becomes an XML file like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<page>
    <metadata>
        <!-- Page information -->
    </metadata>
    
    <content>
        <!-- Page content -->
    </content>
    
    <quality_control>
        <!-- OCR quality metrics -->
    </quality_control>
</page>
```

### Quality Indicators

**OCR Confidence:**
- **0.95-1.00**: Excellent - no review needed ✓
- **0.85-0.94**: Good - optional review
- **0.70-0.84**: Fair - review recommended ⚠
- **< 0.70**: Poor - review required ❌

**Manual Review Flag:**
- `false`: Automated processing sufficient
- `true`: Human review recommended

---

## Troubleshooting

### "Tesseract not found"

**Problem:** Can't locate Tesseract OCR

**Solutions:**
1. Install Tesseract from the link above
2. Add to PATH (Windows: System Environment Variables)
3. Or specify path when running:
   ```bash
   python ocr_to_xml_converter.py \
     --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
     --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

### "No images found"

**Problem:** Script can't find your images

**Solutions:**
1. Check images are in: `01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/`
2. Verify file extensions: `.png`, `.jpg`, or `.jpeg`
3. Check spelling of directory name

### Low OCR Confidence

**Problem:** XML shows low confidence scores

**Solutions:**
1. Use higher resolution source images
2. Ensure images are clear and readable
3. Check image contrast and brightness
4. May need manual review/correction

### Validation Errors

**Problem:** Validator reports errors

**Solutions:**
1. Read the error messages carefully
2. Check the specific XML file mentioned
3. Compare to example files in `02_EXAMPLES/`
4. Manual correction may be needed

---

## Advanced Usage

### Convert Single Image

```bash
python ocr_to_xml_converter.py \
  --input-file path/to/page_0515.png \
  --page-number 515 \
  --chapter 21
```

### Validate Specific File

```bash
python validate_xml_output.py \
  --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
```

### Verbose Output

```bash
python ocr_to_xml_converter.py \
  --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
  --verbose

python validate_xml_output.py \
  --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT \
  --verbose
```

---

## Manual Review Process

When a file needs manual review:

### 1. Identify Files Needing Review

The validation script will list them, or check:
```bash
grep -l "manual_review_required>true" 01_TEXTBOOK/OCR/01_XML_OUTPUT/*.xml
```

### 2. Review the File

Open in text editor alongside source image:
- Compare XML text to image
- Fix OCR errors (typos, misread characters)
- Correct paragraph breaks if needed
- Fix section classification (header/body/footer)

### 3. Update Quality Control Section

```xml
<quality_control>
    <ocr_confidence>0.82</ocr_confidence>
    <manual_review_required>false</manual_review_required>  <!-- Change to false -->
    <issues_detected>corrected 3 spelling errors</issues_detected>  <!-- Note changes -->
    <reviewed_by>Your Name</reviewed_by>  <!-- Add your name -->
</quality_control>
```

### 4. Re-validate

```bash
python validate_xml_output.py \
  --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
```

---

## File Reference

| File | Purpose |
|------|---------|
| `ocr_to_xml_converter.py` | Main conversion script |
| `validate_xml_output.py` | XML validation script |
| `convert_ocr_to_xml.bat` | Windows batch script |
| `convert_ocr_to_xml.sh` | Linux/Mac shell script |
| `01_TEXTBOOK/OCR/README.md` | Detailed documentation |
| `01_TEXTBOOK/OCR/QC_STANDARDS.md` | Quality standards |
| `01_TEXTBOOK/OCR/02_EXAMPLES/` | Example XML files |

---

## Expected Processing Time

For 103 pages (CH21-24, pages 515-617):

- **Per page:** 30-60 seconds
- **Total time:** 50-100 minutes
- **Depends on:** Image resolution, computer speed

**Tip:** Start with a few pages to verify everything works before running the full batch.

---

## Quality Checklist

Before considering the conversion complete:

- [ ] All images converted to XML
- [ ] Validation script shows no errors
- [ ] Files needing review have been reviewed
- [ ] Spot-check random pages for accuracy
- [ ] Page numbers match source images
- [ ] Chapter assignments are correct
- [ ] Output files in `01_XML_OUTPUT/` directory

---

## Getting Help

1. **Read the documentation:**
   - `01_TEXTBOOK/OCR/README.md` (detailed guide)
   - `01_TEXTBOOK/OCR/QC_STANDARDS.md` (quality standards)

2. **Check example files:**
   - `01_TEXTBOOK/OCR/02_EXAMPLES/example_page_001.xml`
   - `01_TEXTBOOK/OCR/02_EXAMPLES/example_page_002.xml`

3. **Run validation with verbose mode:**
   ```bash
   python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT --verbose
   ```

4. **Test with single file first:**
   ```bash
   python ocr_to_xml_converter.py \
     --input-file test_image.png \
     --page-number 515 \
     --chapter 21
   ```

---

## Common Commands

```bash
# Full conversion (Windows)
convert_ocr_to_xml.bat

# Full conversion (Linux/Mac)
./convert_ocr_to_xml.sh

# Manual conversion
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24

# Validate all
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

# Validate one file
python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml

# Convert single image
python ocr_to_xml_converter.py --input-file image.png --page-number 515 --chapter 21
```

---

**Quick Start Summary:**

1. Install Python + Tesseract + packages
2. Place images in `01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/`
3. Run `convert_ocr_to_xml.bat` (Windows) or `./convert_ocr_to_xml.sh` (Mac/Linux)
4. Check output in `01_TEXTBOOK/OCR/01_XML_OUTPUT/`
5. Review any flagged files manually
6. Done! ✓

---

**Last Updated:** 2025-11-13  
**For:** HIST-1302 Chapters 21-24 OCR Conversion
