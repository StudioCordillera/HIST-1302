"""
XML Validation Script for HIST-1302 OCR Output
==============================================

Validates XML files against the QC standards defined in QC_STANDARDS.md

Usage:
    # Validate single file
    python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
    
    # Validate entire directory
    python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import re
import sys


class XMLValidator:
    """Validates OCR-generated XML files against QC standards."""
    
    REQUIRED_METADATA_FIELDS = [
        'page_number', 'chapter', 'chapter_title', 'book_title',
        'capture_date', 'ocr_version', 'image_source', 'processing_timestamp'
    ]
    
    REQUIRED_QC_FIELDS = [
        'ocr_confidence', 'manual_review_required', 'issues_detected', 'reviewed_by'
    ]
    
    VALID_SECTION_TYPES = ['header', 'body', 'footer']
    
    def __init__(self, verbose=False):
        """Initialize validator."""
        self.verbose = verbose
        self.errors = []
        self.warnings = []
    
    def log(self, message, level='INFO'):
        """Log a message."""
        if self.verbose or level in ['ERROR', 'WARNING']:
            prefix = {
                'INFO': '  ℹ',
                'WARNING': '  ⚠',
                'ERROR': '  ✗'
            }.get(level, '  ')
            print(f"{prefix} {message}")
    
    def validate_file(self, xml_path):
        """
        Validate a single XML file.
        
        Args:
            xml_path: Path to XML file
            
        Returns:
            tuple: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        xml_file = Path(xml_path)
        
        if not xml_file.exists():
            self.errors.append(f"File not found: {xml_path}")
            return False, self.errors, self.warnings
        
        self.log(f"Validating: {xml_file.name}")
        
        # 1. Parse XML
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError as e:
            self.errors.append(f"XML parse error: {e}")
            return False, self.errors, self.warnings
        
        self.log("XML is well-formed", 'INFO')
        
        # 2. Check root element
        if root.tag != 'page':
            self.errors.append(f"Root element must be 'page', got '{root.tag}'")
        
        # 3. Validate metadata section
        self._validate_metadata(root)
        
        # 4. Validate content section
        self._validate_content(root)
        
        # 5. Validate quality control section
        self._validate_quality_control(root)
        
        # 6. Validate filename matches page number
        self._validate_filename(xml_file, root)
        
        # 7. Check encoding
        self._validate_encoding(xml_file)
        
        # Report results
        is_valid = len(self.errors) == 0
        
        if is_valid:
            self.log("✓ Validation passed", 'INFO')
        else:
            self.log(f"✗ Validation failed with {len(self.errors)} error(s)", 'ERROR')
        
        if self.warnings:
            self.log(f"⚠ {len(self.warnings)} warning(s)", 'WARNING')
        
        return is_valid, self.errors, self.warnings
    
    def _validate_metadata(self, root):
        """Validate metadata section."""
        metadata = root.find('metadata')
        
        if metadata is None:
            self.errors.append("Missing <metadata> section")
            return
        
        # Check all required fields present
        for field in self.REQUIRED_METADATA_FIELDS:
            elem = metadata.find(field)
            if elem is None:
                self.errors.append(f"Missing required metadata field: <{field}>")
            elif elem.text is None or elem.text.strip() == '':
                self.errors.append(f"Empty metadata field: <{field}>")
        
        # Validate specific field formats
        page_num = metadata.find('page_number')
        if page_num is not None and page_num.text:
            try:
                int(page_num.text)
            except ValueError:
                self.errors.append(f"page_number must be integer, got: {page_num.text}")
        
        chapter = metadata.find('chapter')
        if chapter is not None and chapter.text:
            try:
                ch_num = int(chapter.text)
                if ch_num < 21 or ch_num > 24:
                    self.warnings.append(f"Chapter {ch_num} outside expected range (21-24)")
            except ValueError:
                self.errors.append(f"chapter must be integer, got: {chapter.text}")
        
        # Validate date format
        capture_date = metadata.find('capture_date')
        if capture_date is not None and capture_date.text:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', capture_date.text):
                self.errors.append(f"capture_date must be YYYY-MM-DD format, got: {capture_date.text}")
        
        # Validate timestamp format
        timestamp = metadata.find('processing_timestamp')
        if timestamp is not None and timestamp.text:
            try:
                # Basic ISO 8601 check
                if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', timestamp.text):
                    self.errors.append(f"Invalid timestamp format: {timestamp.text}")
            except Exception:
                self.errors.append(f"Invalid timestamp: {timestamp.text}")
        
        self.log("Metadata section validated")
    
    def _validate_content(self, root):
        """Validate content section."""
        content = root.find('content')
        
        if content is None:
            self.errors.append("Missing <content> section")
            return
        
        sections = content.findall('section')
        
        if not sections:
            self.warnings.append("No sections found in content")
            return
        
        # Track section types
        section_types = []
        
        for section in sections:
            section_type = section.get('type')
            
            if section_type is None:
                self.errors.append("Section missing 'type' attribute")
                continue
            
            if section_type not in self.VALID_SECTION_TYPES:
                self.errors.append(f"Invalid section type: {section_type}")
            
            section_types.append(section_type)
            
            # Validate section content
            if section_type == 'body':
                self._validate_body_section(section)
        
        # Check that we have at least a body section
        if 'body' not in section_types:
            self.warnings.append("No 'body' section found")
        
        self.log("Content section validated")
    
    def _validate_body_section(self, body_section):
        """Validate body section structure."""
        paragraphs = body_section.findall('paragraph')
        
        if not paragraphs:
            self.warnings.append("Body section has no paragraphs")
            return
        
        # Check paragraph IDs are sequential
        expected_id = 1
        for para in paragraphs:
            para_id = para.get('id')
            
            if para_id is None:
                self.errors.append("Paragraph missing 'id' attribute")
                continue
            
            try:
                id_num = int(para_id)
                if id_num != expected_id:
                    self.warnings.append(f"Paragraph ID not sequential: expected {expected_id}, got {id_num}")
                expected_id = id_num + 1
            except ValueError:
                self.errors.append(f"Paragraph ID must be integer, got: {para_id}")
            
            # Check paragraph has text
            text_elem = para.find('text')
            if text_elem is None:
                self.errors.append(f"Paragraph {para_id} missing <text> element")
            elif not text_elem.text or text_elem.text.strip() == '':
                self.warnings.append(f"Paragraph {para_id} has empty text")
    
    def _validate_quality_control(self, root):
        """Validate quality control section."""
        qc = root.find('quality_control')
        
        if qc is None:
            self.errors.append("Missing <quality_control> section")
            return
        
        # Check all required fields
        for field in self.REQUIRED_QC_FIELDS:
            elem = qc.find(field)
            if elem is None:
                self.errors.append(f"Missing required QC field: <{field}>")
            elif elem.text is None or elem.text.strip() == '':
                self.errors.append(f"Empty QC field: <{field}>")
        
        # Validate confidence score
        confidence = qc.find('ocr_confidence')
        if confidence is not None and confidence.text:
            try:
                conf_value = float(confidence.text)
                if conf_value < 0.0 or conf_value > 1.0:
                    self.errors.append(f"ocr_confidence must be 0.0-1.0, got: {conf_value}")
                elif conf_value < 0.70:
                    self.warnings.append(f"Low OCR confidence: {conf_value:.2f}")
            except ValueError:
                self.errors.append(f"ocr_confidence must be float, got: {confidence.text}")
        
        # Validate manual review flag
        manual_review = qc.find('manual_review_required')
        if manual_review is not None and manual_review.text:
            if manual_review.text.lower() not in ['true', 'false']:
                self.errors.append(f"manual_review_required must be 'true' or 'false', got: {manual_review.text}")
        
        # Check consistency: low confidence should flag manual review
        if confidence is not None and manual_review is not None:
            try:
                conf_value = float(confidence.text)
                needs_review = manual_review.text.lower() == 'true'
                
                if conf_value < 0.85 and not needs_review:
                    self.warnings.append(f"Low confidence ({conf_value:.2f}) but manual_review_required is false")
            except (ValueError, AttributeError):
                pass
        
        self.log("Quality control section validated")
    
    def _validate_filename(self, xml_file, root):
        """Validate filename matches page number."""
        metadata = root.find('metadata')
        if metadata is None:
            return
        
        page_num_elem = metadata.find('page_number')
        if page_num_elem is None or not page_num_elem.text:
            return
        
        try:
            page_num = int(page_num_elem.text)
            expected_filename = f"page_{page_num:04d}.xml"
            
            if xml_file.name != expected_filename:
                self.warnings.append(
                    f"Filename '{xml_file.name}' doesn't match page number {page_num} "
                    f"(expected '{expected_filename}')"
                )
        except ValueError:
            pass
    
    def _validate_encoding(self, xml_file):
        """Validate file encoding."""
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if 'encoding="UTF-8"' not in first_line and 'encoding="utf-8"' not in first_line:
                    self.warnings.append("XML declaration should specify UTF-8 encoding")
        except UnicodeDecodeError:
            self.errors.append("File is not valid UTF-8")
        except Exception as e:
            self.warnings.append(f"Could not check encoding: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate OCR XML output against QC standards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file
  python validate_xml_output.py --input-file 01_TEXTBOOK/OCR/01_XML_OUTPUT/page_0515.xml
  
  # Validate entire directory
  python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT
  
  # Verbose output
  python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT --verbose
        """
    )
    
    parser.add_argument(
        '--input-file',
        help='Single XML file to validate'
    )
    
    parser.add_argument(
        '--input-dir',
        help='Directory containing XML files to validate'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if not args.input_file and not args.input_dir:
        parser.error('Either --input-file or --input-dir must be specified')
    
    validator = XMLValidator(verbose=args.verbose)
    
    # Collect files to validate
    files_to_validate = []
    
    if args.input_file:
        files_to_validate.append(Path(args.input_file))
    
    if args.input_dir:
        input_dir = Path(args.input_dir)
        if not input_dir.exists():
            print(f"Error: Directory not found: {input_dir}")
            sys.exit(1)
        
        files_to_validate.extend(sorted(input_dir.glob('*.xml')))
    
    if not files_to_validate:
        print("No XML files found to validate")
        sys.exit(0)
    
    print(f"\nValidating {len(files_to_validate)} file(s)...")
    print("=" * 60)
    
    # Validate all files
    results = []
    for xml_file in files_to_validate:
        is_valid, errors, warnings = validator.validate_file(xml_file)
        results.append({
            'file': xml_file,
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings
        })
        
        if not is_valid or warnings:
            print()
            if errors:
                print(f"  Errors in {xml_file.name}:")
                for error in errors:
                    print(f"    • {error}")
            if warnings:
                print(f"  Warnings in {xml_file.name}:")
                for warning in warnings:
                    print(f"    • {warning}")
        
        print()
    
    # Summary
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    total = len(results)
    valid = sum(1 for r in results if r['valid'])
    invalid = total - valid
    total_errors = sum(len(r['errors']) for r in results)
    total_warnings = sum(len(r['warnings']) for r in results)
    
    print(f"Total files:       {total}")
    print(f"Valid:             {valid}")
    print(f"Invalid:           {invalid}")
    print(f"Total errors:      {total_errors}")
    print(f"Total warnings:    {total_warnings}")
    
    if invalid > 0:
        print(f"\n❌ {invalid} file(s) failed validation")
        print("\nFiles needing attention:")
        for result in results:
            if not result['valid']:
                print(f"  • {result['file'].name}")
        sys.exit(1)
    elif total_warnings > 0:
        print(f"\n⚠ All files valid, but {total_warnings} warning(s) found")
        print("\nFiles with warnings:")
        for result in results:
            if result['warnings']:
                print(f"  • {result['file'].name}")
        sys.exit(0)
    else:
        print("\n✓ All files passed validation!")
        sys.exit(0)


if __name__ == '__main__':
    main()
