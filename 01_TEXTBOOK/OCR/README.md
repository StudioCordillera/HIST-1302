# OCR to XML Conversion Guide

## Overview

This guide explains how to convert OCR-processed textbook images (Chapters 21-24, pages 515-617) to structured XML format following the established quality control standards.

## Quick Start

### Prerequisites

1. **Python 3.7+** installed
2. **Tesseract OCR** installed (https://github.com/UB-Mannheim/tesseract/wiki)
3. **Required Python packages**:
   ```bash
   pip install Pillow pytesseract
   ```

### Basic Usage

```bash
# Convert all images in a directory
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24

# Validate the output
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
```

## Directory Structure

```
01_TEXTBOOK/OCR/
├── 00_IMPORT/              # Input files
│   └── tmp/
│       └── CH21-24/        # Place your chapter images here
│           ├── page_0515.png
│           ├── page_0516.png
│           └── ...
│
├── 01_XML_OUTPUT/          # Generated XML files (output)
│   ├── page_0515.xml
│   ├── page_0516.xml
│   └── ...
│
├── 02_EXAMPLES/            # Example XML files
│   ├── example_page_001.xml
│   └── example_page_002.xml
│
├── QC_STANDARDS.md         # Quality control standards (READ THIS!)
└── README.md               # This file
```

## Step-by-Step Guide

### Step 1: Prepare Your Images

1. Place all chapter images in `01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/`
2. Images should be named with page numbers (e.g., `page_0515.png`)
3. Supported formats: PNG, JPG, JPEG

**Image Quality Tips:**
- Use high resolution (recommended: 1920px width minimum)
- Ensure good contrast and readability
- Remove any borders or artifacts if possible

### Step 2: Review QC Standards

Before converting, familiarize yourself with the quality standards:

```bash
# Read the QC standards document
cat 01_TEXTBOOK/OCR/QC_STANDARDS.md

# Review example XML files
cat 01_TEXTBOOK/OCR/02_EXAMPLES/example_page_001.xml
```

Key points:
- All XML must include metadata, content, and quality_control sections
- OCR confidence threshold: 0.85 (below this requires manual review)
- Proper paragraph structure and sequential IDs
- Correct chapter mapping based on page numbers

### Step 3: Run the Conversion

**Option A: Batch Convert All Images**

```bash
python ocr_to_xml_converter.py \
  --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
  --output-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT \
  --start-page 515
```

**Option B: Convert Single Image**

```bash
python ocr_to_xml_converter.py \
  --input-file 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/page_0515.png \
  --page-number 515 \
  --chapter 21 \
  --output-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
```

**Windows Users:**

If Tesseract is not in your PATH:

```bash
python ocr_to_xml_converter.py \
  --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
  --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Step 4: Validate the Output

```bash
# Validate all generated XML files
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

# Validate with verbose output
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT --verbose

# Validate single file
python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
```

The validator checks:
- XML well-formedness
- Required elements present
- Correct data types and formats
- OCR confidence thresholds
- Sequential paragraph IDs
- Filename matches page number

### Step 5: Manual Review (If Needed)

Files requiring manual review will be flagged by the validator when:
- OCR confidence < 0.85
- Validation errors detected
- Warnings about structure or content

**Review Process:**

1. Open the XML file and source image side-by-side
2. Compare the text in the XML to the image
3. Correct any OCR errors or structural issues
4. Update the quality_control section:
   ```xml
   <quality_control>
       <ocr_confidence>0.82</ocr_confidence>
       <manual_review_required>false</manual_review_required>
       <issues_detected>corrected 3 OCR errors</issues_detected>
       <reviewed_by>Your Name</reviewed_by>
   </quality_control>
   ```
5. Re-validate the file

## Chapter Mapping

The converter automatically maps pages to chapters:

| Page Range | Chapter | Chapter Title |
|------------|---------|---------------|
| 515-539 | 21 | The Progressive Era |
| 540-564 | 22 | World War I and the 1920s |
| 565-589 | 23 | The Great Depression |
| 590-617 | 24 | World War II |

## XML Structure

Each XML file contains three main sections:

### 1. Metadata
Information about the page and processing:
```xml
<metadata>
    <page_number>515</page_number>
    <chapter>21</chapter>
    <chapter_title>The Progressive Era</chapter_title>
    <book_title>U.S. History HIST 1302</book_title>
    <capture_date>2025-11-13</capture_date>
    <ocr_version>Tesseract 5.0</ocr_version>
    <image_source>page_0515.png</image_source>
    <processing_timestamp>2025-11-13T05:37:00Z</processing_timestamp>
</metadata>
```

### 2. Content
Structured page content:
```xml
<content>
    <section type="header">
        <text>Chapter 21: The Progressive Era</text>
    </section>
    
    <section type="body">
        <paragraph id="1">
            <text>Main content here...</text>
        </paragraph>
    </section>
    
    <section type="footer">
        <text>Page 515</text>
    </section>
</content>
```

### 3. Quality Control
OCR quality metrics:
```xml
<quality_control>
    <ocr_confidence>0.95</ocr_confidence>
    <manual_review_required>false</manual_review_required>
    <issues_detected>none</issues_detected>
    <reviewed_by>automated</reviewed_by>
</quality_control>
```

## Troubleshooting

### Issue: "Tesseract not found"

**Solution:**
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Or specify the path: `--tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe"`

### Issue: "No images found"

**Solution:**
- Check that images are in the correct directory
- Verify file extensions (.png, .jpg, .jpeg)
- Use absolute or correct relative paths

### Issue: Low OCR confidence

**Solutions:**
- Use higher resolution images (increase scrcpy max-size)
- Improve image contrast/brightness
- Ensure text is clearly readable in source image
- Consider manual text entry for problematic sections

### Issue: Incorrect paragraph breaks

**Solutions:**
- Review the source image layout
- Manually edit XML to correct paragraph structure
- Update paragraph IDs to be sequential

### Issue: Missing headers/footers

**Solutions:**
- Check if header/footer exists in source image
- Manually add header/footer sections if present
- Header detection looks for "Chapter" keyword or short first lines
- Footer detection looks for page numbers or short last lines

## Advanced Usage

### Custom Chapter Mapping

If your page ranges differ, modify the chapter map:

```python
# In ocr_to_xml_converter.py, update CHAPTER_TITLES dictionary
CHAPTER_TITLES = {
    21: "Custom Chapter 21 Title",
    22: "Custom Chapter 22 Title",
    # ...
}

# Or pass custom mapping to batch_convert_directory()
custom_map = {
    515: 21,
    550: 22,
    580: 23,
    600: 24
}
```

### Batch Processing with Scripts

Create a bash/batch script for repeated conversions:

**convert_all.sh** (Linux/Mac):
```bash
#!/bin/bash
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
```

**convert_all.bat** (Windows):
```batch
@echo off
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
pause
```

### Processing Specific Page Ranges

```bash
# Convert only pages 515-520
for i in {515..520}; do
    python ocr_to_xml_converter.py \
        --input-file "01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/page_$(printf '%04d' $i).png" \
        --page-number $i \
        --chapter 21
done
```

## Quality Metrics

Track these for your conversion batch:

```bash
# Count total files
ls 01_TEXTBOOK/OCR/01_XML_OUTPUT/*.xml | wc -l

# Check for files needing review
grep -l "manual_review_required>true" 01_TEXTBOOK/OCR/01_XML_OUTPUT/*.xml

# Average confidence (requires jq or xml parsing)
# See QC_STANDARDS.md for target metrics
```

## Best Practices

1. **Start Small**: Test with 2-3 pages before batch converting all pages
2. **Review Examples**: Study the example XML files before starting
3. **Validate Early**: Run validation after converting small batches
4. **Fix Issues Promptly**: Address validation errors before continuing
5. **Document Changes**: Note any manual corrections in the XML
6. **Backup Originals**: Keep original images safe
7. **Version Control**: Commit XML files to git for tracking changes

## Files Reference

- **ocr_to_xml_converter.py** - Main conversion script
- **validate_xml_output.py** - Validation script
- **QC_STANDARDS.md** - Quality control standards (detailed)
- **02_EXAMPLES/** - Example XML files
- **01_XML_OUTPUT/** - Generated XML output directory

## Getting Help

1. **Read the documentation**:
   - This README
   - QC_STANDARDS.md
   - Example files

2. **Check validation output**:
   ```bash
   python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT --verbose
   ```

3. **Review example files**:
   ```bash
   cat 01_TEXTBOOK/OCR/02_EXAMPLES/example_page_001.xml
   ```

4. **Test with single file first**:
   ```bash
   python ocr_to_xml_converter.py --input-file test.png --page-number 515 --chapter 21
   python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
   ```

## Complete Example Workflow

```bash
# 1. Prepare images (place in 00_IMPORT/tmp/CH21-24/)

# 2. Test with one image
python ocr_to_xml_converter.py \
  --input-file 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/page_0515.png \
  --page-number 515 \
  --chapter 21

# 3. Validate test output
python validate_xml_output.py \
  --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml \
  --verbose

# 4. If test passes, convert all images
python ocr_to_xml_converter.py \
  --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24

# 5. Validate all output
python validate_xml_output.py \
  --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

# 6. Review any flagged files manually

# 7. Re-validate after corrections
python validate_xml_output.py \
  --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
```

## Expected Results

For the complete batch (pages 515-617, 103 pages):

- **Processing time**: ~30-60 seconds per page
- **Total time**: ~50-100 minutes for all pages
- **File size**: ~2-5 KB per XML file
- **Success rate target**: ≥95%
- **Average confidence target**: ≥0.90
- **Manual review rate**: ≤15%

---

**Last Updated**: 2025-11-13  
**Version**: 1.0  
**Contact**: HIST-1302 Course Team
