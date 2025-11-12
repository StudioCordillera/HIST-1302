"""
Kindle Capture CLI - Command-line interface for automated captures
"""

import argparse
import sys
import json
from pathlib import Path
from kindle_capture import KindleCaptureConfig, KindleCaptureOrchestrator

def load_config(config_file):
    """Load configuration from JSON file"""
    if not Path(config_file).exists():
        print(f"[FAIL] Config file not found: {config_file}")
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        return json.load(f)

def create_config_from_file(config_data):
    """Create KindleCaptureConfig object from JSON data"""
    config = KindleCaptureConfig()
    
    # Update paths
    if 'paths' in config_data:
        config.platform_tools_path = config_data['paths'].get('platform_tools', config.platform_tools_path)
        config.tesseract_path = config_data['paths'].get('tesseract', config.tesseract_path)
        config.output_folder = Path(config_data['paths'].get('output_folder', config.output_folder))
        config.adb_path = Path(config.platform_tools_path) / "adb.exe"
        
        # Recreate folders with new path
        config.screenshots_folder = config.output_folder / "screenshots"
        config.text_folder = config.output_folder / "text_data"
        config.output_folder.mkdir(exist_ok=True)
        config.screenshots_folder.mkdir(exist_ok=True)
        config.text_folder.mkdir(exist_ok=True)
    
    # Update scrcpy settings
    if 'scrcpy' in config_data:
        config.scrcpy_window_title = config_data['scrcpy'].get('window_title', config.scrcpy_window_title)
        config.scrcpy_max_size = config_data['scrcpy'].get('max_size', config.scrcpy_max_size)
        config.scrcpy_bitrate = config_data['scrcpy'].get('bitrate', config.scrcpy_bitrate)
        config.initial_delay = config_data['scrcpy'].get('initial_delay', config.initial_delay)
    
    # Update capture settings
    if 'capture' in config_data:
        config.page_turn_delay = config_data['capture'].get('page_turn_delay', config.page_turn_delay)
    
    # Update OCR settings
    if 'ocr' in config_data:
        config.ocr_lang = config_data['ocr'].get('language', config.ocr_lang)
    
    return config

def main():
    parser = argparse.ArgumentParser(
        description='Automated Kindle page capture and OCR tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Capture pages 1-50 from a book
  python kindle_capture_cli.py --book "My Book" --start 1 --end 50
  
  # Use custom config file
  python kindle_capture_cli.py --config my_config.json --book "My Book" --start 1 --end 50
  
  # Capture with custom output folder
  python kindle_capture_cli.py --book "My Book" --start 1 --end 50 --output my_output
        '''
    )
    
    # Required arguments
    parser.add_argument('--book', '-b', 
                       required=True,
                       help='Book title for output files')
    parser.add_argument('--start', '-s',
                       type=int,
                       required=True,
                       help='Starting page number')
    parser.add_argument('--end', '-e',
                       type=int,
                       required=True,
                       help='Ending page number')
    
    # Optional arguments
    parser.add_argument('--config', '-c',
                       default='config.json',
                       help='Path to config file (default: config.json)')
    parser.add_argument('--output', '-o',
                       help='Override output folder path')
    parser.add_argument('--delay', '-d',
                       type=float,
                       help='Override page turn delay (seconds)')
    parser.add_argument('--no-confirm',
                       action='store_true',
                       help='Skip confirmation prompt')
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate page numbers
    if args.start > args.end:
        print("[FAIL] Start page must be <= end page")
        sys.exit(1)
    
    # Load configuration
    print(f"Loading configuration from: {args.config}")
    config_data = load_config(args.config)
    config = create_config_from_file(config_data)
    
    # Apply command-line overrides
    if args.output:
        config.output_folder = Path(args.output)
        config.screenshots_folder = config.output_folder / "screenshots"
        config.text_folder = config.output_folder / "text_data"
        config.output_folder.mkdir(exist_ok=True)
        config.screenshots_folder.mkdir(exist_ok=True)
        config.text_folder.mkdir(exist_ok=True)
    
    if args.delay:
        config.page_turn_delay = args.delay
    
    # Check dependencies
    import os
    if not os.path.exists(config.adb_path):
        print(f"[FAIL] ADB not found at: {config.adb_path}")
        sys.exit(1)
    
    if not os.path.exists(config.tesseract_path):
        print(f"[FAIL] Tesseract not found at: {config.tesseract_path}")
        print("  Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
    
    # Display capture info
    total_pages = args.end - args.start + 1
    print("\n" + "="*60)
    print(" Kindle Capture Configuration")
    print("="*60)
    print(f"Book Title:    {args.book}")
    print(f"Page Range:    {args.start} - {args.end} ({total_pages} pages)")
    print(f"Output Folder: {config.output_folder}")
    print(f"Page Delay:    {config.page_turn_delay}s")
    print("="*60 + "\n")
    
    # Confirm
    if not args.no_confirm:
        print(f"[WARN] Make sure your Kindle app is open on page {args.start}")
        confirm = input("\nProceed? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    # Run capture
    try:
        orchestrator = KindleCaptureOrchestrator(config)
        success = orchestrator.capture_page_range(args.start, args.end, args.book)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[FAIL] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[FAIL] Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
