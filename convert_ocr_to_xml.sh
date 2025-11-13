#!/bin/bash
# OCR to XML Batch Conversion Script
# ====================================

echo ""
echo "========================================"
echo " OCR to XML Conversion for CH21-24"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo "[1/4] Checking dependencies..."
python3 -c "import PIL, pytesseract" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Missing required packages. Installing..."
    pip3 install Pillow pytesseract
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install packages"
        exit 1
    fi
fi
echo "     Dependencies OK"

echo ""
echo "[2/4] Converting images to XML..."
python3 ocr_to_xml_converter.py \
    --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 \
    --output-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Conversion failed"
    exit 1
fi

echo ""
echo "[3/4] Validating XML output..."
python3 validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

echo ""
echo "[4/4] Complete!"
echo ""
echo "Output files are in: 01_TEXTBOOK/OCR/01_XML_OUTPUT"
echo ""
