"""
Quick Test - Capture pages iii through xiv
Roman numerals: iii = 3, iv = 4, ..., xiv = 14
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kindle_capture import KindleCaptureConfig, KindleCaptureOrchestrator

def main():
    print("\n" + "="*60)
    print(" Quick Test: Capture Table of Contents Pages")
    print("="*60 + "\n")
    
    # Initialize configuration
    config = KindleCaptureConfig()
    
    # Check dependencies
    print("Checking dependencies...")
    if not os.path.exists(config.adb_path):
        print(f"[FAIL] ADB not found at: {config.adb_path}")
        return
    print("[OK] ADB found")
    
    if not os.path.exists(config.tesseract_path):
        print(f"[WARN] Tesseract not found at: {config.tesseract_path}")
        print("  OCR will be skipped for this test")
        print("  Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        # Continue anyway for testing capture only
    else:
        print("[OK] Tesseract found")
    
    # Test configuration
    book_title = "College_Algebra_ToC"
    start_page = 3  # Roman numeral iii
    end_page = 14   # Roman numeral xiv
    total_pages = end_page - start_page + 1
    
    print(f"\n[INFO] Book: {book_title}")
    print(f"[INFO] Pages: {start_page} to {end_page} ({total_pages} pages)")
    print(f"[INFO] Roman numerals: iii through xiv")
    print(f"\n[IMPORTANT] Make sure your Kindle app is on page iii (Brief Contents)")
    
    confirm = input("\nReady to capture? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Run capture
    orchestrator = KindleCaptureOrchestrator(config)
    success = orchestrator.capture_page_range(start_page, end_page, book_title)
    
    if success:
        print("\n" + "="*60)
        print(" [SUCCESS] Capture Complete!")
        print("="*60)
        print(f"\nCheck the 'kindle_captures' folder for:")
        print(f"  - {book_title}_{start_page}-{end_page}_TIMESTAMP.md")
        print(f"  - screenshots/ folder with PNG files")
        print(f"  - text_data/ folder with TXT files")
    else:
        print("\n[FAIL] Capture failed. Check error messages above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[FAIL] Interrupted by user")
    except Exception as e:
        print(f"\n[FAIL] Fatal error: {e}")
        import traceback
        traceback.print_exc()
