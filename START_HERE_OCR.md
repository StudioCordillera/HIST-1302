# 🚀 QUICK START - OCR to XML Conversion

## You're Ready to Convert Your Images!

Everything is set up. Here's how to get started in **3 simple steps**:

---

## Step 1: Place Your Images 📂

Copy your chapter images to:
```
01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/
```

**Image requirements:**
- Format: PNG, JPG, or JPEG
- Naming: `page_0515.png`, `page_0516.png`, etc.
- Pages: 515-617 (Chapters 21-24)

---

## Step 2: Run the Conversion ▶️

### Windows
```
Double-click: convert_ocr_to_xml.bat
```

### Mac/Linux
```bash
./convert_ocr_to_xml.sh
```

### Manual (any platform)
```bash
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
```

---

## Step 3: Check Your Results ✅

**Output location:**
```
01_TEXTBOOK/OCR/01_XML_OUTPUT/
```

The script automatically:
- ✅ Converts all images to XML
- ✅ Validates the XML output
- ✅ Reports any issues

---

## What If I Need Help? 🆘

### Quick Help
📄 **OCR_XML_USAGE.md** - Quick start guide with troubleshooting

### Complete Documentation
📄 **SYSTEM_SUMMARY.md** - Full system overview
📄 **01_TEXTBOOK/OCR/README.md** - Technical details
📄 **01_TEXTBOOK/OCR/QC_STANDARDS.md** - Quality standards

### Example Files
📄 **01_TEXTBOOK/OCR/02_EXAMPLES/example_page_001.xml**
📄 **01_TEXTBOOK/OCR/02_EXAMPLES/example_page_002.xml**

---

## Common Issues

### "Tesseract not found"
**Fix:** Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki

### "No images found"
**Fix:** Check images are in correct directory with .png/.jpg/.jpeg extension

### "Module not found"
**Fix:** Run `pip install Pillow pytesseract`

---

## What You'll Get

Each page becomes an XML file with:

✅ **Metadata** - Page number, chapter, dates, timestamps
✅ **Content** - Text structured into header, body paragraphs, footer
✅ **Quality** - OCR confidence score and review status

**Example output:**
```
01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0516.xml
...
01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0617.xml
```

---

## Processing Time

For 103 pages (Chapters 21-24):
- **Time:** 50-100 minutes
- **Per page:** 30-60 seconds
- **File size:** ~2-5 KB each

💡 **Tip:** Start with a few test pages first!

---

## Test Before Full Batch

### Test with single image:
```bash
python ocr_to_xml_converter.py \
  --input-file your_test_image.png \
  --page-number 515 \
  --chapter 21
```

### Validate the output:
```bash
python validate_xml_output.py \
  --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
```

### If test passes, run full batch:
```bash
./convert_ocr_to_xml.sh  # or .bat on Windows
```

---

## Chapter Mapping (Automatic)

The system automatically assigns chapters based on page numbers:

| Pages     | Chapter | Title |
|-----------|---------|-------|
| 515-539   | 21      | The Progressive Era |
| 540-564   | 22      | World War I and the 1920s |
| 565-589   | 23      | The Great Depression |
| 590-617   | 24      | World War II |

---

## Quality Thresholds

**OCR Confidence:**
- ≥0.95 = Excellent ✅
- 0.85-0.94 = Good ✓
- 0.70-0.84 = Fair ⚠️
- <0.70 = Needs review ❌

Files needing review will be flagged automatically.

---

## Ready? Let's Go! 🎯

1. ✅ Place images in `01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/`
2. ✅ Run `convert_ocr_to_xml.bat` or `./convert_ocr_to_xml.sh`
3. ✅ Check output in `01_TEXTBOOK/OCR/01_XML_OUTPUT/`

**That's it!** The system handles the rest.

---

## Need More Info?

📖 **OCR_XML_USAGE.md** - Complete usage guide  
📖 **SYSTEM_SUMMARY.md** - System overview  
📖 **01_TEXTBOOK/OCR/README.md** - Technical documentation

---

**Last Updated:** 2025-11-13  
**Status:** ✅ Ready for production use
