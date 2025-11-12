"""
Quick test to verify the fixed window capture
This should capture the full content with no black borders
"""
import sys
from pathlib import Path

# Test if we can import kindle_capture
try:
    from kindle_capture import KindleCaptureConfig, ScrcpyController
    print("[OK] Successfully imported kindle_capture module")
except ImportError as e:
    print(f"[FAIL] Cannot import kindle_capture: {e}")
    print("\nMake sure you've installed all dependencies:")
    print("  pip install -r requirements.txt")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Test if numpy is available
try:
    import numpy as np
    print("[OK] numpy is available")
except ImportError:
    print("[FAIL] numpy is not installed")
    print("\nPlease install numpy:")
    print("  pip install numpy")
    input("\nPress Enter to exit...")
    sys.exit(1)

print("\n" + "="*60)
print(" Testing Fixed Window Capture")
print("="*60)
print("\nThis test will:")
print("  1. Find the scrcpy/Phone Mirror window")
print("  2. Capture the CLIENT AREA (no borders/titlebar)")
print("  3. AUTO-CROP any black bars")
print("  4. Save to test_captures/fixed_test.png")

input("\nMake sure scrcpy is running with Kindle open.\nPress Enter to start test...")

# Create config and controller
config = KindleCaptureConfig()
controller = ScrcpyController(config)

# Find the window
print("\nLooking for scrcpy window...")
if not controller.find_window():
    print("[FAIL] Could not find scrcpy window!")
    print("\nMake sure:")
    print("  - scrcpy is running")
    print("  - The window is visible (not minimized)")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"[OK] Found window: handle {controller.window_handle}")

# Create output folder
out = Path("test_captures")
out.mkdir(exist_ok=True)

# Capture test screenshot
print("\nCapturing screenshot with new method...")
output_path = out / "fixed_test.png"

if controller.capture_window(output_path):
    print(f"[OK] Screenshot saved to: {output_path.absolute()}")
    print("\n" + "="*60)
    print(" SUCCESS! ")
    print("="*60)
    print("\nCheck the screenshot - it should show:")
    print("  ✓ Full content area (no window borders)")
    print("  ✓ No black bars (auto-cropped)")
    print("  ✓ Clean page content ready for OCR")
else:
    print("[FAIL] Screenshot capture failed")

input("\nPress Enter to exit...")
