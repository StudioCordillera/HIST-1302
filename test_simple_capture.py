"""
Test the Simple Batch Capture - Just test capture function
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are available"""
    print("Testing imports...")
    
    try:
        import win32gui
        print("  ✓ win32gui")
    except ImportError:
        print("  ✗ win32gui (install pywin32)")
        return False
    
    try:
        import win32con
        print("  ✓ win32con")
    except ImportError:
        print("  ✗ win32con (install pywin32)")
        return False
    
    try:
        import win32ui
        print("  ✓ win32ui")
    except ImportError:
        print("  ✗ win32ui (install pywin32)")
        return False
    
    try:
        import numpy as np
        print("  ✓ numpy")
    except ImportError:
        print("  ✗ numpy (install numpy)")
        return False
    
    try:
        from PIL import Image
        print("  ✓ PIL (Pillow)")
    except ImportError:
        print("  ✗ PIL (install Pillow)")
        return False
    
    return True

def test_adb():
    """Test ADB connection"""
    import subprocess
    
    adb_path = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
    
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            devices = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = [d for d in devices if d.strip() and not d.startswith('*')]
            if devices:
                print(f"  ✓ ADB connected to {len(devices)} device(s)")
                for device in devices:
                    print(f"    - {device}")
                return True
            else:
                print("  ⚠️ ADB working but no devices connected")
                return False
        else:
            print(f"  ✗ ADB error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ ADB test failed: {e}")
        return False

def test_single_capture():
    """Test capturing a single screenshot"""
    try:
        from simple_batch_capture import SimpleBatchCapture
        
        capture = SimpleBatchCapture()
        
        # Find window
        if not capture.find_scrcpy_window():
            return False
        
        # Create test output
        test_path = Path("test_single_capture.png")
        
        print("Testing single capture...")
        if capture.capture_screen(test_path):
            print(f"  ✓ Test capture saved: {test_path.absolute()}")
            return True
        else:
            print("  ✗ Test capture failed")
            return False
            
    except Exception as e:
        print(f"  ✗ Capture test failed: {e}")
        return False

def main():
    print("=" * 60)
    print(" Simple Batch Capture - Test")
    print("=" * 60)
    
    all_good = True
    
    # Test 1: Imports
    print("\n1. Testing Python packages...")
    if not test_imports():
        print("\n❌ Missing required packages! Install with:")
        print("  pip install pywin32 Pillow numpy")
        all_good = False
    
    # Test 2: ADB
    print("\n2. Testing ADB connection...")
    if not test_adb():
        print("\n⚠️ ADB issues detected. Make sure:")
        print("  - Your Android device is connected via USB")
        print("  - USB debugging is enabled")
        print("  - You've authorized the ADB connection")
        all_good = False
    
    # Test 3: Window capture (only if other tests pass)
    if all_good:
        print("\n3. Testing window capture...")
        print("  Make sure scrcpy or Phone Mirror is running with Kindle open")
        input("  Press Enter when ready...")
        
        if not test_single_capture():
            print("\n⚠️ Window capture issues detected. Make sure:")
            print("  - scrcpy is running (or Phone Mirror app)")
            print("  - The window is visible and not minimized")
            print("  - Kindle app is open on your device")
            all_good = False
    
    # Results
    print("\n" + "=" * 60)
    if all_good:
        print("✅ ALL TESTS PASSED!")
        print("\nYour system is ready for batch capture!")
        print("Run: python simple_batch_capture.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nFix the issues above before running batch capture.")
    print("=" * 60)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()