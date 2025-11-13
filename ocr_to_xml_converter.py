"""
OCR to XML Converter for HIST-1302 Textbook
============================================

This script converts OCR-processed images to structured XML format
following the quality control standards defined in the examples.

Directory Structure:
    01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24/  - Input images
    01_TEXTBOOK/OCR/01_XML_OUTPUT/          - Output XML files
    01_TEXTBOOK/OCR/02_EXAMPLES/            - Example XML files (QC standards)

Usage:
    python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
    
    Or for single file:
    python ocr_to_xml_converter.py --input-file path/to/image.png --page-number 515 --chapter 21
"""

import argparse
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sys
import re

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install Pillow pytesseract")
    sys.exit(1)


class OCRToXMLConverter:
    """Converts OCR-processed images to structured XML format."""
    
    # Chapter titles mapping
    CHAPTER_TITLES = {
        21: "The Progressive Era",
        22: "World War I and the 1920s",
        23: "The Great Depression",
        24: "World War II"
    }
    
    def __init__(self, book_title="U.S. History HIST 1302", tesseract_path=None):
        """
        Initialize the converter.
        
        Args:
            book_title: Title of the textbook
            tesseract_path: Path to tesseract executable (if not in PATH)
        """
        self.book_title = book_title
        
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_text_from_image(self, image_path):
        """
        Extract text from image using OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            tuple: (extracted_text, confidence_score)
        """
        try:
            image = Image.open(image_path)
            
            # Get OCR data with confidence
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Extract text
            text = pytesseract.image_to_string(image)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return text, avg_confidence / 100.0
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return "", 0.0
    
    def parse_text_structure(self, text):
        """
        Parse OCR text into structured sections (header, body, footer).
        
        Args:
            text: Raw OCR text
            
        Returns:
            dict: Structured content with sections
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return {
                'header': [],
                'body': [],
                'footer': []
            }
        
        # Simple heuristic: first line as header, last line as footer
        header_lines = []
        footer_lines = []
        body_lines = []
        
        # Detect header (often contains "Chapter" or is short)
        if len(lines) > 0 and (
            'chapter' in lines[0].lower() or 
            len(lines[0].split()) <= 6
        ):
            header_lines.append(lines[0])
            remaining_lines = lines[1:]
        else:
            remaining_lines = lines
        
        # Detect footer (often contains page number or is short)
        if len(remaining_lines) > 0 and (
            re.search(r'page\s+\d+', remaining_lines[-1].lower()) or
            re.match(r'^\d+$', remaining_lines[-1]) or
            len(remaining_lines[-1].split()) <= 3
        ):
            footer_lines.append(remaining_lines[-1])
            body_lines = remaining_lines[:-1]
        else:
            body_lines = remaining_lines
        
        return {
            'header': header_lines,
            'body': body_lines,
            'footer': footer_lines
        }
    
    def create_xml_structure(self, page_number, chapter, image_filename, 
                            ocr_text, confidence, timestamp=None):
        """
        Create XML structure for a page.
        
        Args:
            page_number: Page number
            chapter: Chapter number
            image_filename: Source image filename
            ocr_text: Extracted OCR text
            confidence: OCR confidence score (0.0 to 1.0)
            timestamp: Processing timestamp (defaults to now)
            
        Returns:
            ElementTree.Element: Root XML element
        """
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create root element
        root = ET.Element('page')
        
        # Metadata section
        metadata = ET.SubElement(root, 'metadata')
        ET.SubElement(metadata, 'page_number').text = str(page_number)
        ET.SubElement(metadata, 'chapter').text = str(chapter)
        
        chapter_title = self.CHAPTER_TITLES.get(chapter, f"Chapter {chapter}")
        ET.SubElement(metadata, 'chapter_title').text = chapter_title
        ET.SubElement(metadata, 'book_title').text = self.book_title
        ET.SubElement(metadata, 'capture_date').text = datetime.now().strftime('%Y-%m-%d')
        ET.SubElement(metadata, 'ocr_version').text = 'Tesseract 5.0'
        ET.SubElement(metadata, 'image_source').text = image_filename
        ET.SubElement(metadata, 'processing_timestamp').text = timestamp
        
        # Content section
        content = ET.SubElement(root, 'content')
        
        # Parse text structure
        structure = self.parse_text_structure(ocr_text)
        
        # Add header section
        if structure['header']:
            header_section = ET.SubElement(content, 'section', type='header')
            for line in structure['header']:
                ET.SubElement(header_section, 'text').text = line
        
        # Add body section
        if structure['body']:
            body_section = ET.SubElement(content, 'section', type='body')
            
            # Group body lines into paragraphs (simple approach: split by empty lines)
            current_paragraph = []
            paragraph_id = 1
            
            for line in structure['body']:
                if line:
                    current_paragraph.append(line)
                elif current_paragraph:
                    # Create paragraph
                    para = ET.SubElement(body_section, 'paragraph', id=str(paragraph_id))
                    ET.SubElement(para, 'text').text = ' '.join(current_paragraph)
                    paragraph_id += 1
                    current_paragraph = []
            
            # Add final paragraph if exists
            if current_paragraph:
                para = ET.SubElement(body_section, 'paragraph', id=str(paragraph_id))
                ET.SubElement(para, 'text').text = ' '.join(current_paragraph)
        
        # Add footer section
        if structure['footer']:
            footer_section = ET.SubElement(content, 'section', type='footer')
            for line in structure['footer']:
                ET.SubElement(footer_section, 'text').text = line
        
        # Quality control section
        qc = ET.SubElement(root, 'quality_control')
        ET.SubElement(qc, 'ocr_confidence').text = f"{confidence:.2f}"
        
        # Determine if manual review is needed (confidence < 0.85)
        manual_review = 'true' if confidence < 0.85 else 'false'
        ET.SubElement(qc, 'manual_review_required').text = manual_review
        
        issues = 'low_confidence' if confidence < 0.85 else 'none'
        ET.SubElement(qc, 'issues_detected').text = issues
        ET.SubElement(qc, 'reviewed_by').text = 'automated'
        
        return root
    
    def prettify_xml(self, elem):
        """
        Return a pretty-printed XML string.
        
        Args:
            elem: XML element
            
        Returns:
            str: Formatted XML string
        """
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")
    
    def convert_image_to_xml(self, image_path, output_path, page_number, chapter):
        """
        Convert a single image to XML.
        
        Args:
            image_path: Path to input image
            output_path: Path for output XML file
            page_number: Page number
            chapter: Chapter number
            
        Returns:
            bool: True if successful
        """
        print(f"Processing: {image_path}")
        print(f"  Page: {page_number}, Chapter: {chapter}")
        
        # Extract text
        ocr_text, confidence = self.extract_text_from_image(image_path)
        
        if not ocr_text:
            print(f"  WARNING: No text extracted from image")
            return False
        
        print(f"  OCR Confidence: {confidence:.2%}")
        
        # Create XML structure
        xml_root = self.create_xml_structure(
            page_number=page_number,
            chapter=chapter,
            image_filename=Path(image_path).name,
            ocr_text=ocr_text,
            confidence=confidence
        )
        
        # Write to file
        xml_string = self.prettify_xml(xml_root)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        print(f"  ✓ Saved to: {output_path}")
        
        if confidence < 0.85:
            print(f"  ⚠ Low confidence - manual review recommended")
        
        return True
    
    def batch_convert_directory(self, input_dir, output_dir, start_page=515, 
                                chapter_map=None):
        """
        Convert all images in a directory to XML.
        
        Args:
            input_dir: Directory containing images
            output_dir: Directory for output XML files
            start_page: Starting page number
            chapter_map: Dict mapping page ranges to chapters
                        e.g., {515: 21, 540: 22, 565: 23, 590: 24}
        
        Returns:
            dict: Statistics about the conversion
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Default chapter mapping for pages 515-617
        if chapter_map is None:
            chapter_map = {
                515: 21,  # Chapter 21: pages 515-539
                540: 22,  # Chapter 22: pages 540-564
                565: 23,  # Chapter 23: pages 565-589
                590: 24   # Chapter 24: pages 590-617
            }
        
        # Find all images
        image_files = sorted(
            list(input_path.glob('*.png')) +
            list(input_path.glob('*.jpg')) +
            list(input_path.glob('*.jpeg'))
        )
        
        if not image_files:
            print(f"No images found in {input_dir}")
            return {'total': 0, 'success': 0, 'failed': 0}
        
        print(f"\nFound {len(image_files)} images to process")
        print("=" * 60)
        
        stats = {'total': len(image_files), 'success': 0, 'failed': 0}
        
        for i, image_file in enumerate(image_files, 1):
            # Extract page number from filename
            match = re.search(r'(\d+)', image_file.stem)
            if match:
                page_num = int(match.group(1))
            else:
                page_num = start_page + i - 1
            
            # Determine chapter
            chapter = max([ch for pg, ch in sorted(chapter_map.items()) if pg <= page_num])
            
            # Output filename
            output_file = output_path / f"page_{page_num:04d}.xml"
            
            print(f"\n[{i}/{len(image_files)}]")
            
            try:
                success = self.convert_image_to_xml(
                    image_path=image_file,
                    output_path=output_file,
                    page_number=page_num,
                    chapter=chapter
                )
                
                if success:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
                stats['failed'] += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("CONVERSION SUMMARY")
        print("=" * 60)
        print(f"Total files:     {stats['total']}")
        print(f"Successful:      {stats['success']}")
        print(f"Failed:          {stats['failed']}")
        print(f"Success rate:    {stats['success']/stats['total']*100:.1f}%")
        print(f"\nOutput directory: {output_path.absolute()}")
        
        return stats


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert OCR images to XML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all images in a directory
  python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24
  
  # Convert a single image
  python ocr_to_xml_converter.py --input-file page_0515.png --page-number 515 --chapter 21
  
  # Specify custom output directory
  python ocr_to_xml_converter.py --input-dir images/ --output-dir xml_output/
  
  # Specify tesseract path (Windows)
  python ocr_to_xml_converter.py --input-dir images/ --tesseract "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        """
    )
    
    parser.add_argument(
        '--input-dir',
        help='Directory containing input images'
    )
    
    parser.add_argument(
        '--input-file',
        help='Single input image file'
    )
    
    parser.add_argument(
        '--output-dir',
        default='01_TEXTBOOK/OCR/01_XML_OUTPUT',
        help='Directory for output XML files (default: 01_TEXTBOOK/OCR/01_XML_OUTPUT)'
    )
    
    parser.add_argument(
        '--page-number',
        type=int,
        help='Page number (required for single file conversion)'
    )
    
    parser.add_argument(
        '--chapter',
        type=int,
        help='Chapter number (required for single file conversion)'
    )
    
    parser.add_argument(
        '--start-page',
        type=int,
        default=515,
        help='Starting page number for batch conversion (default: 515)'
    )
    
    parser.add_argument(
        '--tesseract',
        help='Path to tesseract executable (if not in PATH)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.input_dir and not args.input_file:
        parser.error('Either --input-dir or --input-file must be specified')
    
    if args.input_file and (args.page_number is None or args.chapter is None):
        parser.error('--page-number and --chapter are required when using --input-file')
    
    # Create converter
    converter = OCRToXMLConverter(tesseract_path=args.tesseract)
    
    # Process files
    if args.input_file:
        # Single file conversion
        output_file = Path(args.output_dir) / f"page_{args.page_number:04d}.xml"
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        
        converter.convert_image_to_xml(
            image_path=args.input_file,
            output_path=output_file,
            page_number=args.page_number,
            chapter=args.chapter
        )
    else:
        # Batch conversion
        converter.batch_convert_directory(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            start_page=args.start_page
        )


if __name__ == '__main__':
    main()
