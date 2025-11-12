"""
Direct ADB Screenshot Capture - Bypass scrcpy window issues
This captures screenshots directly from Android device via ADB
"""
import subprocess
import os
import time
from pathlib import Path

class DirectADBCapture:
    def __init__(self):
        self.adb_path = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
        self.output_folder = Path("adb_captures")
        self.output_folder.mkdir(exist_ok=True)
    
    def take_screenshot(self, filename):
        """Take screenshot directly from Android device"""
        print(f"📸 Taking ADB screenshot: {filename}")
        
        # Device path for screenshot
        device_path = f"/sdcard/{filename}"
        local_path = self.output_folder / filename
        
        try:
            # Take screenshot on device
            print("  • Taking screenshot on device...")
            result1 = subprocess.run([
                self.adb_path, "shell", "screencap", "-p", device_path
            ], capture_output=True, text=True)
            
            if result1.returncode != 0:
                print(f"  ❌ Screenshot failed: {result1.stderr}")
                return False
            
            # Pull screenshot to computer
            print("  • Pulling screenshot to computer...")
            result2 = subprocess.run([
                self.adb_path, "pull", device_path, str(local_path)
            ], capture_output=True, text=True)
            
            if result2.returncode != 0:
                print(f"  ❌ Pull failed: {result2.stderr}")
                return False
            
            # Clean up device file
            subprocess.run([
                self.adb_path, "shell", "rm", device_path
            ], capture_output=True)
            
            # Check file size
            if local_path.exists():
                file_size = local_path.stat().st_size
                print(f"  ✅ Success! File size: {file_size:,} bytes")
                return True
            else:
                print("  ❌ File not found after pull")
                return False
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            return False
    
    def turn_page(self):
        """Turn page via ADB swipe"""
        try:
            print("  📄 Turning page...")
            result = subprocess.run([
                self.adb_path, "shell", "input", "swipe",
                "1000", "700",  # From (right side, middle)
                "400", "700",   # To (left side, middle)
                "300"           # Duration 300ms
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✅ Page turned")
                return True
            else:
                print(f"  ❌ Page turn failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Page turn exception: {e}")
            return False
    
    def batch_capture(self, start_page, num_pages, delay=2.0):
        """Capture multiple pages with page turning"""
        print("🔥 Direct ADB Batch Capture")
        print("=" * 50)
        print(f"Capturing {num_pages} pages starting from page {start_page}")
        print(f"Page delay: {delay} seconds")
        print(f"Output folder: {self.output_folder.absolute()}")
        
        input("\nMake sure Kindle is on the starting page. Press Enter to begin...")
        
        success_count = 0
        
        for i in range(num_pages):
            current_page = start_page + i
            filename = f"page_{current_page:04d}.png"
            
            print(f"\n[{i+1}/{num_pages}] Page {current_page}")
            
            if self.take_screenshot(filename):
                success_count += 1
            else:
                print("⚠️ Screenshot failed")
            
            # Turn page (except last one)
            if i < num_pages - 1:
                if self.turn_page():
                    print(f"  ⏱️ Waiting {delay}s for page load...")
                    time.sleep(delay)
                else:
                    print("⚠️ Page turn failed")
                    choice = input("Continue anyway? (y/N): ")
                    if choice.lower() != 'y':
                        break
        
        print("\n" + "=" * 50)
        print("🎯 CAPTURE COMPLETE")
        print("=" * 50)
        print(f"Total attempts: {num_pages}")
        print(f"Successful: {success_count}")
        print(f"Failed: {num_pages - success_count}")
        print(f"Output: {self.output_folder.absolute()}")
        
        return success_count > 0

def test_adb_screenshot():
    """Test a single ADB screenshot"""
    capture = DirectADBCapture()
    
    print("🧪 Testing ADB Screenshot")
    print("=" * 30)
    
    if capture.take_screenshot("test_adb.png"):
        # Try to get image info
        test_file = capture.output_folder / "test_adb.png"
        try:
            from PIL import Image
            img = Image.open(test_file)
            print(f"  📐 Image size: {img.size}")
            print(f"  🎨 Mode: {img.mode}")
        except Exception as e:
            print(f"  ⚠️ Could not analyze image: {e}")
        
        return True
    else:
        return False

if __name__ == "__main__":
    # First test a single screenshot
    if test_adb_screenshot():
        print("\n" + "✅" * 20)
        print("ADB screenshot working! Ready for batch capture.")
        
        # Ask if user wants to do batch capture
        choice = input("\nDo batch capture now? (y/N): ")
        if choice.lower() == 'y':
            start = int(input("Starting page: "))
            count = int(input("Number of pages: "))
            
            capture = DirectADBCapture()
            capture.batch_capture(start, count)
    else:
        print("\n❌ ADB screenshot failed. Check ADB connection.")