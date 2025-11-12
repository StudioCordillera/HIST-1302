"""
Auto-Crop Black Bars from Captures
Automatically detects and removes black bars from phone status bar
"""
import time
import win32gui
import win32con
import win32ui
from PIL import Image, ImageChops
import numpy as np
from pathlib import Path

def find_window():
    """Find scrcpy/Phone Mirror window"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if any(kw in title.lower() for kw in ['scrcpy', 'phone mirror', 'android']):
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    if windows:
        return windows[0]
    return None, None

def capture_client_area(hwnd):
    """Capture ONLY the client area"""
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top
    
    hwnd_dc = win32gui.GetDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)
    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    
    return img

def auto_crop_black_bars(img, threshold=10):
    """Automatically crop black bars from image"""
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
        cropped = img.crop((left_crop, top_crop, right_crop, bottom_crop))
        
        print(f"  Original size: {img.size}")
        print(f"  Cropped to: {cropped.size}")
        print(f"  Removed: {top_crop}px from top, {img.height-bottom_crop}px from bottom")
        
        return cropped
    
    return img

def swipe_page():
    """Swipe to next page via ADB"""
    import subprocess
    adb = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
    subprocess.run([adb, "shell", "input", "swipe", "800", "500", "200", "500", "200"], capture_output=True)

# Main test
print("="*60)
print(" Auto-Crop Test - Remove Black Bars")
print("="*60)

hwnd, title = find_window()
if not hwnd:
    print("\n[FAIL] No scrcpy/Phone Mirror window found!")
    input("Press Enter to exit...")
    exit()

print(f"\n[OK] Found: {title}")
print("\nMake sure Kindle is on page iii (Brief Contents)")
input("Press Enter when ready...")

out = Path("test_captures")
out.mkdir(exist_ok=True)

print("\n[1/2] Capturing and cropping page iii...")
img = capture_client_area(hwnd)
cropped = auto_crop_black_bars(img)
cropped.save(out / "cropped_page_iii.png", 'PNG')
print("  [OK] Saved")

print("[1/2] Turning page...")
swipe_page()
time.sleep(2.5)

print("[2/2] Capturing and cropping page iv...")
img = capture_client_area(hwnd)
cropped = auto_crop_black_bars(img)
cropped.save(out / "cropped_page_iv.png", 'PNG')
print("  [OK] Saved")

print("\n" + "="*60)
print(f" Test complete! Check: {out.absolute()}")
print("="*60)
print("\nThese images should have NO black bars!")
print("Content only - ready for OCR!")

input("\nPress Enter to exit...")
