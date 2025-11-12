"""
Automated Kindle Page Capture and OCR Tool
Captures pages from Kindle app on Android via scrcpy, performs OCR, and creates markdown output
"""

import subprocess
import time
import os
import sys
from pathlib import Path
import win32gui
import win32con
import win32ui
from PIL import Image
import numpy as np
import pytesseract
from datetime import datetime
import json
import re

class KindleCaptureConfig:
    """Configuration settings for the capture process"""
    
    def __init__(self):
        # Paths
        self.platform_tools_path = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools"
        self.adb_path = os.path.join(self.platform_tools_path, "adb.exe")
        self.output_folder = Path("kindle_captures")
        self.screenshots_folder = self.output_folder / "screenshots"
        self.text_folder = self.output_folder / "text_data"
        
        # scrcpy settings
        self.scrcpy_window_title = "scrcpy"
        self.scrcpy_max_size = 1920  # Full resolution
        self.scrcpy_bitrate = "8M"
        
        # Capture settings
        self.page_turn_delay = 2.5  # Seconds to wait after page turn
        self.initial_delay = 3.0  # Seconds to wait for scrcpy to fully load
        
        # OCR settings
        self.tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust if needed
        self.ocr_lang = "eng"
        
        # Create directories
        self.output_folder.mkdir(exist_ok=True)
        self.screenshots_folder.mkdir(exist_ok=True)
        self.text_folder.mkdir(exist_ok=True)

class ScrcpyController:
    """Manages scrcpy connection and window control"""
    
    def __init__(self, config):
        self.config = config
        self.process = None
        self.window_handle = None
        
    def start_scrcpy(self):
        """Launch scrcpy with optimal settings"""
        print("Starting scrcpy...")
        
        cmd = [
            "scrcpy",
            "--max-size", str(self.config.scrcpy_max_size),
            "--bit-rate", self.config.scrcpy_bitrate,
            "--window-title", self.config.scrcpy_window_title,
            "--stay-awake",
            "--turn-screen-off"  # Turn off device screen to save battery
        ]
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for window to appear
            time.sleep(self.config.initial_delay)
            self.find_window()
            
            if self.window_handle:
                print(f"[OK] scrcpy started successfully (PID: {self.process.pid})")
                return True
            else:
                print("[FAIL] Failed to find scrcpy window")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error starting scrcpy: {e}")
            return False
    
    def find_window(self):
        """Find the scrcpy window handle"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if self.config.scrcpy_window_title in title:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            self.window_handle = windows[0]
            # Keep window visible and on top for proper capture
            win32gui.SetWindowPos(
                self.window_handle,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
            return True
        return False
    
    def get_window_rect(self):
        """Get window dimensions"""
        if self.window_handle:
            rect = win32gui.GetWindowRect(self.window_handle)
            return {
                'left': rect[0],
                'top': rect[1],
                'right': rect[2],
                'bottom': rect[3],
                'width': rect[2] - rect[0],
                'height': rect[3] - rect[1]
            }
        return None
    
    def capture_window(self, output_path):
        """Capture screenshot of the scrcpy window (client area only with auto-crop)"""
        if not self.window_handle:
            print("[ERROR] No window handle found")
            return False
        
        try:
            # Bring window to foreground to ensure proper capture
            win32gui.SetForegroundWindow(self.window_handle)
            time.sleep(0.3)  # Brief delay to ensure window is ready
            
            # Get CLIENT area dimensions (content only, no borders/titlebar)
            left, top, right, bottom = win32gui.GetClientRect(self.window_handle)
            width = right - left
            height = bottom - top
            
            # Get the DC of the CLIENT area (not window DC)
            hwnd_dc = win32gui.GetDC(self.window_handle)  # GetDC for client area
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            
            # Create bitmap
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(save_bitmap)
            
            # BitBlt from client area
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
            
            # Save to file
            bmpinfo = save_bitmap.GetInfo()
            bmpstr = save_bitmap.GetBitmapBits(True)
            
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Auto-crop black bars (phone status bar, etc.)
            img = self.auto_crop_black_bars(img)
            
            img.save(output_path, 'PNG')
            
            # Cleanup
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.window_handle, hwnd_dc)
            
            return True
            
        except Exception as e:
            print(f"[FAIL] Error capturing window: {e}")
            return False
    
    def auto_crop_black_bars(self, img, threshold=10):
        """Automatically crop black bars from image (phone status bar, etc.)"""
        import numpy as np
        
        # Convert to numpy array
        np_img = np.array(img)
        
        # Find rows that aren't mostly black
        row_brightness = np_img.mean(axis=(1, 2))
        content_rows = row_brightness > threshold
        
        # Find columns that aren't mostly black
        col_brightness = np_img.mean(axis=(0, 2))
        content_cols = col_brightness > threshold
        
        # Find the bounding box of content
        if content_rows.any() and content_cols.any():
            top_crop = content_rows.argmax()
            bottom_crop = len(content_rows) - content_rows[::-1].argmax()
            left_crop = content_cols.argmax()
            right_crop = len(content_cols) - content_cols[::-1].argmax()
            
            # Crop the image
            return img.crop((left_crop, top_crop, right_crop, bottom_crop))
        
        return img
    
    def stop_scrcpy(self):
        """Stop scrcpy process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("[OK] scrcpy stopped")

class ADBController:
    """Manages ADB commands for device interaction"""
    
    def __init__(self, config):
        self.config = config
        self.adb = config.adb_path
    
    def execute_command(self, command):
        """Execute ADB command"""
        try:
            result = subprocess.run(
                [self.adb] + command,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout, result.stderr
        except Exception as e:
            print(f"[FAIL] ADB command failed: {e}")
            return None, str(e)
    
    def tap_screen(self, x, y):
        """Simulate screen tap at coordinates"""
        stdout, stderr = self.execute_command(["shell", "input", "tap", str(x), str(y)])
        return stdout is not None
    
    def swipe_screen(self, x1, y1, x2, y2, duration=300):
        """Simulate swipe gesture"""
        stdout, stderr = self.execute_command([
            "shell", "input", "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration)
        ])
        return stdout is not None
    
    def press_key(self, keycode):
        """Press a key (e.g., KEYCODE_PAGE_DOWN = 93)"""
        stdout, stderr = self.execute_command(["shell", "input", "keyevent", str(keycode)])
        return stdout is not None
    
    def turn_page_forward(self):
        """Turn page forward in Kindle (swipe left or tap right side)"""
        # Option 1: Swipe left (more reliable for Kindle)
        return self.swipe_screen(800, 500, 200, 500, 200)
        
        # Option 2: Tap right side (uncomment if preferred)
        # return self.tap_screen(900, 500)

class OCRProcessor:
    """Handles OCR processing of captured images"""
    
    def __init__(self, config):
        self.config = config
        
        # Set tesseract path if specified
        if os.path.exists(config.tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
        
    def process_image(self, image_path):
        """Extract text from image using OCR"""
        try:
            img = Image.open(image_path)
            
            # Preprocess image for better OCR
            img = self.preprocess_image(img)
            
            # Perform OCR
            text = pytesseract.image_to_string(
                img,
                lang=self.config.ocr_lang,
                config='--psm 6'  # Assume uniform block of text
            )
            
            return self.clean_text(text)
            
        except Exception as e:
            print(f"[FAIL] OCR failed for {image_path}: {e}")
            return ""
    
    def preprocess_image(self, img):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        img = img.convert('L')
        
        # Optional: Apply thresholding or other enhancements
        # img = img.point(lambda x: 0 if x < 128 else 255, '1')
        
        return img
    
    def clean_text(self, text):
        """Clean up OCR output"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')  # Common misread
        
        return text.strip()

class KindleCaptureOrchestrator:
    """Main orchestrator for the capture process"""
    
    def __init__(self, config):
        self.config = config
        self.scrcpy = ScrcpyController(config)
        self.adb = ADBController(config)
        self.ocr = OCRProcessor(config)
        
    def capture_page_range(self, start_page, end_page, book_title):
        """Capture a range of pages from Kindle app"""
        print(f"\n{'='*60}")
        print(f"Starting capture: {book_title}")
        print(f"Pages: {start_page} to {end_page}")
        print(f"{'='*60}\n")
        
        # Start scrcpy
        if not self.scrcpy.start_scrcpy():
            print("[FAIL] Failed to start scrcpy. Exiting.")
            return False
        
        try:
            # Capture pages
            page_data = []
            total_pages = end_page - start_page + 1
            
            for i, page_num in enumerate(range(start_page, end_page + 1), 1):
                print(f"\n[{i}/{total_pages}] Capturing page {page_num}...")
                
                # Capture screenshot
                screenshot_path = self.config.screenshots_folder / f"page_{page_num:04d}.png"
                if self.scrcpy.capture_window(screenshot_path):
                    print(f"  [OK] Screenshot saved: {screenshot_path.name}")
                    
                    # Perform OCR
                    print(f"  [RUN] Running OCR...")
                    text = self.ocr.process_image(screenshot_path)
                    
                    if text:
                        # Save text data
                        text_path = self.config.text_folder / f"page_{page_num:04d}.txt"
                        text_path.write_text(text, encoding='utf-8')
                        print(f"  [OK] Text extracted ({len(text)} chars)")
                        
                        page_data.append({
                            'page_number': page_num,
                            'text': text,
                            'screenshot': str(screenshot_path)
                        })
                    else:
                        print(f"  [WARN] No text extracted")
                else:
                    print(f"  [FAIL] Screenshot failed")
                
                # Turn page (except on last page)
                if page_num < end_page:
                    print(f"  -> Turning page...")
                    self.adb.turn_page_forward()
                    time.sleep(self.config.page_turn_delay)
            
            # Generate markdown output
            if page_data:
                self.generate_markdown(page_data, book_title, start_page, end_page)
                print(f"\n{'='*60}")
                print(f"[OK] Capture complete! {len(page_data)} pages processed")
                print(f"{'='*60}\n")
            
            return True
            
        finally:
            # Cleanup
            self.scrcpy.stop_scrcpy()
    
    def generate_markdown(self, page_data, book_title, start_page, end_page):
        """Generate markdown file from captured pages"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.config.output_folder / f"{book_title}_{start_page}-{end_page}_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# {book_title}\n\n")
            f.write(f"**Pages:** {start_page} - {end_page}\n\n")
            f.write(f"**Captured:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"---\n\n")
            
            # Write page content
            for page in page_data:
                f.write(f"## Page {page['page_number']}\n\n")
                f.write(f"{page['text']}\n\n")
                f.write(f"---\n\n")
            
            # Write metadata
            f.write(f"\n## Metadata\n\n")
            f.write(f"- **Total Pages Captured:** {len(page_data)}\n")
            f.write(f"- **Screenshots Directory:** `{self.config.screenshots_folder}`\n")
            f.write(f"- **Text Data Directory:** `{self.config.text_folder}`\n")
        
        print(f"\n[OK] Markdown file created: {output_file}")
        
        # Also save JSON metadata
        json_file = output_file.with_suffix('.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'book_title': book_title,
                'start_page': start_page,
                'end_page': end_page,
                'timestamp': timestamp,
                'pages': page_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Metadata saved: {json_file}")

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print(" Kindle Capture & OCR Tool")
    print("="*60 + "\n")
    
    # Initialize configuration
    config = KindleCaptureConfig()
    
    # Check dependencies
    print("Checking dependencies...")
    if not os.path.exists(config.adb_path):
        print(f"[FAIL] ADB not found at: {config.adb_path}")
        return
    print(f"[OK] ADB found")
    
    if not os.path.exists(config.tesseract_path):
        print(f"[WARN] Tesseract not found at: {config.tesseract_path}")
        print("  Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Or update the path in the config")
        return
    print(f"[OK] Tesseract found")
    
    # Get user input
    print("\n" + "-"*60)
    book_title = input("Enter book title: ").strip()
    start_page = int(input("Enter starting page number: "))
    end_page = int(input("Enter ending page number: "))
    print("-"*60)
    
    # Validate input
    if start_page > end_page:
        print("[FAIL] Start page must be <= end page")
        return
    
    # Confirm
    total_pages = end_page - start_page + 1
    print(f"\nReady to capture {total_pages} pages from '{book_title}'")
    print(f"Make sure your Kindle app is open on page {start_page}")
    confirm = input("\nProceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Run capture
    orchestrator = KindleCaptureOrchestrator(config)
    orchestrator.capture_page_range(start_page, end_page, book_title)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[FAIL] Interrupted by user")
    except Exception as e:
        print(f"\n[FAIL] Fatal error: {e}")
        import traceback
        traceback.print_exc()
