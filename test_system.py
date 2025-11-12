"""
System Test & Dependency Checker
Verifies all dependencies and configuration before running captures
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_header(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_status(name, status, message=""):
    """Print check status"""
    symbol = "[OK]" if status else "[FAIL]"
    print(f"{symbol} {name:<30} {'OK' if status else 'FAILED'}")
    if message:
        print(f"  -> {message}")
    return status

def check_python_packages():
    """Check if required Python packages are installed"""
    check_header("Python Packages")
    
    packages = {
        'pywin32': 'win32gui',
        'Pillow': 'PIL',
        'pytesseract': 'pytesseract'
    }
    
    all_ok = True
    for package, import_name in packages.items():
        try:
            __import__(import_name)
            check_status(package, True)
        except ImportError:
            check_status(package, False, f"Install with: pip install {package}")
            all_ok = False
    
    return all_ok

def check_external_tools():
    """Check external tools (ADB, Tesseract, scrcpy)"""
    check_header("External Tools")
    
    all_ok = True
    
    # Check config.json
    config_path = Path("config.json")
    if not config_path.exists():
        check_status("config.json", False, "Configuration file not found")
        return False
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Check ADB
    adb_path = Path(config['paths']['platform_tools']) / "adb.exe"
    if adb_path.exists():
        check_status("ADB", True, str(adb_path))
    else:
        check_status("ADB", False, f"Not found at: {adb_path}")
        all_ok = False
    
    # Check Tesseract
    tesseract_path = Path(config['paths']['tesseract'])
    if tesseract_path.exists():
        try:
            result = subprocess.run(
                [str(tesseract_path), '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.split('\n')[0]
            check_status("Tesseract OCR", True, version)
        except Exception as e:
            check_status("Tesseract OCR", False, str(e))
            all_ok = False
    else:
        check_status("Tesseract OCR", False, f"Not found at: {tesseract_path}")
        print("  -> Download: https://github.com/UB-Mannheim/tesseract/wiki")
        all_ok = False
    
    # Check scrcpy
    try:
        result = subprocess.run(
            ['scrcpy', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.split('\n')[0]
        check_status("scrcpy", True, version)
    except FileNotFoundError:
        check_status("scrcpy", False, "Not found in PATH")
        all_ok = False
    except Exception as e:
        check_status("scrcpy", False, str(e))
        all_ok = False
    
    return all_ok

def check_adb_connection():
    """Check ADB device connection"""
    check_header("ADB Device Connection")
    
    config_path = Path("config.json")
    with open(config_path) as f:
        config = json.load(f)
    
    adb_path = Path(config['paths']['platform_tools']) / "adb.exe"
    
    try:
        # Check for connected devices
        result = subprocess.run(
            [str(adb_path), 'devices'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        devices = [line for line in lines if line.strip() and 'device' in line]
        
        if devices:
            for device in devices:
                device_id = device.split()[0]
                check_status(f"Device {device_id}", True)
            
            # Get device info
            result = subprocess.run(
                [str(adb_path), 'shell', 'getprop', 'ro.product.model'],
                capture_output=True,
                text=True,
                timeout=5
            )
            model = result.stdout.strip()
            
            result = subprocess.run(
                [str(adb_path), 'shell', 'getprop', 'ro.build.version.release'],
                capture_output=True,
                text=True,
                timeout=5
            )
            android_version = result.stdout.strip()
            
            print(f"\n  Device Model: {model}")
            print(f"  Android Version: {android_version}")
            
            return True
        else:
            check_status("ADB Device", False, "No devices found")
            print("\n  Troubleshooting:")
            print("  1. Enable USB Debugging on your device")
            print("  2. Connect via USB")
            print("  3. Accept the USB debugging prompt on device")
            print("  4. Run: adb devices")
            return False
            
    except Exception as e:
        check_status("ADB Connection", False, str(e))
        return False

def check_output_directories():
    """Check if output directories exist"""
    check_header("Output Directories")
    
    config_path = Path("config.json")
    with open(config_path) as f:
        config = json.load(f)
    
    output_folder = Path(config['paths']['output_folder'])
    
    dirs = {
        'Main Output': output_folder,
        'Screenshots': output_folder / 'screenshots',
        'Text Data': output_folder / 'text_data'
    }
    
    all_ok = True
    for name, path in dirs.items():
        if path.exists():
            check_status(name, True, str(path))
        else:
            path.mkdir(parents=True, exist_ok=True)
            check_status(name, True, f"Created: {path}")
    
    return all_ok

def test_scrcpy_launch():
    """Test if scrcpy can launch successfully"""
    check_header("scrcpy Launch Test")
    
    print("Attempting to launch scrcpy for 3 seconds...")
    print("(Window should appear briefly, then close)")
    
    try:
        process = subprocess.Popen(
            ['scrcpy', '--max-size', '1920', '--window-title', 'TEST'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        import time
        time.sleep(3)
        
        process.terminate()
        process.wait(timeout=5)
        
        check_status("scrcpy Launch", True, "Successfully launched and terminated")
        return True
        
    except Exception as e:
        check_status("scrcpy Launch", False, str(e))
        return False

def test_ocr():
    """Test OCR functionality"""
    check_header("OCR Test")
    
    try:
        import pytesseract
        from PIL import Image, ImageDraw, ImageFont
        
        config_path = Path("config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        tesseract_path = Path(config['paths']['tesseract'])
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
        
        # Create test image with text
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 30), "Test OCR Text 123", fill='black')
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        
        if "Test" in text or "OCR" in text:
            check_status("OCR Test", True, f"Extracted: '{text.strip()}'")
            return True
        else:
            check_status("OCR Test", False, f"Unexpected result: '{text.strip()}'")
            return False
            
    except Exception as e:
        check_status("OCR Test", False, str(e))
        return False

def print_summary(results):
    """Print test summary"""
    check_header("Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} [OK]")
    print(f"Failed: {failed} [FAIL]")
    
    if failed == 0:
        print("\n" + "="*60)
        print(" [OK] All tests passed! System is ready.")
        print("="*60)
        print("\nYou can now run:")
        print("  python kindle_capture.py")
        print("  or")
        print("  python kindle_capture_cli.py --book \"Title\" --start 1 --end 10")
        return True
    else:
        print("\n" + "="*60)
        print(" [FAIL] Some tests failed. Fix issues above.")
        print("="*60)
        print("\nFailed tests:")
        for name, passed in results.items():
            if not passed:
                print(f"  - {name}")
        return False

def main():
    """Run all system tests"""
    print("\n" + "="*60)
    print(" Kindle Capture System Test")
    print("="*60)
    
    results = {}
    
    # Run all tests
    results['Python Packages'] = check_python_packages()
    results['External Tools'] = check_external_tools()
    results['ADB Connection'] = check_adb_connection()
    results['Output Directories'] = check_output_directories()
    results['OCR Test'] = test_ocr()
    
    # Optional: scrcpy launch test (requires device)
    if results['ADB Connection']:
        try:
            results['scrcpy Launch'] = test_scrcpy_launch()
        except:
            results['scrcpy Launch'] = False
    
    # Print summary
    success = print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nFatal error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
