# OCR to XML Conversion - Quality Control Standards

## Overview

This document defines the quality control (QC) standards for converting OCR-processed textbook images to XML format. All XML outputs must conform to these standards to ensure consistency and data quality.

## Directory Structure

```
01_TEXTBOOK/OCR/
├── 00_IMPORT/              # Input files
│   └── tmp/
│       └── CH21-24/        # Chapter 21-24 images (pages 515-617)
├── 01_XML_OUTPUT/          # Generated XML files
└── 02_EXAMPLES/            # Example XML files demonstrating QC standards
    ├── example_page_001.xml
    └── example_page_002.xml
```

## XML Schema Structure

### Required Root Element
Every XML file must have a single root element: `<page>`

### Required Child Elements

#### 1. Metadata Section (`<metadata>`)
Contains information about the page and processing:

```xml
<metadata>
    <page_number>515</page_number>              <!-- Page number in textbook -->
    <chapter>21</chapter>                        <!-- Chapter number -->
    <chapter_title>The Progressive Era</chapter_title>  <!-- Chapter title -->
    <book_title>U.S. History HIST 1302</book_title>    <!-- Textbook title -->
    <capture_date>2025-11-13</capture_date>     <!-- Date image was captured -->
    <ocr_version>Tesseract 5.0</ocr_version>    <!-- OCR software version -->
    <image_source>page_0515.png</image_source>   <!-- Source image filename -->
    <processing_timestamp>2025-11-13T05:37:00Z</processing_timestamp>  <!-- ISO 8601 timestamp -->
</metadata>
```

**Required Fields:**
- `page_number`: Integer, must match physical page number
- `chapter`: Integer, chapter number (21-24 for current batch)
- `chapter_title`: String, full chapter title
- `book_title`: String, consistent across all pages
- `capture_date`: ISO 8601 date format (YYYY-MM-DD)
- `ocr_version`: String, OCR software and version
- `image_source`: String, source image filename
- `processing_timestamp`: ISO 8601 datetime with timezone

#### 2. Content Section (`<content>`)
Contains the actual page content structured into sections:

```xml
<content>
    <section type="header">
        <text>Chapter 21: The Progressive Era</text>
    </section>
    
    <section type="body">
        <paragraph id="1">
            <text>The Progressive Era (1890-1920) was a period of widespread social activism...</text>
        </paragraph>
        
        <paragraph id="2">
            <text>Progressives sought to address the problems caused by industrialization...</text>
        </paragraph>
        
        <!-- Optional: Lists -->
        <list type="unordered">
            <item>The establishment of regulatory agencies</item>
            <item>Child labor laws</item>
            <item>Pure Food and Drug Act</item>
        </list>
    </section>
    
    <section type="footer">
        <text>Page 515</text>
    </section>
</content>
```

**Section Types:**
- `header`: Page/chapter headers
- `body`: Main content
- `footer`: Page footers, page numbers

**Content Elements:**
- `<paragraph>`: Text paragraphs with required `id` attribute (sequential numbering)
- `<text>`: Text content within sections or paragraphs
- `<list>`: Optional, for lists with `type` attribute (`ordered` or `unordered`)
- `<item>`: List items

#### 3. Quality Control Section (`<quality_control>`)
Documents the OCR quality and review status:

```xml
<quality_control>
    <ocr_confidence>0.95</ocr_confidence>              <!-- 0.0 to 1.0 -->
    <manual_review_required>false</manual_review_required>  <!-- true/false -->
    <issues_detected>none</issues_detected>            <!-- or description -->
    <reviewed_by>automated</reviewed_by>               <!-- or reviewer name -->
</quality_control>
```

**Required Fields:**
- `ocr_confidence`: Decimal 0.0 to 1.0, average OCR confidence score
- `manual_review_required`: Boolean (true/false)
  - Set to `true` if confidence < 0.85
  - Set to `true` if issues detected
- `issues_detected`: String describing any issues or "none"
- `reviewed_by`: String, "automated" or reviewer name

## Quality Control Standards

### 1. OCR Confidence Thresholds

| Confidence Score | Status | Action Required |
|------------------|--------|-----------------|
| ≥ 0.95 | Excellent | No review needed |
| 0.85 - 0.94 | Good | Optional spot check |
| 0.70 - 0.84 | Fair | Manual review recommended |
| < 0.70 | Poor | Manual review required |

### 2. Mandatory Quality Checks

Before finalizing any XML file, verify:

- [ ] **Valid XML**: File parses without errors
- [ ] **All required elements**: Metadata, content, and QC sections present
- [ ] **Proper encoding**: UTF-8 encoding declared and used
- [ ] **Sequential IDs**: Paragraph IDs are sequential integers
- [ ] **Page numbering**: Page numbers match source images
- [ ] **Chapter mapping**: Correct chapter assigned based on page number
- [ ] **Timestamp format**: ISO 8601 format with timezone
- [ ] **Text completeness**: No truncated paragraphs or missing sections

### 3. Content Structure Guidelines

**Text Parsing:**
- Preserve original paragraph structure
- Remove excessive whitespace
- Maintain line breaks only where meaningful
- Clean up OCR artifacts (e.g., "|" instead of "l")

**Section Classification:**
- **Header**: Usually contains chapter title or section heading
  - Typically the first line of the page
  - Often in different formatting (bold, larger)
  
- **Body**: Main content of the page
  - Group related sentences into paragraphs
  - Separate distinct paragraphs
  - Identify lists when present
  
- **Footer**: Page numbers and footer text
  - Usually the last line of the page
  - May contain page numbers or publication info

**Paragraph Guidelines:**
- One `<paragraph>` per logical paragraph
- Each paragraph gets a unique sequential `id`
- Combine fragmented sentences from OCR into complete paragraphs
- Don't split paragraphs unless there's a clear break

### 4. Chapter Mapping

For pages 515-617 (Chapters 21-24):

| Page Range | Chapter | Chapter Title |
|------------|---------|---------------|
| 515-539 | 21 | The Progressive Era |
| 540-564 | 22 | World War I and the 1920s |
| 565-589 | 23 | The Great Depression |
| 590-617 | 24 | World War II |

## File Naming Convention

XML output files must follow this naming pattern:
```
page_XXXX.xml
```

Where:
- `XXXX` is the 4-digit zero-padded page number
- Examples: `page_0515.xml`, `page_0516.xml`, `page_0617.xml`

## Validation Process

### Automated Validation
Run the validation script to check all XML files:

```bash
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
```

The validator checks:
- XML well-formedness
- Required elements present
- Valid confidence scores
- Proper date/timestamp formats
- Sequential paragraph IDs
- Filename matches page number

### Manual Review Criteria

Manual review is required when:
1. OCR confidence < 0.85
2. Automated validation fails
3. Complex page layouts (tables, diagrams, multi-column)
4. Mathematical formulas or special characters
5. First and last pages of each chapter

### Review Process

For pages requiring manual review:

1. **Open source image** and XML side-by-side
2. **Verify accuracy**: Compare text in XML to image
3. **Check structure**: Ensure paragraphs and sections are correctly identified
4. **Correct errors**: Fix OCR mistakes, spelling errors, formatting
5. **Update QC section**:
   - Set `reviewed_by` to your name
   - Update `issues_detected` if any found
   - Set `manual_review_required` to `false` after review

## Common Issues and Solutions

### Issue: Low OCR Confidence
**Causes:**
- Poor image quality
- Complex layouts
- Small fonts
- Handwritten annotations

**Solutions:**
- Re-capture at higher resolution
- Adjust image preprocessing
- Manual text entry for problematic sections

### Issue: Incorrect Paragraph Breaks
**Causes:**
- OCR treating each line as separate
- Multi-column layouts

**Solutions:**
- Manually merge related sentences
- Review page layout in source image
- Adjust parsing logic for specific patterns

### Issue: Missing Header/Footer
**Causes:**
- Header/footer not detected by heuristics
- Non-standard page layout

**Solutions:**
- Manually add header/footer sections
- Update detection rules if pattern is common

### Issue: Special Characters
**Causes:**
- OCR misreading symbols
- Encoding issues

**Solutions:**
- Use Unicode escape sequences
- Verify UTF-8 encoding
- Manual correction

## Example Workflow

### Single Page Conversion

```bash
# Convert single image to XML
python ocr_to_xml_converter.py \
  --input-file 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/page_0515.png \
  --page-number 515 \
  --chapter 21

# Validate output
python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml

# Manual review if needed
vim 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
```

### Batch Conversion

```bash
# Convert all images in directory
python ocr_to_xml_converter.py \
  --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
  --output-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT \
  --start-page 515

# Validate all output
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

# Review flagged files
# (validation script will list files needing review)
```

## Quality Metrics

Track these metrics for each batch:

- **Total pages processed**: Count of XML files generated
- **Average OCR confidence**: Mean confidence across all pages
- **Manual review rate**: Percentage requiring manual review
- **Error rate**: Percentage with validation errors
- **Processing time**: Time per page

Target metrics:
- Average confidence: ≥ 0.90
- Manual review rate: ≤ 15%
- Error rate: ≤ 5%
- Processing time: ≤ 30 seconds/page

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-13 | Initial QC standards document |

## Contact

For questions about QC standards or to report issues:
- Review example files in `01_TEXTBOOK/OCR/02_EXAMPLES/`
- Check this documentation
- Consult with course instructor

---

**Last Updated**: 2025-11-13  
**Document Owner**: HIST-1302 Course Team
