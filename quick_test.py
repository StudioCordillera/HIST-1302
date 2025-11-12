"""
Simple Interactive Test - Just capture 2 test pages
"""
import time
import win32gui
import win32con
import win32ui
from PIL import Image
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

def capture(hwnd, path):
    """Capture window screenshot"""
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)
    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    img.save(path, 'PNG')
    
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

def swipe_page():
    """Swipe to next page via ADB"""
    import subprocess
    adb = r"C:\Users\WORK_ADMIN\Projects\01_TOOLS\ADB_Tools\platform-tools\adb.exe"
    subprocess.run([adb, "shell", "input", "swipe", "800", "500", "200", "500", "200"], capture_output=True)

# Main test
print("="*60)
print(" Quick 2-Page Test")
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

print("\n[1/2] Capturing page iii...")
capture(hwnd, out / "test_page_iii.png")
print("  [OK] Saved")

print("[1/2] Turning page...")
swipe_page()
time.sleep(2.5)

print("[2/2] Capturing page iv...")
capture(hwnd, out / "test_page_iv.png")
print("  [OK] Saved")

print("\n" + "="*60)
print(f" Test complete! Check: {out.absolute()}")
print("="*60)
print("\nIf images look good, run the full capture:")
print("  python test_capture_toc.py")

input("\nPress Enter to exit...")
