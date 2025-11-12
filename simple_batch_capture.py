"""
Simple Batch Screen Capture Script
Simplified version focusing on: Capture → Scroll → Repeat
No OCR, just clean screenshots for a specified page range
"""
import time
import subprocess
import win32gui
import win32con
import win32ui
from PIL import Image
import numpy as np
from pathlib import Path

class SimpleBatchCapture:
    def __init__(self):
        # Configuration
        self.adb_path = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
        self.output_folder = Path("batch_captures")
        self.page_turn_delay = 2.5  # Seconds between captures
        
        # Create output directory
        self.output_folder.mkdir(exist_ok=True)
        
        # Window handle will be set when found
        self.window_handle = None
    
    def find_scrcpy_window(self):
        """Find the scrcpy or Phone Mirror window"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                # Look for common window titles
                keywords = ['scrcpy', 'phone mirror', 'android', 'kindle']
                if any(keyword in title.lower() for keyword in keywords):
                    windows.append((hwnd, title))
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            self.window_handle, title = windows[0]
            print(f"[OK] Found window: {title}")
            return True
        else:
            print("[FAIL] No scrcpy/Phone Mirror window found!")
            print("Make sure scrcpy is running or your phone mirroring app is open")
            return False
    
    def capture_screen(self, output_path):
        """Capture the current screen and save to file"""
        if not self.window_handle:
            print("[ERROR] No window handle found")
            return False
        
        try:
            # Bring window to foreground
            win32gui.SetForegroundWindow(self.window_handle)
            time.sleep(0.3)  # Brief pause to ensure window is ready
            
            # Get client area (content only, no borders)
            left, top, right, bottom = win32gui.GetClientRect(self.window_handle)
            width = right - left
            height = bottom - top
            
            # Capture the client area
            hwnd_dc = win32gui.GetDC(self.window_handle)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(save_bitmap)
            
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
            
            # Convert to PIL Image
            bmpinfo = save_bitmap.GetInfo()
            bmpstr = save_bitmap.GetBitmapBits(True)
            
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Auto-crop black bars if any
            img = self.auto_crop_black_bars(img)
            
            # Save the image
            img.save(output_path, 'PNG')
            
            # Cleanup
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.window_handle, hwnd_dc)
            
            print(f"  ✓ Captured: {output_path.name}")
            return True
            
        except Exception as e:
            print(f"  ✗ Capture failed: {e}")
            return False
    
    def auto_crop_black_bars(self, img, threshold=10):
        """Remove black bars from screenshot (status bars, etc.)"""
        try:
            # Convert PIL Image to numpy array
            img_array = np.array(img)
            
            # Calculate brightness for each row and column
            row_brightness = img_array.mean(axis=(1, 2))  # Average across width and channels
            col_brightness = img_array.mean(axis=(0, 2))  # Average across height and channels
            
            # Find content boundaries
            content_rows = row_brightness > threshold
            content_cols = col_brightness > threshold
            
            if content_rows.any() and content_cols.any():
                # Find first and last content rows/columns
                top = np.where(content_rows)[0][0]
                bottom = np.where(content_rows)[0][-1] + 1
                left = np.where(content_cols)[0][0]
                right = np.where(content_cols)[0][-1] + 1
                
                # Crop the image
                return img.crop((left, top, right, bottom))
            else:
                return img
                
        except Exception as e:
            print(f"  Warning: Auto-crop failed, using original: {e}")
            return img
    
    def turn_page(self):
        """Turn to next page using ADB swipe command"""
        try:
            # Swipe from right to left (next page)
            cmd = [
                self.adb_path, "shell", "input", "swipe",
                "800", "500",  # Start position (right side)
                "200", "500",  # End position (left side)
                "200"          # Duration in ms
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✓ Page turned")
                return True
            else:
                print(f"  ✗ Page turn failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ✗ Page turn error: {e}")
            return False
    
    def batch_capture(self, start_page, total_pages):
        """Main batch capture function"""
        print("=" * 60)
        print(f" Simple Batch Capture: {total_pages} pages")
        print("=" * 60)
        
        # Find the window
        if not self.find_scrcpy_window():
            return False
        
        print(f"\nCapturing {total_pages} pages starting from page {start_page}")
        print(f"Output folder: {self.output_folder.absolute()}")
        print(f"Page turn delay: {self.page_turn_delay} seconds")
        
        input("\n⚠️  Make sure Kindle is on the starting page and ready to capture.\nPress Enter to begin...")
        
        success_count = 0
        failed_count = 0
        
        for i in range(total_pages):
            current_page = start_page + i
            print(f"\n[{i+1}/{total_pages}] Page {current_page}:")
            
            # Generate filename with zero-padding
            filename = f"page_{current_page:04d}.png"
            output_path = self.output_folder / filename
            
            # Capture the current page
            if self.capture_screen(output_path):
                success_count += 1
            else:
                failed_count += 1
                print(f"  ⚠️  Failed to capture page {current_page}")
            
            # Turn page (except for the last one)
            if i < total_pages - 1:
                if self.turn_page():
                    print(f"  💤 Waiting {self.page_turn_delay}s for page to load...")
                    time.sleep(self.page_turn_delay)
                else:
                    print(f"  ⚠️  Failed to turn page from {current_page}")
                    # Ask user if they want to continue
                    choice = input("Continue anyway? (y/N): ").lower()
                    if choice != 'y':
                        break
        
        # Summary
        print("\n" + "=" * 60)
        print(" BATCH CAPTURE COMPLETE")
        print("=" * 60)
        print(f"Total pages: {total_pages}")
        print(f"Successfully captured: {success_count}")
        print(f"Failed: {failed_count}")
        print(f"Output folder: {self.output_folder.absolute()}")
        
        if success_count > 0:
            print(f"\n✅ {success_count} screenshots saved successfully!")
            print("   You can now run OCR processing on these images")
        
        return success_count > 0


def main():
    """Interactive main function"""
    capture = SimpleBatchCapture()
    
    print("Simple Batch Screen Capture Tool")
    print("=" * 60)
    print("This tool will:")
    print("  1. Find your scrcpy/Phone Mirror window")
    print("  2. Capture the current page")
    print("  3. Turn the page via ADB")
    print("  4. Wait for page to load")
    print("  5. Repeat for specified number of pages")
    print("\nPrerequisites:")
    print("  ✓ scrcpy running with your Android device")
    print("  ✓ Kindle app open on the starting page")
    print("  ✓ ADB connection working")
    
    print("\n" + "-" * 60)
    
    # Get user input
    try:
        start_page = int(input("Starting page number: "))
        total_pages = int(input("Total pages to capture: "))
        
        if total_pages <= 0 or start_page < 0:
            print("❌ Invalid page numbers!")
            return
        
        print(f"\n📋 Plan: Capture {total_pages} pages starting from page {start_page}")
        print(f"   Will capture pages {start_page} to {start_page + total_pages - 1}")
        
        # Final confirmation
        confirm = input("\nProceed? (y/N): ").lower()
        if confirm != 'y':
            print("Cancelled by user.")
            return
        
        # Start the capture process
        capture.batch_capture(start_page, total_pages)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Capture interrupted by user (Ctrl+C)")
    except ValueError:
        print("❌ Please enter valid numbers!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()