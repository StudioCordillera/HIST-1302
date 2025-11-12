"""
Quick window test - just find and capture one screenshot
"""
from simple_batch_capture import SimpleBatchCapture
from pathlib import Path

print("Quick Capture Test")
print("=" * 40)

capture = SimpleBatchCapture()

print("1. Finding scrcpy window...")
if capture.find_scrcpy_window():
    print("2. Capturing single screenshot...")
    
    test_file = Path("quick_test.png")
    if capture.capture_screen(test_file):
        print(f"✅ SUCCESS! Screenshot saved: {test_file.absolute()}")
        print(f"File size: {test_file.stat().st_size} bytes")
    else:
        print("❌ Capture failed")
else:
    print("❌ No window found - make sure scrcpy is running")

print("\nTest complete!")